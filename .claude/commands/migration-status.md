# /migration-status

You are producing a **read-only progress dashboard** for the Suite 6 → v2 migration: which
sections of the canonical `testrail-suite-v2.md` tree have been fetched/drafted, migrated
(published), and audited, which have open coverage gaps, and which haven't been started at all.

This command makes **no edits** to any file — not `ai-context/*.json`, not `coverage-gaps.md`,
nothing. It only reads and reports. If something looks wrong while you're building the report
(a stale timestamp, a file that should be renamed, an open gap that's actually closed), tell the
user in the output — do not fix it inline. Fixing belongs to `/migrate-section`, `/audit-section`,
or a manual edit the user explicitly asks for.

---

## Input

`$ARGUMENTS` — optional. Blank or `all` reports on the entire tree. A top-level section number or
name (e.g. `09`, `"09. Legal Policies"`, `"Cookie Banner"`) scopes the report to that section and
its descendants. Unrecognized input: report on everything and note that the filter didn't match
anything, rather than erroring out.

---

## Step 1 — Parse the canonical section tree

Read the fenced tree diagram in `testrail-suite-v2.md` under `## Section structure` (the
`CookieYes Functional Test Suite v2` block). Build a flat list of every **leaf** node — a node
with no further indentation beneath it — keeping its full ancestor path and top-level number,
e.g.:

```
01. Authentication > Sign Up > Core
01. Authentication > Sign Up > Standard (Free)
04. Cookie Banner > Customization Sidebar > Content > GDPR
04. Cookie Banner > Customization Sidebar > Content > US State Laws
09. Legal Policies > Privacy Policy Generator > Company Details > Business Details
```

`06. Consent Log`, `07. Languages`, `08. Advanced Settings`, and `16. Miscellaneous` are leaves
themselves (per the doc's "intentionally flat sections" note) — don't expect children for them.

If `$ARGUMENTS` scopes to one top-level section, keep only leaves under it for the rest of this
command, but still run Step 2's file inventory globally (a file can be misfiled under the wrong
number, which you can only catch by looking at everything).

## Step 2 — Inventory ai-context files

```bash
ls ai-context/cases-*.json ai-context/draft-*.json 2>/dev/null
```

For each file, read its JSON and classify:

- **Bare list** (top-level JSON is an array, not `{section, cases: [...]}`): this predates the
  draft/cases schema. Don't assume unpublished — check whether the cases inside carry real
  (non-null) `id` fields. If TestRail credentials and a suite id are available, confirm with:
  ```bash
  uv run .claude/scripts/fetch_testrail.py validate-cases-file ai-context/<file> --verify-routing --project-id 1 --suite-id <v2_suite_id>
  ```
  Classify as **"legacy schema, published"** (real ids, routing verifies) or **"legacy schema,
  unpublished"** (null ids or routing fails) — this is the same split `/audit-section` already
  makes; reuse it rather than inventing a third category.
- **`draft-<slug>.json` with no matching `cases-<slug>.json`**: drafted, not yet migrated.
- **`draft-<slug>.json` AND `cases-<slug>.json` both present for the same slug**: a gap-closing
  publish that stopped short of `/migrate-section` Step 5c-ii's merge — flag this explicitly, it's
  a known transient state the workflow expects someone to finish, not a bug.
- **`cases-<slug>.json` only, dict-shaped**: published. Read `published_at` for the publish
  timestamp — **but also check `migrated_at`**, since at least one prior session used that
  undocumented field name instead (`cookie-banner-layout`, `general`, as of the last check).
  Treat either field as evidence of publish, and call out any file using `migrated_at` as a
  naming-drift note in your output rather than silently normalizing it — that's a real
  inconsistency against what `fetch-section.md`/`migrate-section.md` document, worth a human
  eventually reconciling.
- For every dict-shaped file, also read `fetched_at`, `grilled_at`, and `audited_at`. A published
  file with an empty `audited_at` is due for `/audit-section`.

## Step 3 — Match files to tree leaves

Match is inherently fuzzy — one file sometimes covers multiple tree leaves (e.g.
`cases-cookie-banner-content.json` covers both the GDPR and US State Laws leaves), and slugs are
derived from the section name, not the full ancestor path. For each file, match on its own
`section` field text and filename slug against the leaf list from Step 1. **Print the file's raw
`section` field next to your match** so the user can eyeball a bad match instead of trusting a
silent guess.

Any leaf from Step 1 with no matching file at all → **not started**.

## Step 4 — Pull open gap counts

Read `coverage-gaps.md`. Its `## ` headings already use the exact tree-path format (e.g.
`## 09. Legal Policies > Privacy Policy Generator`). For each heading, count bullet items that
are **not** struck through with `~~...~~` (those are closed, keep them out of the open count) —
this is the section's open-gap count. Sections with no heading in this file have zero tracked
gaps (not the same as zero real gaps — just none flagged yet).

## Step 5 — Report

Emit one table, grouped by top-level section number, in ascending order:

| Section | Status | Cases | Fetched | Grilled | Published | Audited | Open Gaps | Notes |
|---|---|---|---|---|---|---|---|---|

- **Status** is one of: `Not started`, `Drafted`, `Gap-closing (needs merge)`, `Legacy (published)`,
  `Legacy (unpublished)`, `Published`, `Published — audit due`.
- **Cases** is the case count from the file, blank for `Not started`.
- **Notes** carries anything from Steps 2–3 worth a human's attention: field-name drift, a fuzzy
  match worth double-checking, a bare list, a stale draft/cases pair.

After the table, add a short **Data-integrity notes** section (only if non-empty — don't pad it)
listing anything found during Step 2 that's a pipeline inconsistency rather than a migration-
progress fact: `migrated_at` vs `published_at` drift, gap-closing pairs awaiting merge, legacy
bare-list files, section-field mismatches. These are exactly the kind of thing that's invisible
looking at one file at a time and only shows up when scanning all of them at once — the entire
reason this command exists — so don't bury them at the bottom in passing; call them out clearly.

Do not propose or make fixes in this command. If the user wants to act on a finding (run an
audit, finish a merge, reconcile a field name), point them at the right command
(`/audit-section`, `/migrate-section`) and stop there.
