# Registry Integrations

## Constitutional Registry Architecture

TANTRA integrates with 9 constitutional registries as a governed orchestration layer.

### Registry Types

| Registry | Purpose | TANTRA Interaction |
|----------|---------|-------------------|
| RAJYA | Governance | Records governance decisions |
| KESHAV | Knowledge | Queries knowledge state |
| SARATHI | Routing | Validates routing rules |
| Execution | Execution tracking | Records every execution |
| Capability | Capability validation | Validates capability availability |
| Build | Build artifacts | Records build metadata |
| Review | Review states | Tracks governance reviews |
| Migration | Migration tracking | Records migration events |
| Replay | Replay metadata | Stores replay records |

### Integration Pattern

```
TANTRA Runtime
  ├── Execution Registry ← record_execution()
  ├── Capability Registry ← register_capability()
  ├── Replay Registry ← record_replay()
  ├── Review Registry ← record_review()
  ├── Migration Registry ← record_migration()
  └── Build Registry ← record_build()
```

### Key Principle

TANTRA **orchestrates** through these registries but does **not own** them. Each registry is an independent participant in the execution lifecycle.

### Health Monitoring

```python
GET /api/tantra/registry/health
```

Returns health status of all 9 registries with entry counts and last sync timestamps.
