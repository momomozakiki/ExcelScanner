# fastapi_versioning.md

## LATEST (Top = Current Version)
v1.0.1 | 2026-02-03 | Clean architecture alignment
  • Changed: Emphasized route=auth/validation only; services own business logic
  • Reason: Enforce separation of concerns and maintainability
  • Revert command: git checkout v1.0.0 -- aidocs/fastapi_protocol.md

v1.0.0 | 2026-02-03 | New protocol foundation
  • Added: FastAPI Expert Protocol with anti-hallucination gates and security boundaries
  • Reason: Establish verifiable, modular API standards
  • Revert command: git rm --cached aidocs/fastapi_protocol.md aidocs/fastapi_versioning.md
