You are migrating test cases from the legacy CookieYes TestRail Suite 6 into the new v2 suite.

Section to migrate: **$ARGUMENTS**

Follow these steps exactly:

---

## Step 1 — Read the source of truth

Read both reference documents in full:

- `testrail-suite-v2.md` — v2 section structure, placement rules, run_type and
  automation_type rules, plan-gated feature conventions
- `migration-conventions.md` — title format, step writing standard, what to drop,
  behavioural variant rules, and the complete case example

If no draft is loaded in Step 2, `migration-conventions.md` is the style guide for
inline rewriting in Step 3.

---

## Step 2 — Load source cases

Check whether a style-rewrite draft already exists for this section:

```
ai-context/draft-<section-slug>.json
```

(`<section-slug>` uses the same canonical rule defined in `/fetch-section` Step 5:
strip leading numeric prefix `^\d+\.\s*`, lowercase, spaces → hyphens.
e.g. `"Cookie Banner"` → `draft-cookie-banner.json`
     `"04. Cookie Banner"` → `draft-cookie-banner.json`
     `"01. Authentication"` → `draft-authentication.json`)

**If the draft file exists:** read it and use its `cases` array as the input to Step 3.
Skip the Suite 6 fetch — the draft is the agreed starting point. Note how many cases are
in the draft, acknowledge any `permission_flag` or `platform_flag` entries, and check the
`fetched_at` timestamp. If the draft is more than two weeks old, warn the user:
> ⚠️ Draft was fetched on `<fetched_at>`. Suite 6 may have changed since then. Consider
> re-running `/fetch-section $ARGUMENTS` to refresh it.

**If the draft has an `existing_cases_file` field** (set by `/draft-section` Step 0), this is a
gap-closing run against an already-published section — publishing in Step 5c will need the extra
merge in Step 5c-ii afterward, since `cases-<section-slug>.json` already exists.

### Step 2a — Review suggested cases (if any)

Before proceeding, check whether any cases in the draft have `"grill_status": "suggested"`.
These were identified during `/grill-section` as missing scenarios and have not yet been
approved for migration.

If suggested cases exist, list each one in this format and then **stop**:

---
**Suggested cases from grill — approve or reject each before migrating**

**S1: [Title]**
- **Gap:** [why this scenario was flagged as missing]
- **Preconditions:** [precondition text]
- **Steps:**
  1. [step] → [expected result]
- **run_type:** [value]

*(repeat for each suggested case)*

---
- Reply `approve N` to include case N in the migration.
- Reply `reject N` to drop case N from the draft.
- Reply `approve-all` to include all suggested cases.
- Reply `reject-all` to drop all suggested cases.
- Reply `done` when finished — migration will proceed with only approved cases.

Wait for the user's replies. Process each instruction and re-show the updated list after
each one. Do not proceed to Step 3 until the user replies `done`.

On `done`:
- Remove all remaining `"suggested"` cases (any not explicitly approved) from the working
  case list. Do not write them to TestRail.
- Approved cases have their `grill_status` treated as `"confirmed"` for the rest of the flow.

If no suggested cases exist in the draft, skip this step silently and continue to Step 3.

**If no draft exists:** stop and tell the user:

> No style-rewrite draft found for this section. Running `/fetch-section $ARGUMENTS` first
> is strongly recommended — it produces a human-reviewed, style-corrected input for this
> command and keeps style decisions and structural decisions in separate review gates.
>
> Reply `fetch-first` to stop here (then run `/fetch-section $ARGUMENTS`).
> Reply `skip-draft` to proceed without a draft. Style rewriting will be applied inline in
> Step 3 alongside structural decisions, with no separate human review gate for rewrites.

Wait for the reply. On `fetch-first`, stop immediately. On `skip-draft`, continue — apply
both the style rewriting rules from `/fetch-section` Step 3 AND the structural rules in
Step 3 below, combined in one pass.

---

## Step 3 — Fetch the live v2 section tree

Before assigning any placements, fetch the current section structure of the v2 suite so
cases are placed into sections that already exist wherever possible.

```bash
uv run .claude/scripts/fetch_testrail.py get-sections 1 <v2_suite_id> --compact
```

Build a map of every existing section: its full path (parent › child), its ID, and its
depth. Use this map in Step 3b to match proposed placements against reality.

---

