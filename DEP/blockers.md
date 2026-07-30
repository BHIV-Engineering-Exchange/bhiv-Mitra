# Blockers

## Current Blockers

| ID | Description | Severity | Owner | Status |
|----|-------------|----------|-------|--------|
| B-001 | External BHIV product APIs not yet live (UniGuru, SETU, etc.) | Medium | Team | Pending |
| B-002 | Capability Runtime (Kanishk) not yet integrated | High | Kanishk | Pending |
| B-003 | MongoDB required for Bucket persistence | High | DevOps | Resolved |

## Resolved Blockers

| ID | Description | Resolution |
|----|-------------|------------|
| B-003 | MongoDB required for Bucket persistence | Docker Compose provides MongoDB service |

## Dependencies

- Kanishk's Capability Runtime for execution engine integration
- Raj's Control Plane for routing through TANTRA
- Vijay's UniGuru Backend for intelligence integration
- Ashwini's Companion for execution state consumption
- Isha's Integration Layer for validation
