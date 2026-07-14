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

#### 2a. Load the account pool

Read `qa-accounts.json` from the project root (if it exists). Build an account map keyed by
plan tier (e.g. `free`, `basic`, `pro`, `ultimate`). If the file does not exist, all
plan-gated cases will be skipped as before — continue without an account pool.

Track a `current_account` variable throughout the session. It starts as the default
`QA2_TEST_EMAIL` / `QA2_TEST_PASSWORD` account from the environment.

#### 2b. Log in

Use the Playwright MCP browser tools to:

1. Navigate to `$QA2_BASE_URL` (read from environment — do not hard-code a URL).
2. If redirected to a login page, fill in `$QA2_TEST_EMAIL` and `$QA2_TEST_PASSWORD` and submit.
3. Confirm you land on the Dashboard (or equivalent post-login page).
4. Take a screenshot and report the logged-in state and current plan tier.

If login fails, stop and report — do not proceed with an unauthenticated session.

### Step 3 — Verify cases (one by one)

Before starting, group the remaining cases (those without a `grill_status`) by their required
plan tier and sort groups so all cases needing the same account run together. This minimises
session switches.

**Plan detection** — infer required tier from the case's `preconditions` text:

| Signal in preconditions | Required account key |
|---|---|
| "Pro plan", "Pro or higher", "paid plan (Pro or higher)" | `pro` |
| "Ultimate plan" | `ultimate` |
| "free plan", "Free account" | `free` |
| "paid plan" (generic, no tier named) | lowest paid tier available in qa-accounts.json |
| No plan mention | current default account |

**Session switching** — before executing each case:
1. Detect the required plan tier.
2. If it matches `current_account` → proceed.
3. If it differs and the tier exists in `qa-accounts.json` → switch session using
   `browser_run_code_unsafe`:
   ```js
   async (page) => {
     await page.context().clearCookies();
     await page.evaluate(() => {
       localStorage.clear();
       sessionStorage.clear();
     });
   }
   ```
   Then navigate to `$QA2_BASE_URL`, log in with the matching account's credentials,
   confirm Dashboard, update `current_account`.
4. If it differs and no matching account exists in `qa-accounts.json` → skip with
   `skipped:plan-gated`.

**Role verification** — before executing any case whose correctness depends on a specific role
(a `permission_flag` case, or any case whose preconditions name a role such as Admin/Editor):
verify the acting account's actual `role_slug` via the Team page or `GET /api/v2/user`
(`organization_users[].role_slug`) before relying on it — do not assume the role recorded in
`qa-accounts.json` still holds. Ownership-transfer round-trips silently change roles: CookieYes
retains the previous owner at Admin access after a transfer, so an account used as an
ownership-transfer recipient earlier in this same grill run (or a prior one) may no longer be
the role it started as. If the role doesn't match what the case requires, correct it (Team page
> ⋯ > Change role) before proceeding — do not record a verdict against a role-tainted account.

#### 3a. Navigate to the starting state

Use the case's `customPreconds` to reach the correct starting page/state. If the precondition
says "User is on the Sign Up page", navigate there directly. Note any navigation issues.

#### 3b. Execute the steps

Walk through each step in `customStepsSeparated`:
- Perform the action described in `content`.
- Observe what the app actually does.
- Compare against the `expected` result.

**Always drive inputs the way a real user would, and always trigger the real submit action —
never infer a verdict from DOM state alone.** Use Playwright's actual typing/`.fill()` methods,
not `dispatchEvent` or direct `.value` assignment: those bypass the framework's input handlers
and can silently fail to trigger validation. For any step whose expected result is a validation
message or a submit-triggered outcome, actually click the real submit control (Save, Publish,
etc.) before recording the verdict — many validation messages only render on submit, not on
type/blur, so a verdict recorded without clicking submit is not evidence of anything. If a step
produces no visible effect, treat that as inconclusive and re-check your input method before
recording a gap or a mismatch.

#### 3c. Record the verdict and write it immediately

| Finding type | Meaning |
|---|---|
| ✅ Confirmed | Steps and expected result match the live app exactly |
| ⚠️ Mismatch | Expected result is wrong (different error message, different redirect, etc.) |
| ❌ Step broken | A step cannot be performed (UI element missing, page doesn't exist, etc.) |
| ⏭️ Skipped | Case cannot be automated — see skip reasons below. Left untouched in the output. |
| 🔍 Gap found | A scenario exists in the app that no draft case covers — captured in Step 4 |

**Word-for-word means word-for-word.** "✅ Confirmed" already requires the expected result to
match the live app exactly — for any expected result that quotes specific text as appearing on
the page (per `migration-conventions.md` §4, "Quoted on-page text — always verbatim"), "exactly"
means character-for-character, not "captures the same idea." No category filter: this applies
whether the quote is a legal disclosure or a plain status badge — if the draft quotes it, it must
be right. If the draft's quote is close but reworded compared to what the live app (or a
received email) actually shows, that is a `⚠️ Mismatch`, not a pass — record the exact live
wording as the fix, the same as any other mismatch.

