---
name: verify-case-live
description: Log into CookieYes QA2 (reusing an existing session where possible) and verify one case-shaped object (title, preconditions, steps) against the live app, returning a per-step verdict. Internal engine shared by /grill-section and /wiki-sync — not meant to be invoked directly by a user, and does not decide which cases to run or what to do with the verdict.
disable-model-invocation: true
---

# Verify Case Live

Adversarially verify a single case-shaped object against the live CookieYes QA2 app using
Playwright, and return a verdict. This is the shared engine behind `/grill-section`'s per-case
verification and `/wiki-sync`'s live-check mechanism (its Step 3 "Mechanism"). Callers own
everything before and after this skill runs: which cases to verify, in what order, and what to do
with the verdict (write `grill_status` to a draft file, or feed it into a reconciliation step).

**This skill never writes to any file.** It only returns verdicts. Persisting them is the caller's
job.

---

## Input contract

- `case` — `{ title, preconditions, customStepsSeparated: [{content, expected}] }`. Source doesn't
  matter — a draft file's case, an already-published case, or a synthetic object built on the fly
  for a one-off live check. No TestRail `id` is required.
- `required_plan_tier` (optional) — pass it if the caller already knows the plan tier this case
  needs. Otherwise this skill infers it from `preconditions` (see Plan detection below).

Session state (`current_account`, whether login has happened yet) persists across calls within the
same run — the first call in a run performs the initial login; later calls only switch accounts
when the required tier changes.

## Output contract

