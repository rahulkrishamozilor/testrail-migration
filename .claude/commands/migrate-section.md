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
4. **Route flagged cases** — cases with `permission_flag: true` go to section 14
   (Permissions); cases with `platform_flag: true` go to section 13 (Platforms). Do not
   include them in the current section's list.
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

Before creating anything, search the v2 suite for cases that may already cover the same
scenarios (e.g. from a prior partial migration run). Use the testrail-search MCP
(`search_test_cases`) scoped to the target v2 section path, and for any case with a
high-similarity hit, surface it to the user rather than creating a duplicate. Skip creation
for any approved case that already has equivalent coverage in v2.

### 5b — Create any missing sections

Using the section map built in Step 3, create only the sections marked `🆕 will be created`.
`add-section` requires a `parent_id` — walk up the path from the top-level section to
create each ancestor before its children. Re-use the IDs of existing sections recorded in
Step 3 as parent IDs where applicable.

### 5c — Write the JSON payload file

Write the case payloads to `ai-context/cases-<section-slug>.json` (the file must be inside
`ai-context/` — paths outside it are rejected by `batch-add-cases`).

Each element in the array must use these exact field names:

```json
[
  {
    "title": "...",
    "customPreconds": "...",
    "customStepsSeparated": [
      { "content": "step text", "expected": "expected result" }
    ],
    "custom_run_type": <run_type_id>
  }
]
```

- `customPreconds` maps to `custom_preconds` (the TestRail preconditions field).
- `customStepsSeparated` maps to `custom_steps_separated` (step-by-step format).
- `custom_run_type` is the numeric ID for the run_type custom field.
  Run `uv run .claude/scripts/fetch_testrail.py get-case-fields` to look up the field ID and
  its allowed values before writing the payload if they are not already known.
- Do not include `custom_automation_type` or `refs` — these fields do not exist in the v2 suite.

### 5d — Create the cases

```bash
uv run .claude/scripts/fetch_testrail.py batch-add-cases <section_id> --json-file ai-context/cases-<section-slug>.json
```

Report the created case IDs from the response.

Never create cases without explicit approval.
