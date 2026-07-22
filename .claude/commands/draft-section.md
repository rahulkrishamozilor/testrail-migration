You are preparing a draft of new v2 test cases for **$ARGUMENTS**, grounded first in a live crawl
of the actual page and then filled in with internal product documentation — not migrated from
Suite 6.

Use this command instead of `/fetch-section` when the section has **no existing Suite 6 cases** —
it appears under "Not yet documented" in `docs/wiki/README.md` or has no matching
`ai-context/cases-<slug>.json` yet. This is a separate, parallel entry point into the same
pipeline: once Suite 6 migration is complete project-wide, `/fetch-section` can be retired and this
becomes the standard way to add any new section from a spec doc.

This command also handles the **gap-closing re-run**: a section that already has a published
`ai-context/cases-<slug>.json` from a prior `/draft-section` pass, where you're now going back to
close a specific gap (e.g. one logged in `coverage-gaps.md` or that file's own
`out_of_scope_notes`). Step 0 below detects this case and scopes everything downstream to avoid
re-authoring what's already published.

This command does NOT create anything in TestRail. Its only output is a draft JSON file in
`ai-context/`, in the exact same shape `/fetch-section` produces — `/grill-section` and
`/migrate-section` consume it unchanged, with zero changes to either command or to
`fetch_testrail.py`. All structural decisions (section placement, final run_type, routing flagged
cases) are still deferred to `/migrate-section`, same as today.

**Why live crawl comes before docs:** internal docs describe intended behavior — a spec's field
list, character limits, plan gates. They do not reliably describe the *current* live page: button
labels, step order, whether a documented field has actually shipped, or whether the current
character limit matches the doc (the character-limit doc for the Privacy Policy Generator, for
example, explicitly flags several fields where the current implementation doesn't match its own
recommended value). Crawling first establishes what is actually true today, so the docs are used
to fill in and cross-check, not as an assumed ground truth to draft blindly against.

Before starting, read `migration-conventions.md` in full — especially §0 (the completeness
standard) and §4 (verbatim-text fidelity). Both matter more here than in `/fetch-section`: there is
no existing case to fall back on.

Follow these steps exactly:

---

## Step 0 — Check for cases already published

Compute the section slug using the same rule as Step 7 (strip leading numeric prefix `^\d+\.\s*`,
lowercase, spaces → hyphens). Check whether `ai-context/cases-<section-slug>.json` already exists.

- **Doesn't exist** — this is a from-scratch draft. Proceed to Step 1 as normal.
- **Exists** — this run is closing a gap in an already-published section, not starting fresh. Read
  the file in full before crawling anything:
  - Every existing case's title and steps are known-covered ground. Nothing in Steps 4–5 below
    should re-author a case for a scenario one of them already covers.
  - Its `out_of_scope_notes`, if present, is the authoritative gap list carried over from
    publishing — treat it as this run's starting scope, not the whole feature. Cross-check it
    against `coverage-gaps.md`'s entry for this section; if the two disagree, `coverage-gaps.md`
    wins, since that's the file every session is supposed to keep current on open/close.
  - Note the existing `section_id` — carry it forward into this run's output (Step 7) instead of
    leaving it `null`.
  - If the user invoked this command for a specific named gap, treat that as the scope for this
    run. If they invoked it plainly (just `$ARGUMENTS`), ask which open gap(s) from
    `out_of_scope_notes` / `coverage-gaps.md` to target before crawling — don't silently
    re-sweep the entire feature.

This changes what Steps 1–5 do: still crawl and author in full for the targeted gap(s), but check
every scenario against the existing cases before writing it up. An item already covered is
silently dropped from the scenario inventory (Step 4), not re-authored. Re-confirming that an
existing published case still matches current live behavior is `/audit-section`'s job, not this
command's.

---

## Step 1 — Live-crawl the page for structural context

### 1a. Load accounts and log in to QA2

Read `qa-accounts.json` from the project root — this is the source of truth for every account and
its credentials (`accounts.<key>.email` / `.password` / `.plan`, plus an optional per-account
`.env` override). Do not read `$QA2_TEST_EMAIL` / `$QA2_TEST_PASSWORD` from the environment; those
are not used by this command.

If `qa-accounts.json` is absent, stop and tell the user it's required — there is no environment
fallback.

