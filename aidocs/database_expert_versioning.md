# database_expert_versioning.md

## LATEST (Top = Current Version)
v1.0.1 | 2026-02-03 | Repository boundaries clarified
  • Changed: Explicit note that business layer owns transactions; repositories avoid commit/rollback
  • Reason: Align with modular design and prevent side effects
  • Revert command: git checkout v1.0.0 -- aidocs/database_expert_protocol.md

v1.0.0 | 2026-02-03 | New protocol foundation
  • Added: Database Expert Protocol with anti-hallucination gates and repository rules
  • Reason: Establish verifiable, minimal, production-safe ORM layer standards
  • Revert command: git rm --cached aidocs/database_expert_protocol.md aidocs/database_expert_versioning.md