**Verify this by extraction, not by eye.** Do not judge a quoted-text match from a screenshot or
an accessibility-tree summary glanced over — both are easy to skim past a wrong word, a dropped
sentence, or a swapped label. For every step whose expected result quotes on-page text (a button
label, tooltip, dialog/banner copy, validation message, confirmation toast — anything the case
presents as literal copy), pull the actual rendered string for that specific element with
`browser_snapshot` or `browser_evaluate` (reading `textContent`/`innerText` on the element, not
a full-page dump), then compare that extracted string against the draft's quoted text
character-by-character — punctuation, capitalization, and whitespace included. Only record
✅ Confirmed once that literal comparison passes; a single-character difference is a ⚠️ Mismatch,
recorded with both strings shown side by side (`expected: "..."` / `actual: "..."`) and the
extracted live text used as the fix. This is what would have caught, at grill-time rather than
in a later retrospective audit, a case claiming a "Copy code" button in the "top-right corner"
when the live button is actually labeled "Copy" and left-aligned, or a banner alert paraphrased
away from its real wording.

**Skip reasons — automatically skip and record reason, do not attempt to execute:**

| Reason code | When to apply |
|---|---|
| `email-required` | Case expects receiving an actual email (verification link, reset email, notification) |
| `time-dependent` | Case requires waiting (expired token after 1 hour, trial day X, "more than N hours after") |
| `destructive-precondition` | Precondition requires a destructive account state (deleted account, cancelled subscription) |
| `plan-gated` | Required plan tier is not available in `qa-accounts.json` (no matching account to switch to) |
| `external-url` | Step navigates to a third-party URL outside the app (T&C, Privacy Policy, marketing site) |
| `manual-only` | Case explicitly marked for manual verification (e.g. contains "[verify manually]" in steps) |

When a case is skipped, record: `⏭️ Skipped (reason-code) — [one-line explanation]`. Do not mark it as failing.

**After recording each verdict, immediately write the result back to the draft file.** Do not
wait until Step 6. For each case, update in place:

- Set `"grill_status"` to the appropriate value (`"confirmed"`, `"fixed"`,
  `"needs-manual-check"`, or `"skipped:<reason-code>"`).
- If the verdict is `"fixed"`, also apply the corrected `expected` text or step content now.
- **Use the Edit tool to update the JSON file directly** — do not write batch scripts to a tmp
  file and run them. Edit the specific fields in place with exact string matching.
- Write changes to `ai-context/draft-<slug>.json` before moving to the next case.

This means the file always reflects the latest grilled state. If the run is interrupted, the
next invocation resumes from where it left off (Step 1 detects the existing `grill_status` fields).

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
another v2 section. Read the list of existing `ai-context/cases-*.json` files, then for
each suggested case ask: does any case in those files already cover this scenario?

```bash
ls ai-context/cases-*.json
```

For each file that could plausibly overlap (e.g. a "Dashboard" case file if the suggested
case involves Dashboard navigation), read its `cases` array and scan the titles. If an
existing case already covers the scenario, **drop the suggestion** and note in the report:
"[title] — already covered in `cases-<slug>.json`."

Only proceed to write a suggested spec if no existing case owns the scenario.

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

- Never skip a case silently — every case gets a verdict, even if it is just ✅ Confirmed.
- Do not modify steps based on assumptions — only update `expected` values where the live app
  directly contradicts the draft. Flag everything else for human review.
- If the QA2 environment is behind a paywall gate for a specific plan, note it and skip only
  that case (not the whole section).
- Navigation always goes in `customPreconds`, not step 1 — apply this correction to any case
  where step 1 is a navigation action.
- Reuse the same browser session for all cases on the same account. Only switch sessions when the required plan tier changes. Track `current_account` so you never log out and back in unnecessarily.
- A cross-cutting fix discovered mid-grill that affects an already-published section (not the
  one this run is grilling) gets edited directly into that section's `ai-context/cases-<slug>.json`
  — never create a new file (e.g. `draft-<slug>-fixes.json`). The target section's `cases-*.json`
  is the only source of truth for its cases; a side file has no downstream consumer and will sit
  unused once the fix is applied, so there is never a reason to create one.