Use the `free` account as the default starting account (lowest tier, so the most gates are visible
from it). Use the Playwright MCP browser tools to:
1. Navigate to the account's `.env` value if it has one; otherwise `$QA2_BASE_URL` (environment —
   only used for the base URL, never for credentials).
2. Log in with that account's `email` / `password` if redirected to a login page.
3. Confirm you land on the Dashboard (or equivalent). If login fails, stop and report — do not
   proceed with an unauthenticated session.

### 1b. Explore the live page

Navigate to the page(s) that make up $ARGUMENTS. This is an adversarial pass, not passive
observation — for every field and control, try to break it and record what actually happens,
not just what it's labeled as. Record, as ground truth:
- Every screen/step/tab the feature actually has, in the order a user encounters them
- Every field/control's actual label, type, and visible constraints (placeholder text, inline
  character counters, tooltips, help text)
- Every visible conditional show/hide behavior — toggle a checkbox or selector and note what
  appears/disappears
- Every visible plan-gating on the default account (locked icon, upgrade nudge, upgrade popup
  copy — capture the nudge headline/body/CTA verbatim via `browser_snapshot` or
  `browser_evaluate`, not by eye)
- Navigation controls (Next/Back/Save draft/Publish) — actually click each one and record the
  resulting state, not just what it appears to do
- **Boundary and invalid input for every field with a visible constraint** — actually submit
  empty, over-limit, duplicate, and malformed values (not just note that a constraint exists)
  and capture the real validation error copy verbatim via `browser_snapshot`/`browser_evaluate`.
  If a field shows no visible constraint, still submit one empty/malformed value to confirm
  whether it's actually required — do not assume from the label alone
- **Error and edge states** reachable without a destructive/irreversible action — duplicate
  entries, empty states, client-side validation, rate limits if triggerable safely

**Destructive or irreversible actions** (final delete, a generate/publish step that can't be
undone, cancelling a subscription) — do not perform these with the default `free` account or any
shared account. If `qa-accounts.json` has a disposable account intended to absorb this kind of
mutation (e.g. `disposableuser`), switch to it using the Step 1c session-clear pattern below and
exercise the action there. If no disposable account is available, do not guess at the outcome —
mark it `[verify against live app — destructive, no disposable account available]` and move on.

Take a screenshot or snapshot of each distinct screen, and of each validation error actually
triggered, for reference during Step 5.

### 1c. Explore plan-gated areas with higher-plan accounts

If `qa-accounts.json` has higher-tier accounts, switch to each (starting from the lowest paid tier
upward) using the same session-clear pattern `/grill-section` uses:

```js
async (page) => {
  await page.context().clearCookies();
  await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
}
```

Then navigate to that account's `.env` value if it has one, otherwise `$QA2_BASE_URL`, log in with
its `email`/`password` from `qa-accounts.json`, confirm Dashboard, and explore the same page again.
Note which fields/steps unlock, and capture any plan-tier-specific copy verbatim. Apply the same
adversarial probing from Step 1b at this tier too — a plan-gated field can carry its own character
limit or validation rule that differs from the default tier, and that only surfaces by actually
submitting boundary and invalid values here, not by assuming it matches the free-tier behavior.
Switch back to the default (`free`) account when done. Skip this sub-step if no higher-tier
accounts are available.

Steps 1b and 1c are now the adversarial pass, not just structural reconnaissance — boundary
values, invalid input, and every clickable control should be actually exercised here, not left for
later. What's still `/grill-section`'s job, run against the draft this command produces:
- Re-verifying everything above after time has passed — the live app can drift between this crawl
  and `/migrate-section`
- Destructive/irreversible actions this crawl deferred for lack of a disposable account
- Scenarios that only emerge from combining this section with another (feature interactions,
  cross-flow state)
- Anything left `[verify against live app]` below because this crawl couldn't reach it

---

## Step 2 — Locate and read the source docs

Look in `internal-docs/` (repo root) for files relevant to $ARGUMENTS. Match by filename keyword
first. If the section name doesn't obviously match any filename, list what's in the directory and
ask the user which file(s) apply — do not guess which doc covers a section.

Read every matching doc **in full** before continuing. For PDFs longer than ~20 pages, check the
page count first (`mdls -name kMDItemNumberOfPages <file>` works on macOS) and read in page-range
chunks, confirming every page is covered before moving to Step 3.

Record each file's path — this becomes `source_docs` in the draft metadata (Step 7).

---

## Step 3 — Reconcile the live crawl against the docs

