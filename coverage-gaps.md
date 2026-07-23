# Known coverage gaps

Tracks scenarios identified during `/grill-section` or `/audit-section` passes that were
deliberately left uncased — not casing gaps due to oversight, but ones flagged and deferred
for a specific reason (plan tier unavailable, risk of a destructive action, out of scope for
that pass). Organized by v2 section (`testrail-suite-v2.md` numbering). Each section's
detail also lives in that section's `ai-context/cases-<slug>.json` under `out_of_scope_notes`
— this file is the cross-section index so gaps don't get lost between sessions.

Update this file whenever a gap is opened or closed. Mark closed gaps with ~~strikethrough~~
and the date/case IDs, rather than deleting the line — keeps the resolution history visible.

---

## 09. Legal Policies > Privacy Policy Generator

File: `ai-context/cases-privacy-policy-generator.json`

- ~~Final "Generate privacy policy" action~~ — **closed 2026-07-14**, cases 39596–39600
  (disposableuser account, Pro-plan site, safe because that account exists to absorb this
  kind of mutating/irreversible action).
- ~~Non-English secondary-language generation~~ — **partially closed 2026-07-15**, case 39604
  (multi-language selection persists correctly after Save draft and a browser refresh on a
  Pro account). **Still open:** per-language editing in Preview (editing an already-selected
  secondary language's translated content) was not exercised and remains uncased.
- **"HTML format" method on the Add-policy-to-site modal** — only "Code snippet" (the
  default-selected method) was exercised during the 2026-07-14 terminal-action re-grill.
- **"Install code" button on the "Policy installed?" confirmation dialog** — only "Yes, I
  have installed" was exercised 2026-07-14.
- **Post-generation editing surface** (Version history, Options menu, "Publish changes") —
  the 2026-07-14 re-grill stopped at the terminal "Yes, I have installed" state; editing an
  already-generated policy and republishing is a distinct, not-yet-cased surface.
- ~~Field-level boundary values beyond the representative cases~~ — **partially closed
  2026-07-16**, cases 39613–39621 (required + character-limit enforcement for Data Retention's
  custom-period and "Not yet decided" fields, and Disclosure of Data's age-category
  opt-in/opt-out, delete/correct/access, sensitive-info, and third-party-disclosure fields).
  **Further closed 2026-07-21**, cases 39730–39736 (Miscellaneous Disclosures: DPO/controller
  2000-char, CCPA metrics 2000-char, custom-safeguard 3000-char + multi-select/duplicate
  validation, verbatim-rendering, toggle-to-No cleanup; Collection of Data > Additional
  Information: cookie-policy-link 2000-char, DNT 2500-char, review-change-process 2500-char) —
  also merged a related No-variant/clean-toggle check into existing case 39486 rather than
  publishing a near-duplicate. **Still open:** boundary values for Company Details fields
  remain untested individually, covered only by representative equivalence-partitioning
  patterns by design.
- **Toggling an answer back to "No" leaves that answer's prior "Yes"-state content stale in
  the generated Preview, instead of reverting or removing it** — a pattern first found
  2026-07-15 during a Company details gap-closing pass and reconfirmed as broader during the
  2026-07-15 Business Details matrix sweep (`ai-context/business-details-matrix-sweep-progress.md`).
  Two confirmed instances of the same root cause:
  - **"Privacy of children" clause** retains stale Yes-variant content after the "under 16"
    answer is cleared. The clause is content-conditional (not GDPR-gated for presence — it
    always renders; only its wording varies by the under-16 answer). Confirmed live: baseline
    default (never answered) correctly shows the No-variant text; answering under-16=Yes
    correctly switches to the parental-consent variant; but setting EU/EEA=No afterward (which
    clears the under-16 question from the wizard) leaves the parental-consent variant stuck in
    the generated policy instead of falling back to the default.
  - **"Sale/sharing of information in the past 12 months" section** renders simultaneously
    with the sibling "Sale/sharing of information" section (which correctly states "We do not
    sell or share...") even when sell/share is currently set to No — reconfirmed at every
    state checked during the matrix sweep (baseline, EU-alone, CA+thresholds, EU+CCPA
    combined, for-profit-alone). The section's *presence* is the defect, independent of
    whatever free-text content is stored inside it (that content may separately be leftover
    dirty test data from earlier sessions on the shared Pro account — not re-confirmed as a
    templating bug; would need a clean-data retest to isolate).
  **Needs PM confirmation** on whether this stale-content-on-toggle-flip pattern is intended
  behavior or a defect before either instance gets cased — not authored into
  `draft-privacy-policy-generator.json` pending that answer.
- **"yes"-placeholder text appearing as clause body content** — noticed as a side effect
  during the same pass, not investigated further. "Sale/sharing of information in the past
  12 months" and the CCPA "Sale or share of information" sections both render the literal
  string "yes" where a free-text description is expected. Root cause not chased; flagged for
  a future pass.
- **Layer 2 Plan Gates cases missing for this feature** — identified 2026-07-16. PPG's
  clause/field-level gates (for-profit question, CCPA-gated chips, the entirely-gated
  Disclosure of data step, the retention "Not yet decided" option — cases 39494–39498) exist
  only as Layer 1 touchpoint cases in the feature section; no Layer 2 case in
  `11. Billing & Upgrade > Plan Gates` consolidates them per plan tier. Per
  `testrail-suite-v2.md`'s "Plan-gated features" Layer 2 feature-scoped exception (added
  2026-07-16), needs one case per plan tier — e.g. `[Plan Gates] Privacy Policy Generator —
  Free plan`, `... — Pro plan` (Basic confirmed identical to Free for every CCPA touchpoint in
  Collection of Data as of the 2026-07-16 re-sweep — for-profit is Pro+-locked on Basic too,
  so CCPA never becomes reachable there; likely a shared precondition rather than its own case
  body, but re-confirm across the rest of the wizard before assuming that holds everywhere).
  **Held 2026-07-16, not just for this feature** — every section in the suite has plan gates,
  so this needs a suite-wide check (which sections already have their Layer 2 case, which have
  only scattered Layer 1 touchpoint cases like PPG did) before authoring PPG's specifically, to
  avoid doing this section-by-section piecemeal. Not yet authored; needs user approval before
  casing either way.
- **"Start over" may not fully reset a saved draft** — observed 2026-07-16 on the Pro account
  during a Collection of Data re-sweep. After "Start over" on a wizard with a prior saved
  draft, the sidebar showed Collection of data/Use of data/Disclosure of data/Data
  retention/Miscellaneous disclosures as already complete, and the dynamic "Disclosure of
  data" step was already present, despite Business Details being freshly unanswered. Actual
  navigation was still correctly re-blocked until Business Details was re-answered, so this
  looks like a stale-checkmark cosmetic issue rather than data loss — but it's relevant to the
  wizard shell's already-flagged, unresolved "Start over" open question
  (`docs/wiki/09-legal-policies/privacy-policy-generator.md`, Resume-draft dialog). Not yet
  root-caused or cased; wizard-shell scope, not Collection of Data.
- **Post-purchase success toaster not cased** — identified 2026-07-20. Completing a plan
  purchase/upgrade initiated from the PPG page (e.g. via a plan-gate nudge) should display a
  confirmation toaster message, but no case exercises this. Exact copy and trigger point (which
  gate, which checkout step) not yet confirmed live — needs a grill pass before casing.

---

## 09. Legal Policies > Cookie Policy Generator

File: `ai-context/cases-cookie-policy-generator.json`

- **Correction (2026-07-22):** an earlier pass here wrongly concluded this section was entirely
  unpublished, because `09. Legal Policies > Cookie Policy Generator` (id 1974) is a parent
  category with zero cases of its own — the 97 real cases live in its ten children
  (`Wizard Navigation & Progress`, `Language Settings`, `About Cookies`, `Use of Cookies`,
  `Types of Cookies`, `Cookie Preferences`, `Generate Policy`, `Policy Preview & Translations`,
  `Install & Publish`, `Manage Policy`, ids 1990–1999) plus 12 cases correctly routed out to
  `11. Billing & Upgrade > Plan Gates` by `plan_gate_flag`. `cases-cookie-policy-generator.json`
  was added to `ai-context/` after this note was first written and confirms full coverage — every
  live case is tracked locally and vice versa. The one real defect from the earlier pass stands:
  case 39543's precondition referenced a sibling case as "case 43", a draft-array placeholder
  that was never resolved to a real id and, per that draft's own missing feature-section file at
  the time, looked dangling — it has since been fixed to state the fact inline without a
  cross-reference (2026-07-22). Note for future audits: `validate-cases-file --verify-completeness`
  does not walk child sections, so pointing it at a parent section id like 1974 will falsely flag
  every case without a per-case `section_id` override as `stale_local_case` — check the section's
  live children before trusting that output.
- **Confirmation toaster on "Continue with Free plan" not confirmed** — identified during a
  grill pass on case 39553 (Free-plan account, "You've chosen the Free plan" dialog >
  "Continue with Free plan"). No confirmation toaster was captured after clicking the button,
  but every other generate/regenerate/update action in this feature does show one — if the
  absence is confirmed on a re-check, that would itself be a real inconsistency worth a bug
  report. Not re-verified since; needs a follow-up grill pass on case 39553 specifically.
- **Same "case NN" dangling-reference bug found in a second case (2026-07-22)** — case 39553
  (`Generate Policy` sub-section, not Plan Gates) had the identical "see case 53" placeholder in
  its preconditions as 39543/39551/39552/39554. Fixed locally and live (→ "see case 39551").
- **`/audit-section` full pass completed 2026-07-22** — all 97 cases audited against Suite 6
  source; `audited_at` set in the cases file. Findings needing follow-up, not yet resolved:
  - **39548** — button label "Get started with Basic plan" diverges from Suite 6 ("Select Basic
    plan & generate policy"), but the case's own grill note says the new label was independently
    live-confirmed. `grill_status: skipped:external-url` doesn't carry the usual
    confirmed/fixed protection, so the mechanical priority rule can't resolve this on its own —
    needs a human call on whether to reclassify this case's grill_status.
  - **39552** — Free-plan "View all features" tooltip's 5-item list content (from Suite 6) was
    deliberately left unasserted rather than restored, because the analogous Basic-plan list
    (case 39544) turned out much longer post-redesign — the old 5-item list may be stale. Needs a
    live check to confirm the current Free-plan list, then case the real content.
  - **39553** — the toaster-absence gap above; text-fidelity audit confirms Suite 6 did assert
    toaster text here, reinforcing that a live re-check (not a source restore) is the right next
    step.
  - **39593, 39594, 39595** — newly-suggested gap cases with no Suite 6 precedent
    (`source_case_ids: []`); all quote specific on-page text ("Policy preview" dialog title,
    "One-click install" panel strings, "Edit cookie policy" button) that has never been checked
    against the live app. Need a live spot-check pass.

---

## 10. Profile & Account > Organisations & Sites

File: `ai-context/cases-organisation-and-sites.json`

- **Shopify-connected site cross-account transfer needs a live-verify test account** — a
  Shopify-connected site (created via the Shopify app install) is blocked from cross-account
  transfer with the error "This site can only be transferred to an organization you own, as it
  is connected to your account via CookieYes' Shopify app." Sourced from C9717/C17212 (C11237,
  filed under the Shopify section but showing the generic banner instead, is a
  faulty/mislabeled duplicate from a Suite-6 section mix-up, excluded as a source). Case not
  yet live-verified — needs a Shopify-connected test site, which doesn't currently exist in
  `qa-accounts.json`.
- **"Add staging site" Plan Gates touchpoint may need consolidating** — verified live
  2026-07-10 as plan-gated (disabled with a premium/upgrade badge icon on Free plan, enabled on
  Basic). Cased per `migration-conventions.md` §6 as its own `plan_gate_flag: true` case routed
  to `11. Billing & Upgrade > Plan Gates`, since no existing Plan Gates case covered this
  touchpoint. May need merging into a consolidated per-plan Plan Gates walkthrough case later
  rather than staying a standalone touchpoint case.

---

## 11. Billing & Upgrade

- **Auto-unlocked free 14-day Pro trial on new signup** — identified 2026-07-21 during the
  `01. Authentication > Sign Up > Core` grill (a real signup + email-verification test).
  Immediately after verifying a brand-new free-signup account, the Dashboard shows a modal:
  "Get the best of CookieYes with Pro Plan" / "We've automatically unlocked a free 14-day Pro
  trial, no setup, no card required. Enjoy advanced scans, higher pageview limit, and more
  control!" with a feature list (4,000 pages/scan, 300,000 pageviews/month, geo-targeted
  banner, monthly scheduled scanning) and an "Explore Pro features" button. No existing case
  in any published section covers this. Belongs in `11. Billing & Upgrade` (trial display /
  nudge conventions), not in Authentication — out of scope for the Sign Up Core pass that
  found it. Not yet authored; needs a grill pass on Billing & Upgrade once that section is
  migrated.
  **Addendum 2026-07-21** (found during the Standard (Free) restore grill): the same modal
  fires regardless of which signup page-copy variant was shown (see the Standard (Free) entry
  below), and on at least one throwaway account the resulting trial state was internally
  contradictory — see that entry for detail. Relevant to whichever case(s) eventually cover
  this modal.

