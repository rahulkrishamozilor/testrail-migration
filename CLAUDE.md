# CookieYes TestRail Migration — v2

This project migrates the legacy CookieYes TestRail suite (Suite 6, ~12,000 cases) into the new
structured v2 suite. The v2 suite reduces duplication by eliminating plan-variant and role-variant
clones and replacing them with canonical cases and preconditions.

---

## Source of truth

`testrail-suite-v2.md` — read this first before any migration work. It defines the section
structure, naming conventions, run_type rules, plan-gated feature conventions, and placement
rules for every scenario type. Do not deviate from it.

---

## TestRail setup

| | Suite ID |
|---|---|
| Legacy suite (source) | 6 |
| New v2 suite (target) | **TBD — must be created in TestRail UI first, then update `.env` with `TESTRAIL_SUITE_ID_V2`** |

Project ID: 1 (CookieYes)

---

## Tools

### fetch_testrail.py
Thin CLI wrapper for the TestRail REST API. Run with `uv run`:

```bash
# Search sections in Suite 6
uv run .claude/scripts/fetch_testrail.py get-sections 1 6 --match "keyword" --compact

# Get all cases in a section
uv run .claude/scripts/fetch_testrail.py get-cases 1 6 --section-id <id>

# Get cases across multiple sections
uv run .claude/scripts/fetch_testrail.py get-cases-for-sections 1 6 --match "keyword"

# Create a section in the v2 suite
uv run .claude/scripts/fetch_testrail.py add-section 1 <v2_suite_id> "<name>" <parent_id>

# Batch create cases in a section
uv run .claude/scripts/fetch_testrail.py batch-add-cases <section_id> --json-file <path>
```

### testrail-search MCP
Hybrid semantic + keyword search over the indexed Suite 6 cases. Use it to find relevant
existing cases before writing new ones. Available as an MCP tool in this project.

---

## Migration workflow

1. **User invokes `/migrate-section <section-name>`**
2. Agent fetches Suite 6 cases for that section area
3. Agent applies v2 rules and proposes canonical cases
4. User reviews the proposed cases
5. User approves — agent creates cases in TestRail v2 suite

Cases are never created without explicit user approval.

---

## v2 transformation rules (summary)

Full rules are in `testrail-suite-v2.md`. Key points:

- **Remove role prefixes** — `[Account Owner]`, `[Admin]`, `[Editor]` do not appear in titles outside section 14
- **Collapse plan duplicates** — one canonical case, plan state in Preconditions
- **Equivalence partitioning** — write separate cases only when behavior genuinely differs between plans
- **Role divergence cases** — flag for section 14 (Permissions), do not create in feature sections
- **Nudge entry points** — feature section owns "nudge opens". Button destination owned by section 11
- **Plan Gates** — one case per plan in `11. Billing & Upgrade > Plan Gates`, tagged `smoke`
- **run_type default** — `regression`. Use `smoke` only for the single most critical happy-path check per feature area
- **automation_type** — set `Playwright` when the case is behavior-testable and automation will cover it