Compare Step 1's observations with Step 2's docs directly, before writing any cases:

- **In the docs but not observed live** → the doc may describe a not-yet-shipped or since-removed
  state. Do not write a case for it as if it's current behavior — note it in
  `reconciliation_notes` (Step 7) as `doc-ahead-of-live`, and either skip it or mark any resulting
  case `[verify against live app]` with an explicit callout that it wasn't seen during the crawl.
- **Observed live but not in the docs** → the docs are incomplete for this. Live observation is the
  source of truth here; write the case from what was crawled, and note the gap as
  `live-ahead-of-docs`.
- **Both present but conflicting** (a character limit, a label, plan-tier assignment, wording) →
  live behavior wins for "what's true today." Write the case against live behavior, and note the
  conflict as `doc-live-mismatch` — this is exactly the kind of drift the character-limit-style
  audit docs are trying to catch, so it's worth surfacing back to whoever owns the doc, not just
  silently resolving it in the case.

Every entry needs a one-line reason, the same discipline `/fetch-section` applies to
`dropped_source_case_ids` — a reconciled discrepancy should stay distinguishable from one nobody
noticed.

---

## Step 4 — Build a scenario inventory

Merge Step 1's structural findings with Step 2's field-level logic, resolved per Step 3, into a
list of distinct testable units:

- Each screen/step in the flow, in the order confirmed live
- Each field, its type, and whether it's always shown or conditional
- Each plan-gating rule (confirmed live where possible, per the doc where not yet crawled)
- Each character/length limit (live value takes precedence per Step 3)
- Each piece of **verbatim output text** — generated content, labels, tooltips, error copy,
  upgrade-nudge copy — captured live where seen, from the doc otherwise
- Each validation/business rule implied by the doc

Group related fields into candidate cases by shared behavior pattern, not one case per field —
apply equivalence partitioning per `migration-conventions.md` (e.g. "text field appears when a
boolean is Yes, has a character limit" is one pattern, covering several fields in one case with the
field list noted).

**If Step 0 found an existing `cases-<slug>.json`,** check every item in this inventory against
its cases before it becomes a candidate: does an existing case's title/steps already cover this
scenario? If yes, drop it from the inventory — do not author a case for it — and record it in
`overlap_notes` (Step 7) with the existing case's id. Only scenarios with no existing match, or
that are the specific targeted gap from Step 0, move on to Step 5.

**Log explicit scope decisions.** If a doc covers ground deliberately out of scope for this pass
(e.g. a shared doc covers two features but $ARGUMENTS is only one), record it in
`out_of_scope_notes` (Step 7) with a one-line reason.

---

## Step 5 — Author v2-style cases

For each item in the scenario inventory, write a case directly in v2 style — there is no rewrite
step because there is no prior case wording to rewrite, only crawled behavior and doc spec to
translate into a case.

### Title
Same format as `/fetch-section`: `[Feature Area] Scenario being tested`. Feature area is the
section's app-facing name (e.g. `Privacy Policy Generator`), not the doc's internal terminology.

### Steps and expected results
- Every step and expected result must trace to something either observed live (Step 1) or stated
  in the docs (Step 2) — never invented.
- Prefer the live-observed wording for UI elements (button labels, field labels, navigation) since
  that's what a tester will actually see. Prefer the doc's wording for generated/output content
  (policy clauses, etc.) since that's typically longer than what's practical to transcribe from a
  screenshot — but if Step 1 already captured it verbatim via `browser_snapshot`/`browser_evaluate`,
  use the live-captured string, since it's closer to ground truth than the doc.
- Since Step 1b/1c now actually submits invalid/boundary input and clicks every control, this
  marker should be rare — reserved for what the adversarial crawl genuinely couldn't reach: a
  destructive action with no disposable account available, a plan tier not in
  `qa-accounts.json`, or a detail neither the crawl nor the docs pinned down. Where that applies,
  mark the expected result `[verify against live app]` — distinct from `/fetch-section`'s
  `[inferred]` marker, since this is a known gap rather than an inference from context.
  `/grill-section` treats both markers the same way: confirm or fix against the live app. If a
  draft ends up with many of these markers, that's a signal Step 1 was cut short, not that this
  marker is the normal path.
- Apply the verbatim-text fidelity check exactly as `/fetch-section` Step 3 does: any expected
  result asserting specific on-page text must quote the exact wording captured in Step 1 or Step 2,
  not a paraphrase.

