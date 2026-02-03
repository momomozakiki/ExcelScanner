## Universal AI Agent Protocol (Framework-Agnostic)
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
└── aidocs/                          # ONE AND ONLY ONE aidocs folder at project root
    ├── frontend_expert_protocol.md
    ├── frontend_expert_versioning.md
    ├── backend_expert_protocol.md
    ├── backend_expert_versioning.md
    ├── database_expert_protocol.md
    └── database_expert_versioning.md
```

**Critical Enforcement Rules**:
```bash
# BEFORE any action, AI agent MUST:
if [ ! -d "aidocs" ]; then
  echo "ERROR: aidocs folder missing at project root" >&2
  exit 1
fi

# Verify EXACTLY ONE aidocs folder exists:
if [ $(find . -type d -name "aidocs" | wc -l) -ne 1 ]; then
  echo "ERROR: Multiple aidocs folders detected — violates protocol" >&2
  exit 1
fi

# Read agent-specific protocol:
AGENT_PROTOCOL="aidocs/${AGENT_NAME}_expert_protocol.md"
if [ ! -f "$AGENT_PROTOCOL" ]; then
  echo "ERROR: Missing protocol file: $AGENT_PROTOCOL" >&2
  exit 1
fi
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

**Why This Format Wins**:
- Top = Current — find latest changes quickly
- Revert command included — easy rollback
- Machine-readable — `grep "^v" versioning.md \| head -1` finds current
- Incident-linked — changes tied to real events
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

# ❌ WRONG: Unstructured natural language
"Hey can you make a modal that's accessible?"
```

### Universal Anti-Hallucination Enforcement Checklist

**Every AI agent MUST pass these checks BEFORE output**:

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
```typescript
// ✅ CORRECT: Atomic core function (reusable)
function formatDate(date: Date, format: 'iso' | 'human'): string {
  // ONE responsibility: date formatting
}

// ❌ WRONG: Monolithic function (not reusable)
function processOrderAndNotifyUserAndLogAnalytics(order: Order) {
  // 3 responsibilities — violates modularity
}
```

#### Composition Pattern:
```
Level 1: Core Functions (atomic verbs)
  • formatDate()
  • validateEmail()
  • hashPassword()

Level 2: Domain Functions (compose Level 1)
  • createUser() = validateEmail() + hashPassword() + saveUser()

Level 3: Workflow Functions (compose Level 2)
  • onboardUser() = createUser() + sendWelcomeEmail() + assignOnboardingTask()
```

**Golden Rule**: 
> "If a function does >1 distinct thing (separated by 'and' in description), split it."

### Agent Naming Convention

| Requirement | Rule | Examples |
|-------------|------|----------|
| Length | ≤20 characters INCLUDING spaces | ✅ `frontend expert` (16 chars)<br/>❌ `nextjs_tailwind_radix_ui_specialist` (38 chars) |
| Clarity | Describes expertise domain ONLY | ✅ `database expert`<br/>❌ `super_db_wizard_2026` |
| Uniqueness | No overlap with other agents | ✅ `auth expert` + `payment expert`<br/>❌ `backend expert` (too broad — overlaps with auth/payment) |

**Valid Names**:
- `frontend expert` (16)
- `backend expert` (14)
- `database expert` (16)
- `auth expert` (11)
- `ui components` (13)

### Protocol Update Workflow (MANDATORY)

```mermaid
flowchart TD
    A[AI Agent detects protocol issue] --> B{Is change critical?}
    B -->|Yes| C[Alert user: “Protocol conflict detected”]
    B -->|No| D[Log issue for next review]
    C --> E[User approves change?]
    E -->|No| F[Continue with current protocol]
    E -->|Yes| G[Update protocol.md]
    G --> H[Append to versioning.md<br/>TOP = latest change]
    H --> I[Commit with tag: protocol/{agent}/vX.Y.Z]
    I --> J[Notify dependent agents]
```

**Critical Rule**: 
> AI agent MUST NEVER auto-update protocols — user approval required for ALL changes.

### Complete Agent Workflow (Per Task)

1. **Pre-Action Check**  
   ```bash
   [ -d "aidocs" ] && [ -f "aidocs/${AGENT}_expert_protocol.md" ]
   ```

2. **Read Protocol**  
   Parse `protocol.md` for:  
   - ✅ Allowed actions  
   - ❌ Forbidden actions  
   - 🔒 Security boundaries  

3. **Anti-Hallucination Scan**  
   Run AH-1 through AH-5 checks on proposed output  

4. **Modularity Check**  
   Verify function has ≤1 responsibility (no "and" in description)  

5. **Boundary Check**  
   Confirm no cross-expertise imports/calls  

6. **Output**  
   Only if ALL checks pass → deliver concise, minimal solution  

7. **Protocol Conflict?**  
   If detected → halt + alert user (never auto-fix)  

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

**This protocol works for ANY stack**: 
- Next.js/Tailwind/Radix UI 
- FastAPI/SQLAlchemy 
- PySide6 
- SvelteKit/Prisma 
- Flutter/Dart 
- ...or any future framework

> **Golden Rule**: "If it can't be verified against official documentation, it doesn't exist." — Hallucination prevention is non-negotiable.
