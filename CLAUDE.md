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

# Check whether the v2 suite already has something like this — live, mid-run, paginated
# automatically. Omit --section-ids to search the entire suite.
uv run .claude/scripts/fetch_testrail.py get-cases-for-sections 1 <v2_suite_id> --match "keyword"

# Create a section in the v2 suite
uv run .claude/scripts/fetch_testrail.py add-section 1 <v2_suite_id> "<name>" <parent_id>

# Batch create cases in a section
uv run .claude/scripts/fetch_testrail.py batch-add-cases <section_id> --json-file <path>

# Repo health check — run anytime, catches list-format drift, unpublished cases sitting in a
# cases-*.json file, duplicate ids, and (with --verify-routing) flagged cases that landed in the
# wrong section. Read-only, no TestRail creds needed unless --verify-routing is passed.
uv run .claude/scripts/fetch_testrail.py validate-cases-file --all
uv run .claude/scripts/fetch_testrail.py validate-cases-file --all --verify-routing --project-id 1 --suite-id <v2_suite_id>
```

`migrate-section.md` Step 5d also runs this automatically (with `--verify-routing`) right after
every publish — a non-zero exit there means stop and fix the file before reporting the migration
done, not report success anyway.

**Checking whether the v2 suite already covers something, mid-run:** use
`get-cases-for-sections <project_id> <v2_suite_id> --match "keyword"` (omit `--section-ids` to
search the whole suite) — it fetches live cases, paginates automatically, and filters by title
keyword. For a more rigorous check before publishing a batch of new cases, use `dedup-check`
(fuzzy-matches title + body against a section's existing live cases, flags anything at/above a
similarity threshold). Prefer either of these over scanning local `ai-context/cases-*.json` files
for this purpose — the local files are this project's own mirror and can go stale if TestRail was
ever edited directly or a file was never written back.

### testrail-search MCP
Hybrid semantic + keyword search over the indexed Suite 6 cases. Use it to find relevant
existing cases before writing new ones. Available as an MCP tool in this project.
`get_test_case(case_id)` fetches one Suite 6 case in full by numeric id — used by
`/audit-section` to compare a published case's wording against its actual source text.

---

## Migration workflow

1. **User invokes `/fetch-section <section-name>`** — style-rewrite draft, human-reviewed, sourced
   from Suite 6. **`/draft-section <section-name>`** is the parallel entry point for sections with
   no Suite 6 cases at all — live-crawls the actual QA2 page first for structural ground truth,
   then fills in with files from `internal-docs/`, flagging any mismatch between the two. Both
   write the same `ai-context/draft-<slug>.json` shape, so everything downstream is identical.
2. **User invokes `/grill-section <section-name>`** — verifies the draft against the live QA app
3. **User invokes `/migrate-section <section-name>`** — applies structural v2 rules, publishes
   to TestRail on explicit `publish`
4. **User invokes `/audit-section <section-name>`** (anytime after publish, or `all` for every
   published section) — retrospective check that no legally/functionally load-bearing text
   (consent/banner copy, warnings, transactional emails — see `migration-conventions.md` §4)
   got paraphrased away during the pipeline, plus a structural re-check via
   `validate-cases-file`. Run this periodically, not just once per section — it's the
   systematic version of the manual "v1 audit" that first caught this happening on
   Organisations & Sites.

**`/migration-status [section]`** — read-only progress dashboard across the whole tree (or one
top-level section): what's not started, drafted, published, or due for audit, plus open gap
counts from `coverage-gaps.md`. Run anytime; makes no edits. Useful before picking the next
section to work on, or to spot pipeline drift (e.g. a file stuck mid-merge, an inconsistent
timestamp field) that's invisible looking at one section at a time.

**`/wiki-sync [section]`** — keeps `docs/wiki/` (the LLM-readable app knowledge base) in sync with
what `/grill-section`/`/audit-section` have actually verified. Not a numbered pipeline step and
not scoped to the migration — it's a periodic health check meant to keep running long after
Suite 6 → v2 work is done, same standing as `/migration-status`. Natural times to run it: after
`/audit-section` finishes on a section (its `audit_note`/`audit_status` fields are one of its
main sources), or periodically across `all` sections to catch drift. Never writes to
`docs/wiki/*.md` without explicit approval.

Cases are never created without explicit user approval.

`coverage-gaps.md` tracks scenarios deliberately deferred during a `/grill-section` or
`/audit-section` pass (plan tier unavailable, destructive action, out of scope for that pass),
organized by v2 section — check it before starting work on a section to see what's already
known to be incomplete, and update it when a gap opens or closes.

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
- **automation_type** — not used in v2 (not a TestRail field). Do not set it. See `testrail-suite-v2.md` open issue M4