### Plan gating
Set `plan_gate_flag: true` wherever Step 1c confirmed a plan-tier restriction live, or Step 2's
docs state one that Step 1 didn't contradict. `/migrate-section` still performs the actual routing
to `11. Billing & Upgrade > Plan Gates`.

### Preconditions
Same rule as `/fetch-section`: state only what's non-default (a specific plan tier, a prior step's
output, a conditional field's trigger having been set). If nothing non-default applies, `none`.

### Boundary / validation cases
Use the live-confirmed limit and error copy from Step 1b/1c's adversarial probing — the crawl
should have actually submitted over-limit, empty, and duplicate values and captured the real
validation response. Fall back to the doc's stated limit marked `[verify against live app]` only
where the crawl genuinely couldn't reach that field (e.g. it sits behind a plan tier with no
matching account). Cluster by field-behavior pattern per Step 4, not one case per field:
valid → over-limit → empty (if required).

---

## Step 5b — Enforce a logical case order

Identical rule to `/fetch-section` Step 3b: the draft array order is the published order
(`batch-add-cases` posts in array sequence). Cluster by sub-area in the order a user encounters it
(wizard/flow step order confirmed in Step 1), then within each cluster: render/display case first,
then happy-path, then input variants and validation (valid → duplicate → invalid → empty →
over-length), then cancel/dismiss, then destructive last. `permission_flag` cases go last overall.

---

## Step 6 — Present draft for review

Show every case. **Stop after presenting.** Do not write any files. Do not call any tools.

---
**Draft Case N: [Title]**
- **Preconditions:** [rewritten, or `none`]
- **Steps:**
  1. [step] → [expected result]
  2. [step] → [expected result]
- **Source:** live crawl / [doc filename] p.[page] / both
- **Authoring notes:** [any `[verify against live app]` marker used, any reconciliation note that
  produced this case, or `none`]
- **Flag:** `plan_gate_flag` / `permission_flag` / `platform_flag` / none

---

After all draft cases, show a **Reconciliation summary** listing every `doc-ahead-of-live`,
`live-ahead-of-docs`, and `doc-live-mismatch` entry from Step 3, then output this block exactly and
**stop**:

---
**Review the draft above.**

This draft combines a live crawl with internal docs — no TestRail changes have been made, and
items marked `[verify against live app]` have not been fully confirmed.

- Reply `skip N` to remove draft case N.
- Reply `edit N` followed by the corrected fields to update draft case N.
- Reply `save` to save the draft.
---

Wait for the user's reply. Process any `skip` or `edit` instructions, re-display the updated list,
and wait again. Do not proceed to Step 7 until the user explicitly replies `save`.

---

## Step 7 — Save draft on `save`

**Only reachable after the user replies `save`.**

Write `ai-context/draft-<section-slug>.json`, using the same canonical slug rule as
`/fetch-section` Step 5 (strip leading numeric prefix `^\d+\.\s*`, lowercase, spaces → hyphens).

**If a file already exists from a previous run:**

- **From-scratch mode** (Step 0 found no `cases-<slug>.json`) — replace it silently. This is a
  redo of the same not-yet-published draft; git history is the safety net.