One verdict per step (or one overall verdict, per the caller's need):

| Verdict | Meaning |
|---|---|
| `confirmed` | Step and expected result match the live app exactly |
| `mismatch` | Expected result is wrong — returned with fix text (current wording only, see the Fix-text rule below) |
| `broken` | The step cannot be performed (UI element missing, page doesn't exist, etc.) |
| `skipped:<reason-code>` | Could not be automated — see Skip reasons below |
| `needs-manual-check` | Inconclusive — flag for human review |

(There is no "gap found" verdict here — hunting for scenarios no case covers is the caller's own
exploration step, not something this skill does.)

---

## Account & session management

### Load the account pool

Read `qa-accounts.json` from the project root — the source of truth for every account and its
credentials (`accounts.<key>.email` / `.password` / `.plan`, plus an optional per-account `.env`
override). Build an account map keyed by plan tier (e.g. `free`, `basic`, `pro`, `ultimate`). If the
file does not exist, tell the caller: all plan-gated cases must be skipped, continue without an
account pool.

Do not read `$QA2_TEST_EMAIL` / `$QA2_TEST_PASSWORD` from the environment; those are not used by
this skill. If `qa-accounts.json` is absent, stop and report that it's required for login — there
is no environment fallback.

Track a `current_account` variable for the life of the run. On the first call, it starts as the
`free` account from `qa-accounts.json` (lowest tier, so the most plan gates are visible by default).

### Log in (first call only)

Use the Playwright MCP browser tools to:

1. Navigate to `current_account`'s `.env` value if it has one; otherwise `$QA2_BASE_URL`
   (environment — only used for the base URL, never for credentials).
2. If redirected to a login page, fill in `current_account`'s `email` and `password` from
   `qa-accounts.json` and submit.
3. Confirm you land on the Dashboard (or equivalent post-login page).
4. Take a screenshot and report the logged-in state and current plan tier.

If login fails, stop and report — do not proceed with an unauthenticated session.

### Plan detection

Infer the required tier from the case's `preconditions` text (skip this if `required_plan_tier`
was passed explicitly):

| Signal in preconditions | Required account key |
|---|---|
| "Pro plan", "Pro or higher", "paid plan (Pro or higher)" | `pro` |
| "Ultimate plan" | `ultimate` |
| "free plan", "Free account" | `free` |
| "paid plan" (generic, no tier named) | lowest paid tier available in `qa-accounts.json` |
| No plan mention | current default account |

### Session switching

Before verifying each case:
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
   Then navigate to that account's `.env` value if it has one, otherwise `$QA2_BASE_URL`, log in
   with its `email`/`password` from `qa-accounts.json`, confirm Dashboard, update
   `current_account`.
4. If it differs and no matching account exists in `qa-accounts.json` → return `skipped:plan-gated`
   without executing the case.

Reuse the same browser session across consecutive cases on the same account — only switch when
the required plan tier actually changes.

### Role verification

Before executing any case whose correctness depends on a specific role (a `permission_flag` case,
or any case whose preconditions name a role such as Admin/Editor): verify the acting account's
actual `role_slug` via the Team page or `GET /api/v2/user` (`organization_users[].role_slug`)
before relying on it — do not assume the role recorded in `qa-accounts.json` still holds.
Ownership-transfer round-trips silently change roles: CookieYes retains the previous owner at
Admin access after a transfer, so an account used as an ownership-transfer recipient earlier in
this same run (or a prior one) may no longer be the role it started as. If the role doesn't match
what the case requires, correct it (Team page > ⋯ > Change role) before proceeding — do not return
a verdict against a role-tainted account.

---

## Verify the case

### Navigate to the starting state

Use the case's `preconditions` to reach the correct starting page/state. If it says "User is on
the Sign Up page", navigate there directly. Note any navigation issues.

### Execute the steps

Walk through each step in `customStepsSeparated`:
- Perform the action described in `content`.
- Observe what the app actually does.
- Compare against the `expected` result.

**Always drive inputs the way a real user would, and always trigger the real submit action — never
infer a verdict from DOM state alone.** Use Playwright's actual typing/`.fill()` methods, not
`dispatchEvent` or direct `.value` assignment: those bypass the framework's input handlers and can
silently fail to trigger validation. For any step whose expected result is a validation message or
a submit-triggered outcome, actually click the real submit control (Save, Publish, etc.) before
recording the verdict — many validation messages only render on submit, not on type/blur, so a
verdict recorded without clicking submit is not evidence of anything. If a step produces no visible
effect, treat that as inconclusive and re-check your input method before recording a mismatch.

### Determine the verdict

**Word-for-word means word-for-word.** `confirmed` already requires the expected result to match
the live app exactly — for any expected result that quotes specific text as appearing on the page
(per `migration-conventions.md` §4, "Quoted on-page text — always verbatim"), "exactly" means
character-for-character, not "captures the same idea." No category filter: this applies whether the
quote is a legal disclosure or a plain status badge — if the case quotes it, it must be right. If
the case's quote is close but reworded compared to what the live app (or a received email) actually
shows, that is a `mismatch`, not a pass — return the exact live wording as the fix, the same as any
other mismatch.

**Verify this by extraction, not by eye.** Do not judge a quoted-text match from a screenshot or an
accessibility-tree summary glanced over — both are easy to skim past a wrong word, a dropped
sentence, or a swapped label. For every step whose expected result quotes on-page text (a button
label, tooltip, dialog/banner copy, validation message, confirmation toast — anything the case
presents as literal copy), pull the actual rendered string for that specific element with
`browser_snapshot` or `browser_evaluate` (reading `textContent`/`innerText` on the element, not a
full-page dump), then compare that extracted string against the case's quoted text
character-by-character — punctuation, capitalization, and whitespace included. Only return
`confirmed` once that literal comparison passes; a single-character difference is a `mismatch`,
returned with both strings shown side by side (`expected: "..."` / `actual: "..."`) and the
extracted live text as the fix. This is what catches, at verify-time rather than in a later
retrospective audit, a case claiming a "Copy code" button in the "top-right corner" when the live
button is actually labeled "Copy" and left-aligned, or a banner alert paraphrased away from its
real wording.

**The fix text is the current wording only — never a comparison against what it replaced.** When
returning a `mismatch` fix (or any other correction to a precondition or expected result), the fix
is just the correct, current text. Never append a parenthetical contrasting it with the old/stale/
reworded/previously-drafted version (`(NOT "..." — that label no longer exists)` and similar). A
case body is read cold by someone with no memory of what it used to say — a negation of text
they've never seen is confusing, not clarifying, and this phrasing has already leaked into
published cases (see `coverage-gaps.md` history). If the discrepancy itself is worth preserving —
why it changed, when it was caught, whether it needs a follow-up — that's the caller's job to
record in `coverage-gaps.md` or a run log, not something this skill embeds in the fix text.

### Skip reasons — automatically skip and return the reason, do not attempt to execute

| Reason code | When to apply |
|---|---|
| `email-required` | Case expects receiving an actual email (verification link, reset email, notification) |
| `time-dependent` | Case requires waiting (expired token after 1 hour, trial day X, "more than N hours after") |
| `destructive-precondition` | Precondition requires a destructive account state (deleted account, cancelled subscription) |
| `plan-gated` | Required plan tier is not available in `qa-accounts.json` (no matching account to switch to) |
| `external-url` | Step navigates to a third-party URL outside the app (T&C, Privacy Policy, marketing site) |
| `manual-only` | Case explicitly marked for manual verification (e.g. contains "[verify manually]" in steps) |

Return `skipped:<reason-code>` — do not mark it as failing.

---

## Rules

- Never silently drop a case — every invocation returns a verdict, even if it's just `confirmed`.
- Do not modify expected text based on assumptions — only return a `mismatch` fix where the live app
  directly contradicts the case. Flag everything else as `needs-manual-check`.
- If QA2 is behind a paywall gate for a specific plan, that's `skipped:plan-gated` for this case
  only — never a reason to abort the whole run.
- Reuse the same browser session for all cases on the same account. Only switch sessions when the
  required plan tier changes.
