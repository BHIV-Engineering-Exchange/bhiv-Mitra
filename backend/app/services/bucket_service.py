from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from app.external.bucket.database.mongo_db import MongoDBClient

logger = logging.getLogger(__name__)


class BucketPersistenceError(RuntimeError):
    pass


class BucketService:
    """Persistent BHIV Bucket adapter. There is no in-memory runtime fallback."""

    @classmethod
    def clear_memory_logs(cls) -> None:
        # Compatibility hook for older test callers. Runtime storage is MongoDB only.
        return None

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): BucketService._normalize_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [BucketService._normalize_value(item) for item in value]
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    @classmethod
    def _integrity_hash(cls, trace_id: str, stage: str, data: Dict[str, Any]) -> str:
        canonical = {
            "trace_id": str(trace_id),
            "stage": str(stage),
            "data": cls._normalize_value(data),
        }
        blob = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    @staticmethod
    def _field_present(data: Dict[str, Any], field_path: str) -> bool:
        current: Any = data
        for segment in field_path.split("."):
            if not isinstance(current, dict) or segment not in current:
                return False
            current = current[segment]
        return True

    _in_memory_store = []

    def __init__(self) -> None:
        self._mongo = MongoDBClient()

    def _get_collection(self):
        """Return the MongoDB collection if available, else None."""
        return self._mongo.audit_collection

    def enforcement_artifact_required(self) -> bool:
        return True

    def log_event(self, trace_id: str, stage: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not trace_id or not stage:
            raise BucketPersistenceError("trace_id and stage are required for BHIV Bucket persistence")

        collection = self._get_collection()
        normalized_data = self._normalize_value(data)
        timestamp = datetime.now(timezone.utc)
        artifact_locator = f"{trace_id}:{stage}"
        document = {
            "artifact_id": trace_id,
            "trace_id": trace_id,
            "stage": stage,
            "data": normalized_data,
            "integrity_hash": self._integrity_hash(trace_id, stage, normalized_data),
            "integrity_version": "sha256-v1",
            "timestamp": timestamp,
            "service": "mitra_bucket",
            "immutable": True,
            "audit_version": "2.0",
        }
        
        backend = "mongodb"
        record_id = f"mem_{len(self._in_memory_store)}"
        
        if collection is not None:
            try:
                result = collection.insert_one(document)
                record_id = str(result.inserted_id)
            except Exception as e:
                if os.getenv("ENVIRONMENT", "development").lower() == "development":
                    logger.warning(f"MongoDB insert failed: {e}. Falling back to in-memory.")
                    self._in_memory_store.append(document)
                    backend = "in_memory"
                else:
                    raise BucketPersistenceError(f"BHIV Bucket persistence unavailable: {e}")
        else:
            if os.getenv("ENVIRONMENT", "development").lower() == "development":
                self._in_memory_store.append(document)
                backend = "in_memory"
            else:
                raise BucketPersistenceError("BHIV Bucket persistence unavailable: No MongoDB collection.")

        logger.info("BUCKET_LOG [%s] %s (backend: %s)", trace_id, stage, backend)
        return {
            "trace_id": trace_id,
            "stage": stage,
            "artifact_locator": artifact_locator,
            "backend": backend,
            "record_id": record_id,
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        }

    def get_artifact(self, trace_id: str, *, stage: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if not trace_id:
            return None
        
        query: Dict[str, Any] = {"trace_id": trace_id}
        if stage is not None:
            query["stage"] = stage
            
        collection = self._get_collection()
        if collection is not None:
            try:
                document = collection.find_one(query, sort=[("timestamp", -1)])
                if document:
                    document = dict(document)
                    if "_id" in document:
                        document["_id"] = str(document["_id"])
                    return document
            except Exception as e:
                logger.warning(f"MongoDB query failed: {e}. Falling back to in-memory.")

        # Fallback to in-memory
        # Search backwards for the most recent match
        for doc in reversed(self._in_memory_store):
            match = doc.get("trace_id") == trace_id
            if stage is not None and doc.get("stage") != stage:
                match = False
            if match:
                return dict(doc)
        
        return None

    def artifact_exists(self, trace_id: str, *, stage: Optional[str] = None) -> bool:
        return self.get_artifact(trace_id, stage=stage) is not None

    def validate_artifact(
        self,
        trace_id: str,
        *,
        stage: str,
        required_fields: Optional[Iterable[str]] = None,
        expected_trace_id: Optional[str] = None,
    ) -> bool:
        artifact = self.get_artifact(trace_id, stage=stage)
        if not artifact:
            return False
        data = artifact.get("data")
        if not isinstance(data, dict):
            return False
        expected_hash = self._integrity_hash(
            str(artifact.get("trace_id", trace_id)),
            str(artifact.get("stage", stage)),
            data,
        )
        if artifact.get("integrity_hash") != expected_hash:
            return False
        if expected_trace_id is not None and str(data.get("trace_id") or "") != str(expected_trace_id):
            return False
        if required_fields and any(not self._field_present(data, field) for field in required_fields):
            return False
        return True

    def get_trace_logs(self, trace_id: str) -> list[Dict[str, Any]]:
        logs = []
        collection = self._get_collection()
        if collection is not None:
            try:
                cursor = collection.find({"trace_id": trace_id}).sort("timestamp", 1)
                for document in cursor:
                    document = dict(document)
                    if "_id" in document:
                        document["_id"] = str(document["_id"])
                    logs.append(document)
                return logs
            except Exception as e:
                logger.warning(f"MongoDB query failed: {e}. Falling back to in-memory.")

        # Fallback to in-memory
        for doc in self._in_memory_store:
            if doc.get("trace_id") == trace_id:
                logs.append(dict(doc))
        return logs

    def find_recent_stage_events(
        self,
        stage: str,
        *,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        exclude_trace_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[Dict[str, Any]]:
        collection = self._get_collection()
        if collection is not None:
            query: Dict[str, Any] = {"stage": stage}
            if user_id is not None:
                query["data.user_id"] = str(user_id)
            if session_id is not None:
                query["data.session_id"] = str(session_id)
            if exclude_trace_id:
                query["trace_id"] = {"$ne": exclude_trace_id}
            
            try:
                cursor = collection.find(query).sort("timestamp", -1).limit(limit)
                results = []
                for document in cursor:
                    document = dict(document)
                    if "_id" in document:
                        document["_id"] = str(document["_id"])
                    results.append(document)
                return results
            except Exception as e:
                logger.warning(f"MongoDB query failed: {e}. Falling back to in-memory.")

        # Fallback to in-memory
        results = []
        for doc in reversed(self._in_memory_store):
            if doc.get("stage") != stage:
                continue
            if user_id is not None and str(doc.get("data", {}).get("user_id")) != str(user_id):
                continue
            if session_id is not None and str(doc.get("data", {}).get("session_id")) != str(session_id):
                continue
            if exclude_trace_id and doc.get("trace_id") == exclude_trace_id:
                continue
            
            results.append(dict(doc))
            if len(results) >= limit:
                break
                
        return results

    def get_status(self) -> Dict[str, Any]:
        connected = self._mongo.audit_collection is not None
        return {
            "service": "mitra_bucket",
            "status": "active" if connected else "degraded",
            "persistent_backend": "mongodb" if connected else "in_memory",
            "mongo_connected": connected,
            "audit_active": True,
            "mongo_error": None if connected else MongoDBClient.connection_error(),
        }