- **Gap-closing mode** (Step 0 found a `cases-<slug>.json`) — do **not** replace it. An existing
  `draft-<slug>.json` here means an earlier gap-closing pass already left pending, unpublished
  cases in it for a *different* gap than the one just closed — exactly what happens if
  `/draft-section` gets run twice on the same section before either pass reaches
  `/migrate-section`. Overwriting would silently destroy that pending work. Instead, merge:
  1. Read the existing draft in full.
  2. Append this run's new cases to its `cases` array (don't touch the existing entries).
  3. Append this run's `out_of_scope_notes` / `reconciliation_notes` / `overlap_notes` onto the
     existing arrays — these are additive, not competing, same as `/migrate-section`'s Step 5c-ii
     merge.
  4. Update `fetched_at` to this run's timestamp and merge `source_docs` (union, no duplicates).
  5. Leave `section_id` and `existing_cases_file` as they already were.

  Show the user a one-line summary (N existing cases + M new cases merged) before moving on —
  this is still touching a file with pending work in it, so don't do it silently.

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
  "source_docs": ["internal-docs/<file>.pdf"],
  "existing_cases_file": "ai-context/cases-<slug>.json",
  "out_of_scope_notes": [
    { "topic": "...", "reason": "..." }
  ],
  "reconciliation_notes": [
    { "type": "doc-ahead-of-live", "detail": "..." },
    { "type": "live-ahead-of-docs", "detail": "..." },
    { "type": "doc-live-mismatch", "detail": "..." }
  ],
  "overlap_notes": [
    { "scenario": "...", "existing_case_id": 39441, "reason": "already covered, not re-authored" }
  ],
  "cases": [
    {
      "id": null,
      "title": "...",
      "preconditions": "...",
      "steps": [
        { "content": "...", "expected": "..." }
      ],
      "run_type": "regression",
      "source_case_ids": ["live crawl", "internal-docs/<file>.pdf p.2"],
      "permission_flag": false,
      "platform_flag": false,
      "plan_gate_flag": false,
      "rewrite_notes": "authored from live crawl + doc spec — no Suite 6 source"
    }
  ]
}
```

**Compatibility note — read before diverging from this shape:** `fetched_at` and `source_case_ids`
are reused field names, not renamed, so `/grill-section`, `/migrate-section`, and the
`batch-add-cases` / `validate-cases-file` scripts in `fetch_testrail.py` need zero changes to
consume this draft:

- `fetched_at` — here it marks when this draft was authored, combining the live crawl and the
  source docs. `/migrate-section` Step 2's staleness check ("draft older than two weeks, re-run
  fetch") still fires the same way — for this draft it should be read as "the live app or the
  source docs may have changed since this timestamp."
- `source_case_ids` — holds free-text provenance strings (`"live crawl"`, `"<file> p.<n>"`) instead
  of Suite 6 numeric case IDs. `fetch_testrail.py`'s `DRAFT_STRIP_FIELDS` strips this field
  unconditionally before POSTing to TestRail regardless of its contents, and no code path parses it
  as an integer — so this is safe. It is purely informational, and `/migrate-section` Step 4's
  "Source: ..." line will print these strings as-is.
- `permission_flag` / `platform_flag` / `plan_gate_flag` / `run_type` — identical meaning and
  values to `/fetch-section`'s output; `/migrate-section` Step 3b routes them the same way.
- `source_docs`, `out_of_scope_notes`, `reconciliation_notes` — new top-level fields, informational
  only, not read by any downstream script. Keep them in the file for human/audit traceability even
  though nothing enforces their presence.
- `existing_cases_file`, `overlap_notes` — new fields, only populated in gap-closing mode (Step 0
  found a `cases-<slug>.json`). Informational only, same as the fields above.
- `section_id` — in gap-closing mode, set this to the existing section's id noted in Step 0
  instead of `null`.

**Gap-closing mode — read before running `/migrate-section` on this output.** This draft contains
only the new gap-closing cases, not the full section. `/migrate-section` Step 5c publishes from
`draft-<slug>.json` and then renames it to `cases-<slug>.json` once every case has an id — if
`cases-<slug>.json` already exists, a plain rename would overwrite it and silently drop every
previously-published case's local record (the cases themselves stay in TestRail; only this
tracking file's history is at risk). Tell the user this explicitly before they run
`/migrate-section`, and confirm with them whether the two files should be merged by hand first —
do not let a rename clobber an existing `cases-<slug>.json` unattended.

After saving, tell the user:

> Draft saved to `ai-context/draft-<section-slug>.json` — N cases (M marked
> `[verify against live app]`), grounded in a live crawl and [doc list].
> Run `/grill-section $ARGUMENTS` next to close out anything still marked
> `[verify against live app]` before `/migrate-section`.

If in gap-closing mode, append:

> This is a gap-closing run against the existing `ai-context/cases-<section-slug>.json` (P
> cases already published) — K scenarios were skipped as already covered (see `overlap_notes`).
> Before running `/migrate-section`, note that its publish step renames `draft-<slug>.json` to
> `cases-<slug>.json`, which would overwrite the existing file rather than merge into it — flag
> this and agree on a merge approach first.

If this run merged into an already-existing `draft-<slug>.json` (Step 7's gap-closing-mode merge
rule), append instead of the plain "N cases" line above:

> `draft-<section-slug>.json` now holds Q cases total: R still pending from an earlier
> gap-closing pass, plus N new from this one. All Q are unpublished — running `/migrate-section`
> will publish everything in the file, not just this run's cases.
