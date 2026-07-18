"""
MultilingualService — Language Detection & Translation for Mitra AI

Supports only English and Hindi. All other languages default to English.
No langdetect dependency — uses script-based detection for reliability.
"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("MultilingualService")

# Supported languages: English + Hindi only
SUPPORTED_LANGUAGES = {"en": "English", "hi": "Hindi"}

# Import translator (only for English ↔ Hindi)
try:
    from app.services.mitra_tts_integration.translator import (
        translate,
        translate_to_english,
        translate_from_english,
    )
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    logger.warning("[MultilingualService] Translator not available, translation disabled")


def _has_devanagari(text: str) -> bool:
    """Check if text contains Devanagari script (Hindi)."""
    for ch in text:
        if '\u0900' <= ch <= '\u097F':  # Devanagari Unicode block
            return True
    return False


def _is_english(text: str) -> bool:
    """Check if text looks like English (ASCII-based with common Latin characters)."""
    if not text:
        return True
    # If it has Devanagari, it's not English
    if _has_devanagari(text):
        return False
    # If mostly ASCII, treat as English
    ascii_count = sum(1 for ch in text if ord(ch) < 128)
    return ascii_count / max(len(text), 1) > 0.8


class MultilingualService:
    def __init__(self):
        pass

    def detect_language(self, text: str) -> str:
        """
        Detect language: returns 'hi' for Hindi (Devanagari), 'en' for everything else.
        No langdetect — purely script-based.
        """
        if not text or not text.strip():
            return "en"
        if _has_devanagari(text):
            return "hi"
        return "en"

    @staticmethod
    def _is_short_english_utterance(text: str) -> bool:
        if not text:
            return True
        if not text.isascii():
            return False
        short_phrases = {
            "hi", "hello", "hey", "thanks", "thank you", "bye", "goodbye",
            "who are you", "what is your name", "what's your name",
            "what can you do", "how are you",
        }
        if text in short_phrases:
            return True
        words = [part for part in text.split(" ") if part]
        greeting_tokens = {"hi", "hello", "hey"}
        if words and words[0] in greeting_tokens and len(words) <= 4:
            return True
        if len(words) <= 3 and all(word in {"hi", "hello", "hey", "thanks", "bye"} for word in words):
            return True
        return False

    def translate_text(self, text: str, target_lang: str, source_lang: str = None) -> str:
        """Translate text. Only supports en ↔ hi."""
        if not text or not text.strip():
            return text
        if target_lang == source_lang:
            return text
        if target_lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[MultilingualService] Unsupported target language: {target_lang}, returning original")
            return text
        if not TRANSLATOR_AVAILABLE:
            return text
        try:
            return translate(text, target_language=target_lang, source_language=source_lang or "auto")
        except Exception as e:
            logger.error(f"[MultilingualService] Translation failed: {e}")
            return text

    def translate_to_english(self, text: str, source_lang: str = "auto") -> str:
        """Translate Hindi → English."""
        if not TRANSLATOR_AVAILABLE:
            return text
        try:
            return translate_to_english(text, source_language=source_lang)
        except Exception as e:
            logger.error(f"[MultilingualService] Translation to English failed: {e}")
            return text

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """Translate English → Hindi."""
        if target_lang not in SUPPORTED_LANGUAGES:
            return text
        if not TRANSLATOR_AVAILABLE:
            return text
        try:
            return translate_from_english(text, target_language=target_lang)
        except Exception as e:
            logger.error(f"[MultilingualService] Translation from English failed: {e}")
            return text

    def get_language_metadata(self, text: str) -> Dict[str, Any]:
        """
        Get language metadata. Script-based detection only.
        """
        detected = self.detect_language(text)
        return {
            "detected_language": detected,
            "language_name": SUPPORTED_LANGUAGES.get(detected, "English"),
            "confidence": 1.0,
            "needs_translation": detected != "en",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def validate_language_support(self, language_code: str) -> bool:
        return language_code in SUPPORTED_LANGUAGES

    def get_supported_languages(self) -> list:
        return list(SUPPORTED_LANGUAGES.keys())
