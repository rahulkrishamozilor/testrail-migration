# /grill-section

You are an adversarial QA agent. Your job is to verify a draft set of v2 test cases against the
live CookieYes QA2 environment using Playwright, then produce a hardened draft ready for
`/migrate-section`.

---

## Input

`$ARGUMENTS` — the section name to grill (same as you would pass to `/fetch-section` or
`/migrate-section`). Example: `Webapp (Free Signup) > Signup and Login`.

The draft cases are in `ai-context/draft-<slug>.json` where `<slug>` is a kebab-case version of
the section name. If no draft file exists, tell the user to run `/fetch-section` first.

---

## Workflow

### Step 1 — Load the draft

Read the draft JSON file from `ai-context/`. Present a summary: how many cases, which sections
they target, run_type breakdown.

Check each case for an existing `"grill_status"` field. If any are present, this is a resumed
run — report how many cases are already grilled vs. remaining. In Step 3, skip any case that
already has a `grill_status` set (do not re-execute it).

### Step 2 — Load accounts and log in to QA2

Handled by the `verify-case-live` skill's account/session management (invoked as part of Step 3
below) — it loads `qa-accounts.json`, tracks `current_account`, and performs the initial login on
its first call. Nothing to do manually here beyond noting the precondition: if `qa-accounts.json`
does not exist, the skill will report that and all plan-gated cases will be skipped.

### Step 3 — Verify cases (one by one)

Before starting, group the remaining cases (those without a `grill_status`) by their required
plan tier and sort groups so all cases needing the same account run together. This minimises
session switches (`verify-case-live` only switches accounts when the required tier actually
changes, but the call order is this command's decision, not the skill's).

For each case, in that order: invoke the `verify-case-live` skill with
`{ title: case.title, preconditions: case.customPreconds, customStepsSeparated: case.customStepsSeparated }`.
The skill handles plan detection, session switching, role verification, navigation, step
execution/comparison, and returns a verdict per step — see
`.claude/skills/verify-case-live/SKILL.md` for that mechanism in full (word-for-word extraction
discipline, the fix-text rule, skip-reason codes, etc.). This command owns only what comes next:
mapping the skill's verdict onto this draft file's bookkeeping.

**Map the skill's verdict to `grill_status` and record it immediately** — do not wait until
Step 6. For each case, update in place:

| Skill verdict | `grill_status` |
|---|---|
| `confirmed` (all steps) | `"confirmed"` |
| `mismatch` (any step) | `"fixed"` — apply the corrected `expected` text or step content the skill returned |
| `broken` (any step) | `"needs-manual-check"` |
| `needs-manual-check` | `"needs-manual-check"` |
| `skipped:<reason-code>` | `"skipped:<reason-code>"` |

- **Use the Edit tool to update the JSON file directly** — do not write batch scripts to a tmp
  file and run them. Edit the specific fields in place with exact string matching.
- Write changes to `ai-context/draft-<slug>.json` before moving to the next case.

This means the file always reflects the latest grilled state. If the run is interrupted, the
next invocation resumes from where it left off (Step 1 detects the existing `grill_status` fields).

A 🔍 **Gap found** — a scenario that exists in the app but no draft case covers — is not a
`verify-case-live` verdict; it comes out of this command's own exploration in Step 4 below.

### Step 4 — Hunt for missing scenarios

After verifying the existing cases, actively explore the feature area to find scenarios the draft
does not cover. This step is mandatory — do not skip it.

#### 4a. Explore the live UI

Navigate the relevant pages in QA2 and look for:
- UI states, flows, and branches not represented by any draft case
- Empty states (no data, first-time user, cleared history)
- Error and validation paths (invalid input, server errors, rate limits)
- Boundary conditions (max length, zero, one, many)
- Cancel / dismiss / back flows
- Success confirmation states and what happens on repeat action
- Feature interactions (e.g. toggling a setting while something else is active)

#### 4b. Reason over the draft systematically

For each draft case, ask: what is the complementary negative or edge-case path that is not
covered? Also ask: are there entry points, triggers, or precondition variants that lead to
different behaviour and are not yet captured?

#### 4c. Explore plan-gated areas with higher-plan accounts

After exploring the UI with the default account, switch to each higher-plan account available
in `qa-accounts.json` (starting from the lowest paid tier upward) and explore areas that are
only accessible on those plans. Look specifically for:

- Features, settings, or layout options that are locked or hidden on the default account
- UI states that only exist on paid plans (e.g. Popup layout, combined consent templates,
  advanced geo-targeting options)
- Upgrade nudges: verify the headline, body text, CTA label, and which plans are listed
- Behaviour differences between plan tiers (e.g. does the same feature work differently on
  Pro vs Ultimate?)

