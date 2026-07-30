# DEP Metadata — MITRA Universal Hover Companion

| Field             | Value                                             |
|-------------------|---------------------------------------------------|
| **Project**       | MITRA Universal Hover Companion                   |
| **Phase**         | Phase 1 Convergence                               |
| **Owner**         | Ashwini Wadekar                                   |
| **Sprint**        | AI-Augmented Execution Sprint (8–12 hrs)          |
| **Repository**    | MITRA-Universal-Companion                         |
| **Stack**         | Vanilla JS (Web Components) + Python/FastAPI      |
| **Created**       | 2026-07-29                                        |
| **Last Updated**  | 2026-07-30                                        |

## Scope

Build the one canonical MITRA Companion that follows the user across the entire BHIV ecosystem. MITRA should feel like the operating system companion — not a feature inside one application.

## Integration Dependencies

| Team Member    | Role                          | API Contract                        |
|----------------|-------------------------------|-------------------------------------|
| Raj Prajapati  | MITRA Control Plane           | `/api/assistant`, `/api/mitra/*`    |
| Ashmit         | TANTRA Runtime                | Event stream for execution state    |
| Kanishk        | Universal Capability Runtime  | Capability lifecycle events         |
| Pratham        | Production Runtime            | Deployment validation               |
| Vijay Dhawan   | UniGuru Backend               | Intelligence APIs via Raj           |
| Isha           | UniGuru Integration           | Cross-product continuity validation |
