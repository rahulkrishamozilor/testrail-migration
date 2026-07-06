You are preparing a style-rewrite draft of Suite 6 test cases for **$ARGUMENTS**.

This command does NOT create anything in TestRail. Its only output is a draft JSON file in
`ai-context/` that `/migrate-section` will consume. All structural decisions (section
placement, plan collapsing, run_type, automation_type) are deferred to `/migrate-section`.

Before starting, read `migration-conventions.md` in full. It defines the title format, step
writing standard, what to drop, and the complete case example. Apply those conventions in
Step 3.

Follow these steps exactly:

---

## Step 1 — Fetch all Suite 6 cases

Cast a wide net — Suite 6 duplicates cases per plan variant and per role. You need all of
them to identify which cases are style duplicates vs. genuine behavioral variants.

```bash
uv run .claude/scripts/fetch_testrail.py get-sections 1 6 --match "<keyword>" --compact
uv run .claude/scripts/fetch_testrail.py get-cases-for-sections 1 6 --match-keywords "<keyword>" --max-cases 300
```

Check the `casesTruncated` flag in the response. If `true`, increase `--max-cases` and
re-fetch until the flag is `false`.

Record the Suite 6 section IDs returned by `get-sections` — these become `searched_section_ids`
in the draft metadata written in Step 5.

---

## Step 2 — Group by logical scenario

Group the fetched cases by their underlying scenario, ignoring role and plan prefixes.

- Cases that differ only in a role or plan prefix ([Account Owner], [Admin], [Webapp Free],
  [Agency], [Trial with card], etc.) **and** have identical step content and expected results
  → one group → one draft case. List all source case IDs.
- Cases that have different steps **or** different expected results → separate groups →
  separate draft cases. Note what the behavioral difference is.

Within each group, use the Account Owner / active paid plan case as the base text.

---

## Step 3 — Rewrite to v2 style

For each group, produce a rewritten case. Apply only style changes — do not make structural
decisions about section placement, run_type, or automation_type.

### Title

Remove all role and plan/platform prefixes, then reformat:

```
[Feature Area] Scenario being tested
```

- **Feature area**: the top-level feature (e.g. `Cookie Banner`, `Sign Up`, `Consent Log`)
- **Scenario**: concise present-tense description of what is verified

Examples:
- `[Account Owner][Webapp Free] Functionality of Publish Changes button with installation code`
  → `[Cookie Banner] Functionality of Publish Changes button with installation code`
- `[Admin][Agency] Verify user cannot access Billing page`
  → leave this one's title as-is but flag it with `permission_flag: true` (structural call
  for `/migrate-section`)

Prefixes to strip: `[Account Owner]`, `[Admin]`, `[Editor]`, `[Webapp Free]`, `[Agency]`,
`[Trial with card]`, `[Trial without card]`, `[Plugin]`, `[Shopify]`, `[Wix]`, and any
combination thereof.

### Steps

- Rewrite steps to test **behavior**, not UI copy or layout.
- Drop steps whose sole purpose is verifying static text, font size, alignment, or color.
- Each step: present-tense imperative for content ("Click X", "Enter Y"), present-tense
  assertion for expected ("Success message appears", "User is redirected to /dashboard").
- If a step's expected result is missing in the source, write one based on the obvious
  behavioral outcome. Mark it `[inferred]`.

### Preconditions

- Remove "Logged in as Account Owner" — that is the default assumption in v2.
- Keep only state that genuinely differs from the default (specific plan state, pre-created
  data, a prior step's output, etc.).
- If nothing non-default remains, set preconditions to `none`.

---

## Step 4 — Present draft for review

Show every draft case. **Stop after presenting.** Do not write any files. Do not call any tools.

For each case, show the rewritten version alongside a compact diff of what changed.

---
**Draft Case N: [Rewritten Title]**
- **Preconditions:** [rewritten, or `none`]
- **Steps:**
  1. [step] → [expected result]
  2. [step] → [expected result]
- **Source cases:** C##### [, C#####, …]  *(note if plan/role variants were collapsed)*
- **Rewrite notes:** [what changed — stripped prefixes, dropped layout steps, inferred
  expected results — or `none` if steps were unchanged]
- **Flag:** `permission_flag` / `platform_flag` / none  *(for /migrate-section to act on)*

---

After all draft cases, output this block exactly and then **stop**:

---
**Review the draft above.**

This is a style rewrite only — no TestRail changes have been made.

- Reply `skip N` to remove draft case N.
- Reply `edit N` followed by the corrected fields to update draft case N.
- Reply `save` to save the draft and prepare it for `/migrate-section $ARGUMENTS`.
---

Wait for the user's reply. Process any `skip` or `edit` instructions, re-display the updated
list, and wait again. Do not proceed to Step 5 until the user explicitly replies `save`.

---

## Step 5 — Save draft on `save`

**Only reachable after the user replies `save`.**

Overwrite `ai-context/draft-<section-slug>.json` with the final approved cases. If a file
already exists from a previous run, replace it silently — git history is the safety net.

If cases for this section already exist in the v2 suite, include their v2 case `id` in each
matching draft case object. During `/migrate-section`, publish with:

```bash
# New cases (id: null) — posts, writes IDs back, renames draft-* → cases-* when complete
uv run .claude/scripts/fetch_testrail.py batch-add-cases <section_id> \
  --json-file ai-context/draft-<slug>.json --from-draft --only-new --write-back

# Existing cases (id already set) — updates changed fields only
uv run .claude/scripts/fetch_testrail.py batch-update-cases \
  --json-file ai-context/cases-<slug>.json --from-draft
```

The draft file is the source of truth — do not create separate update/add payload files.

**Canonical slug rule** (migrate-section uses this same rule — defined here once):
1. Strip any leading numeric prefix: `^\d+\.\s*`  
   e.g. `"04. Cookie Banner"` → `"Cookie Banner"`, `"01. Authentication"` → `"Authentication"`
2. Lowercase
3. Replace spaces with hyphens

Examples: `"Cookie Banner"` → `cookie-banner`, `"04. Cookie Banner"` → `cookie-banner`,
`"01. Authentication"` → `authentication`

Write the approved cases to `ai-context/draft-<section-slug>.json`.

Before writing, get the current UTC timestamp:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

```json
{
  "section": "<$ARGUMENTS>",
  "suite_id": 16,
  "section_id": null,
  "fetched_at": "<UTC timestamp from above>",
  "grilled_at": null,
  "published_at": null,
  "searched_section_ids": [<Suite 6 section IDs recorded in Step 1>],
  "cases": [
    {
      "id": null,
      "title": "...",
      "preconditions": "...",
      "steps": [
        { "content": "...", "expected": "..." }
      ],
      "run_type": "regression",
      "source_case_ids": [12345, 12346],
      "permission_flag": false,
      "platform_flag": false,
      "rewrite_notes": "..."
    }
  ]
}
```

- `permission_flag: true` — case involves a role permission divergence; `/migrate-section`
  will route it to section 14.
- `platform_flag: true` — case is platform-specific (Plugin/Shopify/Wix); `/migrate-section`
  will route it to section 13.

After saving, tell the user:

> Draft saved to `ai-context/draft-<section-slug>.json` — N cases.
> Run `/migrate-section $ARGUMENTS` to apply structural v2 rules and publish to TestRail.
