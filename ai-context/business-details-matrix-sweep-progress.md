# Business Details matrix sweep — handoff notes

**Status: COMPLETE (2026-07-15).** All 5 planned states were swept across all 7 wizard steps.
Findings synthesized and 3 new cases merged into `ai-context/draft-privacy-policy-generator.json`
(now 12 pending cases); `coverage-gaps.md`'s stale-content entry was generalized. See "Final
outcome" at the bottom of this file for the summary. The rest of this file is kept as-is for
historical context on how the sweep was planned and executed.

Session token usage got high mid-task; this captures everything needed to resume in a fresh
session without re-deriving it. Read this in full before touching Playwright.

## The task

Systematically sweep Business Details' toggles on the Privacy Policy Generator (Company details
gap-closing pass, part of the same `/draft-section` gap-closing chain that already produced
`ai-context/draft-privacy-policy-generator.json`). At each state, check **every step in the
wizard sidebar** — Language preferences, Company details, Collection of data, Use of data,
Disclosure of data, Data retention, Miscellaneous disclosures, Preview & add policy — not just
the two sections originally proposed (Miscellaneous disclosures + Preview). The user explicitly
widened scope to "every section shown in the sidebar."

For each state, check **both the wizard form (input) and the generated policy (Preview, output)**
— not just Preview. The data-controller/representative bug (see below) only exists in the gap
between the two: the wizard field stayed visible with its value, but the value silently didn't
make it into the generated policy. Checking only one side would have missed it.

## Confirmed dependency chain (agreed with user, don't re-derive)

- **EU/EEA** — independent toggle, always available.
- **California** — independent toggle, always available.
- **For-profit organisation?** — only exists as a control if California = Yes. Not reachable
  otherwise. Pro+ gated.
- **Thresholds** ("cross revenue/customer thresholds?") — only exists if for-profit = Yes. Pro+
  gated.
- **Include CCPA clauses anyway?** — only exists if thresholds = No. Pro+ gated.
- **Sell/share personal info?** — independent toggle, always available.
  - Its two free-text follow-ups ("categories sold/shared", "third parties") only exist if
    sell/share = Yes. Already cased (39459 reveal, 39460 char-limit) — don't re-author.

**Practical consequence**: "for-profit = Yes" by itself (without thresholds also answered) is
believed to be a no-op downstream — the actual CCPA-content trigger is
`thresholds = Yes OR include-clauses = Yes`, not for-profit alone. This is an open question to
verify, not yet confirmed. See "Next steps."

A row like EU=1, CA=0, for-profit=1 is not a reachable state at all (for-profit control doesn't
exist without CA=Yes) — don't try to force it.

## Planned state sequence (agreed with user)

1. **Baseline (000)** — EU=No, CA=No, sell/share=No. *(In progress — see "Where we left off.")*
2. **EU alone (100)** — EU=Yes, CA=No, sell/share=No.
3. **California + thresholds alone (011-ish)** — EU=No, CA=Yes, for-profit=Yes,
   thresholds=Yes (the actual CCPA trigger), sell/share=No.
4. **Both together (111-ish)** — EU=Yes + the CCPA trigger from state 3.
5. **For-profit-without-thresholds edge case** — CA=Yes, for-profit=Yes, thresholds left
   unanswered/No — to confirm the "no-op downstream" belief from above.

At each state: reset cleanly (don't layer on top of the previous state's leftovers — go back to
Business details and explicitly re-toggle everything needed for full attribution), then walk
every wizard step in order, documenting what's visible in each. Only after all states are
collected, synthesize patterns and author cases — don't author cases mid-sweep.

## What's already confirmed — don't re-test from scratch

- **Collection of data** (categories by regulation): case 39469 already sweeps EU=No/thresholds=No
  (defaults only), EU=Yes/CCPA-n/a (GDPR categories added), and a Pro CCPA-applicable state
  (CCPA categories added). Reasonably solid — spend light effort here, cross-check rather than
  re-derive.
- **Additional information** (age/legal-basis/review questions): case 39478 sweeps similarly.
  Reasonably solid.
- **Disclosure of data existence**: cases 39458/39461 confirm the step appears on
  `sell/share=Yes OR thresholds=Yes OR include-clauses=Yes` (OR-logic, each condition
  independently shows/keeps/hides it).
- **Data retention**: cases 39482/83/98 don't reference EU/CA/for-profit at all in their
  preconditions — appears to be purely plan-tier-gated (Free vs Pro+), not regulation-gated.
  Confirm this once, don't sweep the full matrix against it.
- **Miscellaneous disclosures**: this is the real gap. 39484/85/86 don't state EU/EEA or
  CCPA-applicable in their preconditions at all — meaning they were tested at some unstated
  default, not systematically. Only two states have been checked this session
  (see below) — everything else in the matrix is unconfirmed here.

## Already-known bugs (don't rediscover, just watch if they resurface)