For each plan-gated gap found, write a suggested case spec with the required plan noted in
`preconditions`. Switch back to the default account when done.

If `qa-accounts.json` is absent or contains no higher-plan accounts, skip this sub-step.

#### 4d. Cross-check suggested cases against other published sections

Before writing any suggested case spec, check whether the scenario is already owned by
another v2 section — two passes, not just one:

1. **Local pass (fast, first).**
   ```bash
   ls ai-context/cases-*.json
   ```
   For each file that could plausibly overlap (e.g. a "Dashboard" case file if the suggested
   case involves Dashboard navigation), read its `cases` array and scan the titles.

2. **Live pass (authoritative).** The local files are this project's own mirror and can go
   stale (edited directly in TestRail, or never written back) — confirm against the live suite
   before trusting a "not found" from the local scan alone:
   ```bash
   uv run .claude/scripts/fetch_testrail.py get-cases-for-sections 1 <v2_suite_id> --match "keyword"
   ```
   Omit `--section-ids` to search the whole suite; use a keyword drawn from the suggested case's
   title or scenario. This fetches live and paginates automatically — see `CLAUDE.md`'s tool
   reference.

If either pass finds an existing case covering the scenario, **drop the suggestion** and note in
the report: `"[title] — already covered in cases-<slug>.json"` (local) or `"[title] — already
covered live, case <id> (not yet in local mirror)"` (live-only). Only proceed to write a
suggested spec if neither pass finds an existing case.

#### 4e. Produce missing-case specs

For each gap found (across all accounts explored) that is not already covered by another
section, write a full draft-ready case spec using the same JSON shape as the existing draft
cases. Assign `"grill_status": "suggested"`. Do not add a TestRail `id` — leave it absent
or `null`. Title must follow v2 naming conventions (no role prefixes, no plan prefixes).

---

### Step 5 — Report findings

After grilling all cases and hunting for gaps, **read the draft file** to tally verdicts —
do not rely on in-context memory for counts. Build the report from `grill_status` values
present in the file.

Produce a structured report:

```
## Grill report — <section name>

**Confirmed:** X cases
**Skipped (not automatable):** N cases
**Mismatches:** N cases
**Broken steps:** N cases
**Missing cases suggested:** N

### Skipped
- [title] — ⏭️ email-required: case expects a password reset email in inbox

### Mismatches
- Case: [title]
  Step N: expected "..." | actual "..."
  Fix: update expected to "..."

### Broken steps
- Case: [title]
  Step N: [description of what's wrong]

### Missing cases
- **[Suggested title]**
  Gap: [one sentence on why this scenario is uncovered]
  Preconditions: [starting state]
  Steps: [numbered steps]
  Expected: [expected result]
```

After the report, if any suggested cases were found, output this block exactly:

---
**N suggested cases have been added to the draft.**

When you run `/migrate-section $ARGUMENTS`, you will be shown each suggested case and asked
to approve or reject it before anything is created in TestRail.
---

---

### Step 6 — Finalise the draft

Individual case verdicts and fixes were already written incrementally during Step 3. This step
only needs to:

1. **Append suggested cases** from Step 4 (each with `"grill_status": "suggested"`, no TestRail
   `id`).
2. **Write the top-level `"grilled_at"` timestamp** using:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

3. Write the final JSON to `ai-context/draft-<slug>.json`. Do not create a new file.

After writing, confirm: `Draft updated in place — ai-context/draft-<slug>.json (N existing + N suggested cases).`

For reference, the full set of `grill_status` values used across the file:
- `"confirmed"` — verified against the live app, no changes needed
- `"fixed"` — expected result or step text was corrected based on live app behaviour
- `"needs-manual-check"` — broken step or unresolved issue, flagged for human review
- `"skipped:<reason-code>"` — could not be automated; case content is unchanged
- `"suggested"` — new case identified during gap-hunting; not yet in TestRail

---

## Rules

- Never skip a case silently — every case gets a `grill_status`, even if it is just `"confirmed"`.
- Navigation always goes in `customPreconds`, not step 1 — apply this correction to any case
  where step 1 is a navigation action.
- Session reuse, plan-gate skipping, and "don't modify on assumptions" are the `verify-case-live`
  skill's own rules (see its Rules section) — this command doesn't need to re-enforce them, only
  to act correctly on the verdicts it returns.
- A cross-cutting fix discovered mid-grill that affects an already-published section (not the
  one this run is grilling) gets edited directly into that section's `ai-context/cases-<slug>.json`
  — never create a new file (e.g. `draft-<slug>-fixes.json`). The target section's `cases-*.json`
  is the only source of truth for its cases; a side file has no downstream consumer and will sit
  unused once the fix is applied, so there is never a reason to create one.