---

## 01. Authentication > Sign Up > Standard (Free)

File: `ai-context/cases-signup-standard-free.json` (currently mid-restore, see
`draft-signup-standard-free.json`)

- **Signup page has two different copy variants — confirmed intentional A/B experimentation,
  not a bug** — identified 2026-07-21 during the restore grill, cause confirmed by the user
  same day. Free signups are randomly assigned to one of (at least) two trial-model variants:
  "Create Your Free Account" / "Get a lifetime free account. No obligations." / "Get Started"
  vs. "Start Your 14 Day Free Trial" / "We've automatically unlocked a free 14-day Pro trial —
  no setup, no card required." / "Start Free 14-Day Trial". (Original theory during the grill —
  a stale marketing/attribution cookie — was wrong; re-testing with fully cleared cookies still
  produced both variants across repeated /signup loads once enough samples were taken, matching
  random per-signup assignment rather than a sticky cookie flag.) Per the user: this is a live
  experiment and the team plans to converge on **one** trial model soon. Both variants share
  identical field behavior (no required-attribute markers, same checkbox text) and both lead to
  the same post-signup Pro-trial-unlock dashboard modal (see the Billing & Upgrade entry above).
  Not cased pending convergence — casing exact copy for a variant that's about to be retired
  would need re-verification immediately after the experiment concludes anyway. Re-grill this
  case once the user confirms the experiment has ended and one variant is canonical.
