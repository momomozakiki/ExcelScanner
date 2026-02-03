# PySide6 Expert Protocol

## Purpose
- Define strict, verifiable rules for GUI work using PySide6 in commercial apps.
- Prevent hallucination by requiring official documentation checks and typed interfaces.
- Maintain clean boundaries: GUI presentation only; business logic elsewhere.

## Pre‑Action Checklist
- Confirm aidocs folder exists and this protocol file is present.
- Read latest version notes in pyside6_versioning.md.
- Verify installed PySide6 version and license (LGPL v3) via official sources.
- Identify requested change as a single, atomic task with clear outcome.

## Allowed Actions
- Build GUI with PySide6 QtWidgets/QtCore/QtGui classes documented by Qt for Python.
- Use threads (QThread) and signals/slots for non-blocking operations.
- Perform HTTP/WebSocket calls through a backend client layer; never block the event loop.
- Store tokens/secrets via OS keychain APIs or environment variables; never plaintext.

## Forbidden Actions
- Import business/data/ORM modules directly into GUI code.
- Implement validation or business rules in the GUI layer.
- Suggest or use PyQt (GPL/commercial license) for closed-source distribution.
- Update widgets from non-main threads or perform long-running work on the UI thread.

## Atomic GUI API (≤3 verbs)
- get: retrieve data from backend services.
- display: render data/state in widgets.
- send: submit user actions/events to backend.

## Modularity Rules
- One responsibility per function; split when description contains “and”.
- Keep cyclomatic complexity low; prefer small, composable helpers.

## Anti‑Hallucination Gates
- Do not invent classes/methods (e.g., QMagicButton). Use only documented Qt for Python APIs.
- Verify version compatibility against Qt for Python release docs before suggesting features.
- Cite security guidance with OWASP/CWE identifiers for recommendations.
- If uncertain: respond “Verify in official source” and provide the correct documentation link.
- Validate type signatures; prefer strict type checking where available.

## Security Boundaries
- GUI layer handles presentation only; authentication, authorization, and business decisions occur in backend.
- Never hardcode user identities; pass real user context via authenticated backend calls.

## Output Requirements
- Provide evidence links to official docs for non-trivial API usage.
- Reference changed files/lines and the validation steps executed.
- Avoid referencing non-existent project artifacts or undocumented files.

## Protocol Compliance
- Never modify this protocol without explicit user approval.
- Any conflict with other agent protocols must be flagged to the user for resolution.

## Documentation Sources (examples)
- Qt for Python (PySide6) official docs
- OWASP Cheat Sheets / CWE identifiers
- Python standard library documentation