1. **Data controller/representative field** — doc claims `Shown if: EU/EEA = Yes` same as its
   sibling DPO field. Confirmed: DPO correctly hides when EU/EEA=No; this field does not — stays
   visible/editable, and its value is then silently dropped from the generated policy. Already
   drafted as Case 9 in `draft-privacy-policy-generator.json` (title: "[APP DEFECT — verify] The
   data controller/representative field is not hidden by EU/EEA=No...").
2. **"Privacy of children" stale content** — content-conditional clause (not GDPR-gated for
   presence, only for wording) that keeps showing the parental-consent variant after the
   under-16 question is cleared, instead of reverting to the default "we do not knowingly..."
   variant. **Held pending PM confirmation** — logged in `coverage-gaps.md`, not cased.
3. **"yes"-placeholder text** in two Disclosure-of-data-sourced clauses (past-12-months
   sale/sharing sections render literal string "yes" instead of real descriptions). Root cause
   not investigated. Logged in `coverage-gaps.md`.

## Where we left off (literal browser state)

- Logged into QA2 (`https://qa2.kilohub.com`) as the **Pro** account (`qa-accounts.json` key
  `pro`, site `hi.com`).
- On `Company details > Business details` tab, mid-reset toward baseline (000):
  - EU/EEA: already set to **No** (confirmed — clicked through the "Remove GDPR clauses?"
    dialog's "Remove" button).
  - California: just clicked **No** (confirmed selected via the last snapshot).
  - Sell/share: **still Yes** — the two free-text fields ("Contact details, browsing data" /
    "Marketing partners") were still showing in the last snapshot. **Next action: click No on
    "Do you sell or share the personal information of users?"** — may trigger a confirmation
    dialog similar to the GDPR one; handle it the same way (confirm removal).
- Contact information tab already has valid data filled in (Name: "Test Company", Website:
  "https://hi.com", Email: "contact@hi.com", Address filled) — no need to redo this.
- Once baseline (000) is confirmed clean, proceed to walk all 7 wizard steps and document, then
  move to state 2 (EU alone).

## Login reference (from `qa-accounts.json`, don't re-derive)

- Free account: `rahulkrishna+freeplansite@mozilor.com` — site `hd.com`.
- Pro account: `jacksnickel+protest@gmail.com` — site `hi.com`.
- Base URL: `https://qa2.kilohub.com` (from `.env` `QA2_BASE_URL`).
- Logout via the user-menu (top right, unlabeled button) → "Logout" menu item, then log in with
  the other account's credentials — session persists without needing explicit cookie-clearing.

## Where results should end up

- New cases (once the sweep is complete and patterns are synthesized): merge into
  `ai-context/draft-privacy-policy-generator.json`'s `cases` array (currently has 9 pending
  cases from two earlier passes — **do not overwrite**, append). `draft-section.md` Step 7 has
  already been patched to do this automatically in gap-closing mode; if invoking a fresh
  `/draft-section` for this, that logic will kick in.
- New gap/bug findings: `coverage-gaps.md` under "09. Legal Policies > Privacy Policy Generator".
- Reference: a cascade-map artifact was published earlier this session summarizing the fan-out
  structure (trigger → downstream location → confirmed/doc-only/bug status) — regenerate or ask
  the user for the link if useful context, it's not saved to a repo file.

## Next steps for the resuming session

1. Read this file in full.
2. Finish the baseline reset (click No on sell/share, handle any confirmation dialog).
3. Walk all 7 wizard steps at baseline, documenting each (light touch on Collection of
   data/Use of data/Disclosure of data/Data retention per the "already confirmed" section above;
   full attention on Company details/Miscellaneous disclosures/Preview).
4. Proceed through states 2–5 in the planned sequence.
5. Synthesize patterns, present findings to the user, get confirmation before authoring any new
   cases.
6. Merge confirmed cases into the draft file; log any new bugs/gaps into `coverage-gaps.md`.

## Final outcome (2026-07-15)

All 5 states confirmed the full dependency chain as originally agreed, plus resolved two open
questions:

- **for-profit=Yes alone is confirmed a no-op** — with thresholds=No and include-clauses=No, zero
  CCPA content appears anywhere (Miscellaneous disclosures or Preview). The actual trigger is
  `thresholds=Yes OR include-clauses=Yes`, exactly as suspected.
- **"Legal bases for collecting the data" question is confirmed EU/EEA-gated** in both directions
  (previously only observed with EU=Yes, never re-tested with EU=No) — same gating as the
  under-16 age question next to it.
- **New, previously undocumented section found**: "Do we share your information?" (GDPR
  sharing-basis section: consent / legal obligations / business transfers) renders in Preview only
  when EU/EEA=Yes.
- **Data-controller/representative bug (already cased as Case 9) reconfirmed as state-independent**
  — the field is never gated for visibility under any combination tested; its value only renders
  into Contact Us when EU/EEA=Yes, regardless of California/thresholds state.
- **Stale-content-on-toggle-flip pattern generalized** in `coverage-gaps.md` — the already-known
  "Privacy of children" stale-clause bug has a second confirmed instance: the "Sale/sharing... in
  the past 12 months" section renders contradictorily alongside "we do not sell/share" even when
  sell/share is currently No. Still pending PM confirmation on intended-vs-defect before casing.
- **"yes"-placeholder text was seen more broadly** on Disclosure of data's free-text fields during
  the sweep, but on reflection this is more likely leftover dirty test data from earlier sessions
  on the shared Pro account than a widened app bug — deliberately not broadened in
  `coverage-gaps.md` without a clean-data retest to isolate root cause first.

3 new cases were authored into `ai-context/draft-privacy-policy-generator.json` (now 12 pending,
unpublished cases total). Next step for that file is `/grill-section privacy policy generator`
before `/migrate-section`.
