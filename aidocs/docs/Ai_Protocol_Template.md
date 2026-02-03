## Universal AI Agent Protocol (Framework-Agnostic)
### Critical Rules
- Name–File alignment: `{agent_name}_expert_protocol.md`, `{agent_name}_expert_versioning.md`
- Single aidocs folder at project root
- Read agent protocol before action
- Anti-hallucination: no invented APIs/features; verify against official docs
- User approval required for protocol changes
### Core Principles (Apply to ALL AI Agents)
| Principle | Concrete Rule | Verification Method |
|-----------|---------------|---------------------|
| **Anti-Hallucination** | NEVER invent APIs/features — verify against official docs BEFORE output | `grep -r "non_existent_method" output/` must return 0 matches |
| **Expertise Boundary** | Work ONLY within documented expertise — never cross into other domains | Static analysis: `grep "import.*sqlalchemy" frontend_agent_output/` must return 0 |
| **Modular Core Functions** | Expose ≤3 atomic verbs per layer (e.g., `get`/`save`/`delete`) — NO monolithic functions | Cyclomatic complexity ≤5 per function (measured by `radon cc`) |
| **Protocol Compliance** | ALWAYS read `{expertise}_expert_protocol.md` from `{project_root}/aidocs` BEFORE acting | File existence check: `test -f aidocs/{agent}_expert_protocol.md` |
| **User Approval Gate** | NEVER modify protocols without explicit user approval | Versioning file timestamp must be AFTER user approval message |

### Aidocs Folder Structure (MANDATORY)

```
{project_root}/
└── aidocs/ # single folder at project root
    ├── {agent_name}_expert_protocol.md
    └── {agent_name}_expert_versioning.md
  
**Name–File Alignment Rule**
- Filenames MUST match the agent name exactly
- Library-specific names allowed (e.g., `sqlalchemy expert` → `sqlalchemy_expert_protocol.md`)
- If a mismatch is detected, rename files to match the agent name
```

**Critical Enforcement Rules**:
```bash
[ -d aidocs ] || exit 1
[ $(find . -type d -name aidocs | wc -l) -eq 1 ] || exit 1
[ -f "aidocs/${AGENT_NAME}_expert_protocol.md" ] || exit 1
```

### Versioning Format Specification (Optimized for Revertability)
```markdown
# {agent_name}_expert_versioning.md

## LATEST (Top = Current Version)
v3.0.1 | 2026-02-03 | PySide6 v6.5.0 compatibility
  • Changed: QThread usage pattern per Qt 6.5 deprecation warnings
  • Reason: Official Qt docs section 4.2.1 marks old pattern obsolete
  • Revert command: `git checkout v3.0.0 -- aidocs/pyside6_expert_protocol.md`

v3.0.0 | 2026-02-01 | New protocol foundation
  • Added: Anti-hallucination rule #4 (type-check all interfaces)
  • Reason: Production incident #2026-01-15 (type mismatch caused data loss)
  • Revert command: `git revert --no-commit v2.1.0..v3.0.0`

v2.1.0 | 2026-01-15 | Security hardening
  • Changed: Token storage from localStorage → OS keychain
  • Reason: OWASP Mobile Top 10 M2: Insecure Data Storage
  • Revert command: `git checkout v2.0.0 -- src/auth/token_manager.py`
```

**Why This Format Wins**: Top=current; includes revert cmd; machine-readable; incident-linked.
### Inter-Agent Communication Protocol

#### When to Communicate:
| Scenario | Action | Communication Method |
|----------|--------|----------------------|
| Need expertise outside domain | Request help via structured JSON | `{"request": "radix_ui_expert", "task": "custom_calendar_component", "constraints": ["accessibility:WCAG_2.1", "theme:dark_mode"]}` |
| Protocol conflict detected | Flag inconsistency to user | `{"alert": "protocol_conflict", "agent1": "frontend", "agent2": "backend", "issue": "date_format_mismatch"}` |
| Security boundary violation | Block action + notify security agent | `{"security_alert": "orm_direct_access", "source": "frontend_agent", "target": "database_layer"}` |

#### Communication Rules:
```python
# ✅ CORRECT: Structured JSON request
{
  "from_agent": "frontend_expert",
  "to_agent": "radix_ui_expert",
  "request_id": "req_20260203_001",
  "task": "build_accessible_modal",
  "requirements": {
    "wcag_level": "AA",
    "keyboard_nav": true,
    "theme_support": ["light", "dark"]
  }
}

# (avoid unstructured natural language)
```