- **Contradictory trial-state display on a freshly-created account** — identified 2026-07-21.
  On a brand-new Standard (Free) signup (clean-session "Get Started" flow, websiteId 2591),
  the Dashboard simultaneously showed: the plan badge reading "Pro (Trial not started)", a
  separate banner on the same page reading "Your trial has expired: Upgrade to activate
  banner", and the "We've automatically unlocked a free 14-day Pro trial" modal firing as if
  the trial were newly active. Three mutually contradictory trial-state signals on one
  never-before-used account. Same pattern as the already-flagged PPG stale-content-on-toggle
  issue (`09. Legal Policies > Privacy Policy Generator` entry above) in that it's a real,
  reproducible inconsistency but the *intended* behavior isn't obvious from the UI alone.
  **Needs PM/dev confirmation** on which state is correct before casing either the "confirmed"
  or the "bug" version.
- **Password show/hide toggle works but isn't cased for this page** — confirmed live
  2026-07-21 that clicking the eye icon on the signup page's Password field correctly toggles
  the input between masked and plaintext. Not currently covered by any published case:
  `cases-login.json` has an equivalent case (39666) but scoped to the Login page only, and
  `cases-signup-core.json` — despite owning "form validation... shared across all signup
  pages" per the section tree — has no toggle-behavior case at all. Belongs in
  `01. Authentication > Sign Up > Core` as a shared case, not in Standard (Free); not authored
  here or there pending a decision on whether to add it to the already-published Core section.

---

## 01. Authentication > Sign Up > Core

File: `ai-context/cases-signup-core.json`

- **Resend-verification-email cooldown timer** — identified 2026-07-21 during the grill pass.
  On the "Your email verification failed!" page, clicking "Resend Verification Email" shows
  "Verification email has been resent successfully." and replaces the button with a countdown
  ("Resend email in `<N>` seconds", observed starting at 56s) before it can be clicked again.
  A full case spec was drafted and reviewed with the user, but never explicitly approved
  (`approve 1`) before the review gate closed with `done` — per `/migrate-section`'s rule,
  unapproved suggested cases are dropped rather than published. Repro: sign up for a new
  account, open the real verification email, edit the `identity` query parameter (not `token`
  alone — `identity` is what resolves the account; an invalid token with a still-valid,
  already-verified `identity` succeeds instead of failing) to an invalid value, navigate to the
  edited link to reach the failure page, then click Resend. Distinct from the similar-looking
  cooldown already cased for My Account's email-update flow (case 37242 in
  `cases-my-account.json`) — not a duplicate. Needs explicit approval before authoring.

---

*(Add new sections below as gaps are found elsewhere in the migration.)*
