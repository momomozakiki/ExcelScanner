# FastAPI Expert Protocol (with SQLAlchemy ORM)

## Purpose
- Define strict, verifiable rules for building scalable, maintainable APIs using FastAPI that delegate business logic and data access properly.
- Prevent hallucination via documented checks; enforce clean architecture boundaries.

## Pre‑Action Checklist
- Read this protocol and confirm aidocs folder exists.
- Read latest notes in fastapi_versioning.md.
- Verify FastAPI, Pydantic (v2), and SQLAlchemy versions in use via official docs.
- Identify requested change as a single atomic task with clear outcome.

## Allowed Actions
- Implement route handlers that do auth/validation only; delegate to business services.
- Use Pydantic v2 models for request/response DTOs; strict typing.
- Apply JWT auth on protected routes; enable CORS with explicit allow lists.
- Integrate SQLAlchemy via repository pattern; do not expose Sessions outside repositories.
- Use dependency injection for services and repositories.

## Forbidden Actions
- Place business logic in route handlers.
- Return ORM models directly; always serialize DTOs.
- Accept raw SQL or user‑controlled table names.
- Log sensitive data (passwords/tokens/PII).
- Disable security middleware in any environment.

## Atomic API Verbs (≤3)
- get: read domain data via services/repositories.
- save: create/update via services with validation and transactions.
- delete: remove via services respecting soft‑delete policies.

## Modularity Rules
- One responsibility per function; split when description contains “and”.
- Keep cyclomatic complexity low; prefer small, composable handlers and services.

## Anti‑Hallucination Gates
- Do not invent framework features; verify against official FastAPI/Pydantic/SQLAlchemy docs.
- Confirm Pydantic v2 usage (e.g., field validators) per official docs.
- Cite OWASP/CWE identifiers for security recommendations.
- If uncertain: respond “Verify in official source”.
- Validate type signatures with strict type checking where available.

## Security Boundaries
- Authentication/authorization enforced in API layer; business decisions occur in services.
- Secrets loaded from environment/secure vaults; never hardcoded.
- Rate limit per user; sanitize all user strings.

## Output Requirements
- Provide references to official docs for non‑trivial API/security features.
- List changed files and validations (tests/lint/typecheck) executed.
- Avoid referencing non‑existent project artifacts.

## Protocol Compliance
- Never modify this protocol without explicit user approval.
- Flag conflicts with other agent protocols to the user.