## Step 3b — Apply v2 transformation rules

From the draft (or the raw Suite 6 cases if no draft), derive the canonical v2 case list.
These are **structural decisions** — style rewriting is assumed done if a draft was loaded.

1. **Assign section placement** — use the v2 section structure and the "Where specific
   scenario types live" table to determine the correct v2 path for each case. Then check
   each path against the live section map from Step 3:
   - If the section **exists** → record its ID. Mark the placement as `existing`.
   - If the section **does not exist** → mark it as `to be created`. Do not create it yet.
2. **Collapse plan duplicates** — if Free, Trial, Agency, Paid cases have identical steps
   and expected results, write one case. Note the required plan state in Preconditions only
   when behavior genuinely differs.
3. **Separate only on genuine behavioral difference** — different destination, different UI
   state, different outcome = separate cases.
4. **Route flagged cases** — identify the correct target section for each flag type, look
   up its ID in the live section map from Step 3, and stamp `section_id` on the case in the
   draft immediately. Do not include flagged cases in the main section's list.

   | Flag | Target section | Sub-section rule |
   |---|---|---|
   | `permission_flag: true` | `14. Permissions` | Inspect the case — if it tests an Editor restriction, use `14. Permissions > Editor`; if Admin, use `14. Permissions > Admin` |
   | `platform_flag: true` | `13. Platforms` | Create the section if it doesn't exist; use the appropriate platform sub-section |
   | `plan_gate_flag: true` | `11. Billing & Upgrade > Plan Gates` | Single flat section — use its ID directly |

   Stamping `section_id` in the draft is the enforcement mechanism. `batch-add-cases` routes
   each case by its own `section_id`, so flagged cases land in the right section automatically
   regardless of what the default section ID is. Do not rely on remembering to re-route at
   publish time — stamp it now.
5. **Set run_type** — `smoke` for the single most critical happy-path check per section
   (at most one), `regression` for cases that would affect a real user on a common path,
   leave empty for exhaustive edge cases and boundary conditions that rarely regress.

---

## Step 4 — Present proposed cases for review

Before listing cases, output a section map showing every unique target section and whether
it exists in v2 or needs to be created:

---
**Section map**
| Target section | Status |
|---|---|
| `01. Authentication > Sign Up` | ✅ exists (id: 123) |
| `01. Authentication > Forgot Password` | 🆕 will be created |

---

Then list every proposed v2 case in this format. Do not create anything in TestRail yet.

---
**Case 1: [Title]**
⚠️ **Contains inferred expected results — verify before publishing.** *(only when steps include `[inferred]`)*
- **Section:** [full v2 path] — ✅ exists / 🆕 will be created
- **Preconditions:** [exact precondition text, or `none`]
- **Steps:**
  1. [step] → [expected result]
  2. [step] → [expected result]
- **run_type:** [smoke / regression / *(empty)*]
- **Source:** C##### [, C#####, …]  *(informational — from draft `source_case_ids`; not written to TestRail)*

---

If any cases were flagged for section 14 (Permissions), list them separately at the end under
a `## Flagged for section 14 — Permissions` heading.

If any cases carry `platform_flag: true` from the draft, list them separately under a
`## Flagged for section 13 — Platforms` heading. Do not include them in the main case list.

If any cases carry `plan_gate_flag: true` from the draft, list them separately under a
`## Flagged for Plan Gates` heading. Do not include them in the main case list. Set their
`section_id` to the Plan Gates section ID and publish them in the same `batch-add-cases`
call — `batch-add-cases` routes each case by its own `section_id`, so they land in Plan
Gates while the rest land in the feature section.

After presenting all cases, output this block exactly and then **stop**. Do not proceed further.
Do not begin Step 5. Do not write any files. Do not call any tools.

---
**Review the cases above.**

- Reply `skip N` to drop case N from the list.
- Reply `edit N` followed by the corrected fields to update case N.
- Reply `publish` when the list is final and you want cases created in TestRail.

⚠️ Replying `publish` will write these cases to the live TestRail v2 suite. This cannot be undone from this workflow.
---

Wait for the user's reply. Process any `skip` or `edit` instructions — update the displayed
list and re-show it — then wait again. Do not proceed to Step 5 until the user explicitly
replies with the single word **`publish`** and nothing else qualifies as approval.

---

## Step 5 — Publish to TestRail

