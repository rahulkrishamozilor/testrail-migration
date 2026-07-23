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

## Step 2 — Inventory ai-context files, verified against live TestRail

TestRail is the source of truth for "does this case actually exist" — a file's own
`published_at`/`migrated_at` fields are only a claim about that, and this pipeline has already
shown they can drift (duplicate publishes, timestamp fabrication, files that predate the schema
entirely). So verify every run, not just when a file looks ambiguous:

```bash
uv run .claude/scripts/fetch_testrail.py validate-cases-file --all --verify-routing --project-id 1 --suite-id <v2_suite_id>
```

If `TESTRAIL_URL`/`TESTRAIL_USERNAME`/`TESTRAIL_API_KEY` aren't available in this environment, fall
back to `validate-cases-file --all` without `--verify-routing` (still catches missing/duplicate ids
purely locally) and say plainly in the report that live routing wasn't checked this run — don't
silently skip the distinction.

For each file, classify using the validator's output as authoritative over the envelope's own
timestamp claims, falling back to those claims only where the validator has nothing to say:

- **Any case reported with no `id`** (the `unpublished_id` error, or `legacy_list_format`'s
  "no id" case): **drafted**, regardless of what `published_at`/`migrated_at` say. If the file's
  own field claims otherwise, that disagreement is exactly the kind of drift this command exists
  to catch — call it out by name in Notes, don't quietly prefer one source. (This is the same check
  that reclassified `cases-plan-gates-new.json` from "unknown schema" to "drafted" on 2026-07-22.)
- **`legacy_list_format` with all cases carrying real ids**: published, but flag the legacy
  bare-list shape as a normalize-later note — same split `/audit-section` already makes.
- **`flag_routing_mismatch` / `flag_section_not_found`**: the case is still published, but
  misrouted — a data-integrity flag, not a status change.
- **No id-related errors, and `published_at` or `migrated_at` is truthy**: published (now
  TestRail-confirmed, not just locally claimed). Still call out any file using `migrated_at`
  instead of the documented `published_at` as a naming-drift note.
- **`draft-<slug>.json` with no matching `cases-<slug>.json`**: drafted, not yet migrated.
- **`draft-<slug>.json` AND `cases-<slug>.json` both present for the same slug**: a gap-closing
  publish that stopped short of `/migrate-section` Step 5c-ii's merge — flag this explicitly, it's
  a known transient state the workflow expects someone to finish, not a bug.
- Neither an id-bearing case nor `published_at`/`migrated_at` set: not started (or drafted, if a
  `draft-<slug>.json` exists for it).

For every dict-shaped file, also read `fetched_at`, `grilled_at`, and `audited_at`. Publish is the
terminal pipeline state — audit is a periodic, retrospective check layered on top of it, not a
stage the file is "stuck in." Note `audited_at` as a plain fact in the **Audited** column (its
date, or blank if not yet run); don't fold it into **Status**.

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

- **Status** is one of: `Not started`, `Drafted`, `Published`, `Gap-closing (needs merge)`,
  `Legacy (published)`, `Legacy (unpublished)`. `Published` is the terminal pipeline state — there
  is no separate "awaiting audit" status; audit recency is a fact in the **Audited** column, not a
  status value.
- **Cases** is the case count from the file, blank for `Not started`.
- **Audited** is a plain fact, not a pipeline stage: the `audited_at` date if set, or blank if not.
  A `Published` row with a blank **Audited** column is simply flagged as not yet audited — that's
  expected and unremarkable for freshly-published work, not a problem to call out in Notes.
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
