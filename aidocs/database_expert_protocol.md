# Database Expert Protocol (SQLAlchemy + PostgreSQL)

## Purpose
- Define strict, verifiable rules for the database layer using SQLAlchemy ORM with PostgreSQL.
- Prevent hallucination; require official documentation checks and typed interfaces.
- Enforce repository boundaries and transaction ownership in business logic.

## Pre‑Action Checklist
- Confirm aidocs folder and this protocol file exist.
- Read latest version notes in database_expert_versioning.md.
- Verify SQLAlchemy and PostgreSQL versions against official docs before using features.
- Identify requested change as a single, atomic task with a clear outcome.

## Allowed Actions
- Implement repositories exposing only three atomic verbs:
  - get_by_id(id)
  - save(entity)
  - delete(id)
- Use typed domain models and DTOs; avoid exposing ORM models outside repositories.
- Use parameterized queries; avoid string-concatenated SQL.
- Use SQLAlchemy Core for complex queries where appropriate.
- Wrap writes in atomic transactions; ensure rollback on error.

## Forbidden Actions
- Expose Session/connection objects to higher layers.
- Commit or rollback transactions inside repositories if business layer owns boundaries.
- Execute raw SQL for business logic access outside repository interfaces.
- Claim ORM support for non-relational databases.

## Modularity Rules
- One responsibility per function; split when description contains “and”.
- Keep function complexity low and interfaces minimal.

## Anti‑Hallucination Gates
- Do not invent ORM features or methods; verify against SQLAlchemy official documentation.
- Verify async requirements: use AsyncSession and async engine only when project supports it.
- Validate relationships with explicit foreign_keys when ambiguity exists.
- Cite OWASP/CWE identifiers for security recommendations.
- If uncertain: respond “Verify in official source”.

## Security Boundaries
- Credentials only from environment/secret managers; never hardcoded.
- Input sanitized and validated before persistence; avoid SQL injection via parameters.
- Business layer owns transaction boundaries; repositories perform flush operations as required.

## Output Requirements
- Provide references to official docs for non-trivial ORM features.
- List changed files and validations (tests/lint/typecheck) executed.
- Avoid referencing non-existent project artifacts.

## Protocol Compliance
- Never modify this protocol without explicit user approval.
- Flag conflicts with other agent protocols to the user.