### Universal Anti-Hallucination Enforcement Checklist

| Check # | Rule | Verification Command | Fail Action |
|---------|------|----------------------|-------------|
| AH-1 | No invented APIs | `grep -E "(QMagicButton|DependsAsync|MongoSQL)" output.py` | Reject output |
| AH-2 | Version compatibility verified | `pip show {package} \| grep "Version: {required}"` | Reject output |
| AH-3 | Security claims cited | `grep -E "(OWASP|CWE|NIST)" output.md \| wc -l` ≥ 1 | Reject output |
| AH-4 | Uncertainty acknowledged | If uncertain: output MUST contain "Verify in [official_source]" | Reject output |
| AH-5 | Type signatures validated | `mypy --strict output.py` exit code = 0 | Reject output |

> ⚠️ **Hallucination = Critical Failure**: Any output failing AH-1 through AH-5 **MUST BE REJECTED** — no exceptions.

### Modular Code Creation Protocol

#### Core Function Rules:
- Atomic functions only; one responsibility
- Avoid monolithic functions (split when “and” appears)

#### Composition Pattern:
- Level 1: formatDate, validateEmail, hashPassword
- Level 2: createUser = validateEmail + hashPassword + saveUser
- Level 3: onboardUser = createUser + sendWelcomeEmail + assignOnboardingTask

**Golden Rule**: 
> "If a function does >1 distinct thing (separated by 'and' in description), split it."

### Agent Naming Convention

| Requirement | Rule | Examples |
|-------------|------|----------|
| Length | ≤20 characters INCLUDING spaces | ✅ `frontend expert` (16 chars)<br/>❌ `nextjs_tailwind_radix_ui_specialist` (38 chars) |
| Clarity | Describes expertise domain ONLY | ✅ `database expert`<br/>❌ `super_db_wizard_2026` |
| Uniqueness | No overlap with other agents | ✅ `auth expert` + `payment expert`<br/>❌ `backend expert` (too broad — overlaps with auth/payment) |

**Valid Names**:
- frontend expert
- backend expert
- database expert
- auth expert
- ui components

### Protocol Update Workflow (MANDATORY)

1) Detect issue → 2) Decide critical → 3) Alert user → 4) If approved: update protocol + append versioning (Top=current) → 5) Tag commit → 6) Notify dependents

**Critical Rule**: 
> AI agent MUST NEVER auto-update protocols — user approval required for ALL changes.

### Complete Agent Workflow (Per Task)

1) Pre-check: `[ -d aidocs ] && [ -f aidocs/${AGENT}_expert_protocol.md ]`
2) Read protocol: allowed/forbidden/security
3) Run AH-1..AH-5
4) Check modularity (≤1 responsibility)
5) Boundary check (no cross-domain imports)
6) Output only if all pass
7) Conflict → halt + alert user

### Framework-Agnostic Examples

| Domain | Core Function (Atomic) | Composition (Reusable) |
|--------|------------------------|------------------------|
| **Frontend** | `formatCurrency(amount, currency)` | `displayOrderTotal()` = `formatCurrency(order.subtotal) + formatCurrency(order.tax)` |
| **Backend** | `hashPassword(plain)` | `registerUser()` = `validateEmail() + hashPassword() + saveUser()` |
| **Database** | `getById(id)` | `findActiveUsers()` = `getAll() + filterBy(status='active')` |

> **Universal Truth**: Atomic functions work identically whether using Next.js/React OR PySide6 — framework is irrelevant to modularity.

### Critical Enforcement Summary

| Rule | Enforcement Mechanism | Failure Consequence |
|------|------------------------|---------------------|
| Single aidocs folder | `find . -type d -name aidocs \| wc -l` = 1 | Task aborted |
| Protocol read before action | File timestamp < task start time | Output rejected |
| Anti-hallucination checks | AH-1 through AH-5 automated scan | Output rejected |
| Modularity (≤1 responsibility) | Cyclomatic complexity ≤5 + "and" scan | Function rejected |
| User approval for protocol changes | Git commit requires user-signed tag | Change blocked |

**Works for any stack**: Next.js/Tailwind/Radix UI, FastAPI/SQLAlchemy, PySide6, SvelteKit/Prisma, Flutter/Dart, others

> **Golden Rule**: "If it can't be verified against official documentation, it doesn't exist." — Hallucination prevention is non-negotiable.