**Only reachable after the user has replied `publish`.**
If you are not certain the user said `publish`, ask before proceeding. Never infer approval.

### 5a — Check for existing v2 coverage


Before creating anything, check the v2 suite for cases that may already cover the same
scenarios (e.g. from a prior partial migration run). The v2 suite is a growing repo, so do
this **live and section-scoped** — not against a static index.

**First, reconcile the draft to your approved proposal.** The draft file is the single
source of truth — `batch-add-cases` posts it verbatim. So before anything else, edit the
draft file so every case exactly matches what you proposed and the user approved in Steps
3b/4. This includes:

- `section_id` — the resolved v2 target (an existing section's ID, or one you will create
  in 5b). Cases sharing the migration's most common section may omit it and fall back to the
  `<default_section_id>` positional.
- `run_type` — any promotion/demotion you decided (e.g. a case raised to `smoke`).
- `title`, `preconditions`, `steps` — any `edit N` corrections from Step 4.

Do not carry decisions only in your working context: if it isn't in the draft file, it won't
be published. This is what prevents field drift between the draft and TestRail.

Then run the read-only `dedup-check` helper, which fetches the live cases in each target
section and scores every proposed case against them:

```bash
uv run .claude/scripts/fetch_testrail.py dedup-check 1 <v2_suite_id> <default_section_id> \
  --json-file ai-context/draft-<section-slug>.json --threshold 0.5
```

It creates nothing. For each proposed case it reports the top matches (combined score =
0.6·title + 0.4·steps) in its target section. Interpret the results:

- **Score ≈ 1.0** — an exact/near-exact duplicate already exists. Do not create it; record
  the existing case ID against that draft case and skip it (leave its `id` set so
  `--only-new` skips it, or drop it from the publish set).
- **Score ~0.5–0.8** — a related but likely distinct case (often shared title stems, low
  `body_ratio`). Surface it to the user and let them decide before publishing.
- **No matches at/above threshold** — safe to create.

Do not rely on `testrail-search` here — that MCP indexes the legacy Suite 6 (the source),
not the v2 target.

### 5b — Create any missing sections

Using the section map built in Step 3, create only the sections marked `🆕 will be created`.
`add-section` requires a `parent_id` — walk up the path from the top-level section to
create each ancestor before its children. Re-use the IDs of existing sections recorded in
Step 3 as parent IDs where applicable.

### 5c — Publish cases from the draft

Each case's `section_id` was stamped in Step 5a (existing sections) — update any that pointed
at a section you just created in 5b. Then publish in a **single call**. `batch-add-cases` routes each case by its own
`section_id`; the positional `<default_section_id>` is the fallback for cases without one.
This handles multi-section migrations (e.g. feature cases + a Plan Gates case) in one pass —
no temp files, no manual ID merging. The `--from-draft` flag handles field translation
(`preconditions` → `custom_preconds`, `steps` → `custom_steps_separated`,
`run_type` string → integer) and strips internal-only fields (including the per-case
`section_id`, which is routing metadata and never sent in the body). `--only-new` skips any
case that already has an `id` (safe to re-run). `--write-back` patches the returned IDs back
into the draft and renames `draft-<slug>.json` → `cases-<slug>.json` once every case has an ID.

**Verify with a dry run first.** Confirm the on-disk draft matches your intended cases —
`--dry-run` posts nothing and prints the exact payloads + resolved target section per case:

```bash
uv run .claude/scripts/fetch_testrail.py batch-add-cases <default_section_id> \
  --json-file ai-context/draft-<section-slug>.json --from-draft --only-new --dry-run
```

Check the `run_type` integers (`smoke`→2, `regression`→1), target `section_id`s, and step
content match your proposal. The dry run also prints a `Flag-routed cases` summary — if it
warns that any flagged case (`permission_flag`/`platform_flag`/`plan_gate_flag`) has no
per-case `section_id`, that case would silently fall back to `<default_section_id>` instead of
its flag's target section. Treat that warning as blocking: fix the case's `section_id` in the
draft and re-run the dry run until the summary shows all flagged cases resolved to a
non-default section. If anything else is off, fix the draft (not just your context) and re-run
the dry run. Then publish for real:

```bash
uv run .claude/scripts/fetch_testrail.py batch-add-cases <default_section_id> \
  --json-file ai-context/draft-<section-slug>.json \
  --from-draft --only-new --write-back
```

The summary prints a per-section breakdown when cases land in more than one section.

### 5c-ii — Merge a gap-closing publish into the existing cases file

**Applies only when the draft had an `existing_cases_file` field (Step 2).** After 5c's
`--write-back` patches real ids into `draft-<section-slug>.json`, that file will **not** be
renamed to `cases-<section-slug>.json` — `fetch_testrail.py` only renames when that target
doesn't already exist, and here it does. Left alone, this leaves two files describing the same
section: the original `cases-<section-slug>.json` missing the cases you just published, and an
orphaned `draft-<section-slug>.json` holding only them. That breaks the single-source-of-truth
convention every other command (`/audit-section`, `validate-cases-file`, and any future
gap-closing `/draft-section` run) relies on.

Merge them explicitly, right after 5c, by hand — this touches the published source of truth, so
do not script it silently:

1. Read both files in full.
2. Append the newly-published cases (now carrying real ids, from `draft-<section-slug>.json`'s
   `cases` array) to the end of `cases-<section-slug>.json`'s `cases` array.
3. For each gap this run closed, find its entry in `cases-<section-slug>.json`'s
   `out_of_scope_notes` and edit its `reason` in place to prefix
   `RESOLVED <today's date> — <one-line summary + new case ids>` — matching the convention
   already used in that file (see e.g. the "Final 'Generate privacy policy' action" entry in
   `cases-privacy-policy-generator.json`). Don't delete the entry; a resolved note is still
   useful history.
4. Append the new draft's `reconciliation_notes` (if any) onto `cases-<section-slug>.json`'s
   array — these are additive, not competing.
5. Set `cases-<section-slug>.json`'s `published_at` to the new draft's `published_at`.
6. Delete `draft-<section-slug>.json` — its content now lives entirely inside
   `cases-<section-slug>.json`, and keeping both around violates the single-source-of-truth
   convention. Git history is the safety net.
7. Update `coverage-gaps.md`: mark the closed gap's line with `~~strikethrough~~` and the
   date/case IDs, per that file's own instructions — don't leave the resolution only in the JSON.

Show the user a summary (cases appended, gap(s) marked resolved, file deleted) before moving to
Step 5d.

### 5d — Validate the published file

**Mandatory — run this before declaring the migration done.** `--write-back` renames
`draft-<section-slug>.json` → `cases-<section-slug>.json` once every case has an id, but nothing
up to this point verifies that rename was actually earned, or that flagged cases (permission /
platform / plan gate) landed in the section their flag says they should. Don't rely on
remembering to check this — run the validator:

```bash
uv run .claude/scripts/fetch_testrail.py validate-cases-file \
  ai-context/cases-<section-slug>.json --verify-routing --project-id 1 --suite-id <v2_suite_id>
```

(If the rename condition wasn't met — e.g. some cases were intentionally left unpublished — point
this at `ai-context/draft-<section-slug>.json` instead.)

It checks, read-only: every case in the file has a real id; no id is reused; and every
`permission_flag` / `platform_flag` / `plan_gate_flag` case has a `section_id` that resolves
live to a section whose path actually contains "Permissions" / "Platforms" / "Plan Gates" —
catching a flagged case that silently fell back to the default section instead of being routed.

If it exits non-zero, **stop and fix the file before reporting the migration as complete** —
do not report success with unresolved validator errors. Fixing means either publishing the
missing case(s) to their correct section or correcting `section_id` and re-running
`batch-update-cases`, not editing the file to make the check pass.

After validation is clean, report every created case ID and the section each landed in.

### 5e — Keep the ai-context manifest in sync

`ai-context/manifest.json` lists every `cases-*.json`/`draft-*.json` filename in `ai-context/` —
it exists because the daily `migration-status` dashboard routine fetches file content over
`raw.githubusercontent.com` (the only host its sandbox's network policy allows) and has no way
to list a directory otherwise. If this step 5c renamed `draft-<slug>.json` →
`cases-<slug>.json`, or 5c-ii deleted a `draft-<slug>.json`, update
`ai-context/manifest.json`'s `files` array to match reality (add the new `cases-<slug>.json`
name, remove the deleted `draft-<slug>.json` name) and include it in the same commit. Skip this
step only if no filename in `ai-context/` actually changed this run.

Never create cases without explicit approval.
