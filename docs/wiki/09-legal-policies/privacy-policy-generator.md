# Legal Policies > Privacy Policy Generator

**Nav path:** Legal Policies > Privacy Policy Generator (entered from the Dashboard/Legal Policies
nav; a multi-step wizard, each step its own route)
**Route:** (not captured in source data — needs live verification of exact per-step URLs)
**Roles:** Account Owner, Admin, Editor — no case data suggests divergent access; treat as equal
until a permission case says otherwise.
**Plan gating:** Extensive and inconsistent in presentation — three distinct plan-gate UX patterns
coexist in this one feature (see "Plan gating patterns" below). Full CTA/plan matrix lives at
[../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md); this page only
documents what's gated and how it visually presents at each touchpoint.

This page covers the whole wizard in one file for now (progress is section-by-section within it,
not split into separate files per step) — update it in place as more of the feature gets
live-verified.

## Purpose

The Privacy Policy Generator builds a publishable privacy policy through a Q&A wizard. The site
owner declares their regulatory footprint (EU/EEA users? California users?) and business
practices (what data is collected, why, how long it's kept, who it's disclosed to), and the
wizard compiles the answers — verbatim in some places, mapped to boilerplate legal clauses in
others — into a generated policy that can then be published to the site.

## Wizard shell & navigation (cross-cutting)

These behaviors apply across every step, not to one specific page — they're the wizard's shell,
not step content.

**Step list.** A vertical sidebar lists the wizard steps in order: Language preferences, Company
details, Collection of data, Use of data, Disclosure of data, Data retention, Miscellaneous
disclosures, Preview & add policy. Steps other than the current one stay disabled until reached.

- **The "Disclosure of data" step is dynamic** — it does not appear at all by default. It appears
  only when at least one of three conditions on Business details is true: "sell or share personal
  information" = Yes, OR CCPA thresholds = Yes, OR "include CCPA clauses anyway" = Yes (an
  OR-trigger across all three, each confirmed to independently show/keep/hide the step). With all
  three at their default/No state, the step is absent and the sidebar shows only 7 entries, not 8.
- Above the step content: an "X% complete" label and progress bar that updates as steps are
  completed.
- Bottom action bar: "Previous", "Save draft", "Next" — the final step (Preview & add policy)
  shows "Generate privacy policy" instead of "Next".
- A "Preview privacy policy" button sits at the top of the step content area on every step,
  independent of the final "Preview & add policy" step (see below).

**Resume-draft dialog.** Re-entering the wizard with an already-saved draft shows a dialog: "You
have a saved privacy policy draft. Continue where you left off or start over from the beginning."
with buttons "Start over" and "Resume draft". "Resume draft" reopens on the last saved step with
answers intact. "Start over"'s actual effect on previously-saved answers has not been confirmed
live — deliberately avoided during crawling to protect in-progress test state.

**Unsaved-changes dialog.** Editing a field without saving, then clicking a different sidebar
step, shows: "You have unsaved changes. Save your draft before switching steps, discard changes
and reload your last saved draft, or stay on this step." with three buttons:
- **"Save and continue"** — saves the edit (confirmed to persist through a full page reload, not
  just in-memory) and navigates to the selected step.
- **"Stay here"** — closes the dialog, keeps the unsaved edit, stays on the current step.
- **"Discard changes"** — reverts the edit and navigates away. Confirmed scoped correctly to just
  the one edited field/step (contrast with the "Back to Dashboard" Discard below, which is not
  scoped the same way).

**Save-progress dialog (exiting via "Back to Dashboard").** Clicking "Back to Dashboard" with
unsaved data shows a dialog titled "Save progress?" with body "Save a draft to continue where you
left off when you return." and buttons "Discard", "Save draft" (plus a Close icon).
- "Save draft" shows "Draft saved successfully!" and navigates to the Dashboard.
- The Close (X) icon stays on the current step with everything unchanged.
- **[APP DEFECT — confirmed]** "Discard" here does **not** behave like the unsaved-changes
  dialog's Discard — it reverts the **entire draft**, not just the current step's unsaved edit.
  Confirmed reproducible: discarding one unsaved DPO-field edit on Miscellaneous disclosures also
  blanked out Company details > Contact information entirely, dropped overall progress back to
  10%, and made the dynamic "Disclosure of data" step disappear (its trigger condition reverted
  too). This is a full-draft rollback to some earlier checkpoint, not a scoped undo — root cause
  (which checkpoint it reverts to) isn't determinable from the UI alone. Treat as a data-loss risk
  worth flagging to engineering, not a case-authoring error.

**"Preview privacy policy" popup.** Reachable from every step via the button at the top of the
step content area — distinct from the final "Preview & add policy" wizard step. Opens a dialog
titled "Preview privacy policy" that renders the full policy from whatever has been entered so
far, using default content for anything not yet filled in, **translated into whichever primary
language is currently selected** (confirmed fully translated end-to-end, including the policy
heading and every section heading, when German was the selected primary language — even at 0%
wizard completion). On a Free-plan account this popup also shows an upgrade nudge: "Your privacy
policy is missing a few clauses" / "Upgrade to Pro plan to add all the required clauses, to ensure
your policy covers key legal requirements." Closing the popup returns to the same wizard step with
no data changed.

## 1. Language Preferences

- A primary-language selector offers English, Français, Deutsch, Italiano, Español —
  **single-select**: choosing a new one deselects whichever was previously primary.
- Clicking "Next" with no primary language selected shows: "Please make sure that all fields are
  completely filled out before we continue with the process." and stays on the step.
- Once a primary language is chosen, a **"Generate policy in multiple languages" (Basic+)**
  section appears below it, listing the four non-primary languages as secondary-language options
  (the list always excludes whichever language is currently primary, and updates live if the
  primary selection changes).
  - Free plan: secondary-language buttons are disabled, with the text "Upgrade to Basic or above
    to enable multi-language support."
  - Basic plan and higher: secondary-language buttons are enabled and **multi-select** — more than
    one secondary language can be selected and stay selected simultaneously (unlike the
    single-select primary selector).
- **Persistence is asymmetric between primary and secondary selections:**
  - An unsaved **primary**-language change is lost on browser refresh — the previously-saved
    primary reappears, the unsaved selection does not stick.
  - Multiple **secondary**-language selections, once explicitly saved via "Save draft", correctly
    persist through a full page reload (confirmed with three languages: one primary, two
    secondary, all three still correct after reload).
- A "What to know" hints card sits beside the selectors with two fixed Q&A entries about
  translation defaults (verbatim, confirmed identical across Free and Pro tiers):
  - "Are translations available for these languages?" — "Yes. We provide default translations for
    the languages you select. After generating your policy in the primary language, you can review
    and customise each translation to ensure accuracy and local relevance. Offering your privacy
    policy in multiple languages helps meet legal requirements for clarity and accessibility under
    laws like GDPR and CCPA."
  - "Will updates to the default content apply to all translations?" — "No. Changes made to the
    default content won't automatically update your translated versions. Be sure to review and
    adjust each translation after editing your primary policy."
- Clicking "Upgrade to Basic" on the locked multi-language section opens a "Your Privacy Policy is
  incomplete" upgrade modal (see Plan gating patterns below).

## 2. Company Details

### 2a. Contact Information (default tab)

Fields: "Name (either company or individual)" (placeholder "John Doe"), "Website URL"
(placeholder "www.yoursite.com"), "Email address" (placeholder "john@yoursite.com"), "URL to
contact (if applicable)" (placeholder "www.yoursite.com/contact", **optional** — confirmed the
wizard proceeds with it empty), and "Full address" (multi-line placeholder).

Validation (all confirmed live, exact message text):
- Name: 300-character limit — "Please limit your response to 300 characters."
- Website URL: format-validated ("Please enter valid URL") and 500-character limit.
- Email address: format-validated ("Please enter valid email address").
- URL to Contact: optional, 2000-character limit.
- Full Address: 1000-character limit.
- Switching to the Business details tab while a required field is empty is blocked; each empty
  field shows inline "This field is required" (or "Please enter valid address" for Full address),
  plus a page-level banner: "Please make sure that all fields are completely filled out before we
  continue with the process."
- The "URL to Contact" tooltip reads: "The 'URL to contact' refers to the link users can use to
  reach support in case of issues or questions regarding the privacy policy. This is not a
  mandatory field." (live renders typographic curly quotes around 'URL to contact', not straight
  quotes).

### 2b. Business Details

The largest, most interconnected cluster in this feature — a chain of toggles that determines
which regulatory clauses (GDPR, CCPA) apply, and which downstream steps/fields appear throughout
the rest of the wizard.

**The toggle chain, fully mapped:**

| Toggle | Availability | Downstream effect |
|---|---|---|
| Do you have users in EU/EEA? | Always available, any plan | Gates GDPR-specific fields/clauses everywhere in the wizard (see below) |
| Do you have users in California? | Always available, any plan | Gates the "for-profit organisation?" control |
| Are you a 'for-profit' organisation? | Only exists if California = Yes. **Pro+ gated.** | Gates the CCPA thresholds question |
| Do you cross one or more of the following thresholds? | Only exists if for-profit = Yes. **Pro+ gated.** | One of three OR-triggers for CCPA content (see below) |
| Do you want to include CCPA-compliant clauses even if not legally required? | Only exists if thresholds = No. **Pro+ gated.** Becomes mandatory once shown — leaving it unanswered blocks navigation. | The other alternate OR-trigger for CCPA content |
| Do you sell or share the personal information of users? | Always available, any plan | Third OR-trigger; also reveals two free-text fields (below) |

**Confirmed: "for-profit = Yes" alone is a no-op for CCPA content.** The actual trigger for all
CCPA-specific content (the "Disclosure of data" step, the CCPA fields on Miscellaneous
disclosures, the CCPA section in the generated policy) is `thresholds = Yes OR include-clauses =
Yes` — for-profit alone, without either of those also being Yes, produces zero CCPA-specific
content anywhere in the wizard or the generated policy. This was an open question, now resolved
live.

**Toggling California or EU/EEA from Yes to No prompts a removal-confirmation dialog** rather than
silently switching:
- California: "Remove CCPA clauses from your policy?" — "If you remove this clause, all
  CCPA-related sections will be excluded from your policy. Your policy may no longer meet
  California's data privacy requirements." Buttons: "Keep clause", "Remove", Close.
- EU/EEA: "Remove GDPR clauses from your policy?" — "If you remove this clause, all GDPR-related
  sections will be excluded from your policy. Your policy may no longer meet EU/EEA data
  protection requirements." Same button pattern.
- Both dialogs only appear going Yes → No; setting No → Yes applies immediately with no dialog.
- "Remove" genuinely takes effect (answer flips to No, dependent questions/fields disappear
  throughout the wizard); "Keep clause" cancels and leaves the answer at Yes.

**"Sell or share personal information" = Yes** reveals two free-text fields: "Provide the
categories of personal information that are sold or shared" and "...the categories of third
parties to which such information is sold or shared" (both accept and retain free text, both
enforce a 2000-character limit at submit time via "Please limit your response to 2000
characters." — note both internal spec docs state a stale 500-character limit; live has already
shipped the higher limit).

**Tooltips (verbatim, confirmed live):**
- EU/EEA: "Applies to any business that collects and processes the information of EU/EEA
  residents. List of EU/EEA countries:" followed by a link to the UK government's EU/EEA country
  list.
- California: "The CCPA does not mention anything about accidental or one-time visitors. However,
  if your service does not target users from California, you may choose not to answer 'Yes' to
  this question, although it is recommended to do so."
- For-profit: "Under the CCPA/CPRA, only for-profit businesses that collect, share, or sell
  personal information of California residents are required to comply. Nonprofits and government
  entities are generally exempt." (tooltip is reachable via hover even while the control itself is
  Pro+-locked/disabled.)
- Thresholds question lists three criteria verbatim — quote exactly, the third one has slightly
  awkward live phrasing, don't smooth it out: "$25 million or more gross revenue in the previous
  calendar year."; "Process information for 100,000 or more customers"; "Earns 50% or more revenue
  from the sale of the personal information of the customers (including those shared for of
  cross-context behavioural advertising)".

**On a Free plan**, "for-profit organisation?" shows a "Pro+" badge, disabled Yes/No buttons, and
inline text "Upgrade to Pro or higher to add this and the subsequent clauses. CCPA applies only to
eligible for-profit businesses (see criteria on the right -->)." — see Plan gating patterns below.

## 3. Collection of Data

### 3a. Personal Information (default tab)

A chip-selector grid grouped into sub-sections, each with an "add custom" free-text input:

- **Personal data:** Name, Address, Email address, Identification ID number\*, Location data\*,
  Birthday†, Political and religious affiliations†, Biometric information, + custom entries.
- **Behavioral & financial data**†: Internet browsing history, Income and similar information,
  Commercial information.
- **Professional & educational data:** Professional or employment related information,
  Educational information that is not publicly available.
- **Sensitive personal information** groups: Identity & demographics (Racial and ethnic origin,
  Religious or philosophical beliefs, Genetic information, Biometric information, Health
  information, Information regarding sex life, Sexual orientation), Political opinions\* (Political
  opinion), Accounts & authentication† (State ID number, Drivers' licences, Passport numbers,
  Account login information, Social security number), Location tracking† (Precise geolocation
  data, Citizenship or immigration status), Communications & financial data† (Contents of emails
  or text messages, Debit or credit card numbers combined with any security or access code), +
  custom entries.

\* GDPR-gated (EU/EEA = Yes) † CCPA-gated: **visible once California = Yes alone** — independent
of the deeper `thresholds = Yes OR include-clauses = Yes` condition that gates full CCPA *content*
elsewhere in the wizard (Disclosure of data step, generated policy CCPA section — see the
toggle-chain note above). Confirmed live 2026-07-23 (Plan Gates re-sweep,
`ai-context/plan-gates-ppg-resweep-progress.md`): the plan-tier lock is a separate, additional
layer on top of that baseline visibility, not the same condition as content-gating. The default
(non-GDPR, non-CCPA) categories always show; the GDPR and CCPA groups/chips only appear once their
respective visibility condition is met, independently of each other. On Free/Basic, these CCPA
chip groups render locked (padlock icon + amber Pro+/crown badge, remaining clickable without
selecting, inline toast "CCPA/CPRA-related clauses are available on the Pro plan and above."). On
Pro/Ultimate, CCPA-specific chips render as fully normal, unlocked, selectable chips — no lock
icon, no Pro+ badge (see Plan gating patterns).

**Custom data entries** (both Personal and Sensitive sections): accept up to 500 characters,
trim leading/trailing whitespace, reject exact duplicates and empty input, and can be removed
individually without affecting other entries.

**Validation:** leaving both Personal and Sensitive information without at least one selection
blocks progression to Use of data with the page-level "Please make sure that all fields are
completely filled out before we continue with the process." banner — confirmed this is a genuine
blocker (not the unrelated persistent-banner defect on Additional information, below) by selecting
one chip and confirming Next then proceeds. Once both Personal information and Additional
information are complete, "Collection of data" shows a completed checkmark in the sidebar, and its
Personal Information sub-tab remains independently reachable with prior selections retained.

### 3b. Additional Information

A linear Q&A list, structurally distinct from Personal Information's chip-grid:

- **Do you use cookies or other tracking technologies?** (Yes/No) — Yes reveals "Add link to your
  cookie policy" (placeholder "www.yourwebsite.com/cookie-policy") with a helper link to create a
  cookie policy if one doesn't exist. Enforces a 2000-character limit at submit time via "Please
  limit your response to 2000 characters." — the internal spec doc states a stale 500-character
  limit; live has already shipped the higher limit (same pattern as the sell/share categories
  fields in Business Details above).
- **How do you respond to 'Do Not Track' requests?** (free-text, always shown). Enforces a
  2500-character limit at submit time via "Please limit your response to 2500 characters." — the
  internal spec doc states a stale 2000-character limit.
- **Do you collect information about users below the age of 16?** (Yes/No) — **GDPR-gated**,
  only appears when EU/EEA = Yes. Confirmed absent with EU/EEA=No and present with EU/EEA=Yes,
  both directions.
- **What are the legal bases for collecting the data?** (chip-select: Consent, Performing
  contractual obligations, Legal obligations, Public task, Legitimate interest of the controller,
  Vital interest) — **also GDPR-gated identically to the under-16 question**, confirmed both
  directions live.
  - Selecting "Public task" or "Legitimate interest of the controller" reveals a mandatory,
    2000-character-limited justification field with its own icon-only "Confirm"/"Remove" buttons
    (not literal text labels — a doc/manual-test mismatch corrected via live verification).
    Deselecting the chip hides its justification field again.
- **Do you collect information about users below the age of 13?** — **CCPA-gated** (thresholds =
  Yes OR include-clauses = Yes, Pro+), independent trigger from the GDPR under-16 question above.
- **Do you have a process that allows users to review and request changes to their information?**
  (Yes/No) — **CalOPPA-gated**, shown when sell/share = Yes; Yes reveals a free-text description
  field ("Describe how users can review or update their data.") that enforces a 2500-character
  limit at submit time via "Please limit your response to 2500 characters." — the internal spec
  doc states a stale 2000-character limit.
- Every visible conditional question is controlled by its own independent trigger — confirmed by
  toggling triggers individually and in combination and observing only the matching question
  appear/disappear each time.

**[APP DEFECT — confirmed, root cause unresolved]** Clicking "Next" from this tab can leave the
"Please make sure that all fields are completely filled out..." banner **stuck** even after every
visibly-required field on both Personal information and Additional information has been filled
in — reproduced reliably on a Free-plan account with every visible field answered. Root cause not
identifiable from the UI alone (possibly a hidden/required field not rendered for that plan tier,
or a stale validation flag). Flag to engineering rather than treat as a test-authoring error.

## 4. Use of Data

Thin coverage so far — one confirmed case.

- **What are the uses for the information you collect?** — multi-select chips: "To provide and
  maintain service", "To manage your account", "To perform a contract with us", "To contact the
  user", "To send marketing and promotional communications", "To comply with legal obligations for
  targeted advertising", "To manage user requests related to business transfers...", "To evaluate
  and improve our products/services", "To examine the usage trends" — plus a free-text "Add" for a
  custom purpose (Add is disabled until text is entered).
- No plan-gating or conditional-visibility behavior has been observed on this step yet — not yet
  confirmed either way, just not seen.

## 5. Disclosure of Data

**Only appears in the wizard sidebar when its trigger condition is met** — see the Business
Details toggle-chain table above (`sell/share = Yes OR thresholds = Yes OR include-clauses =
Yes`). Not present at all by default.

Fields, once visible:
- **Do you sell or share the personal information of users in the following categories?** —
  options "Users under the age of 16 years" / "Users under the age of 13 years" / "None". The
  under-16 option reveals opt-in/opt-out free-text process fields.
- **What is the process for users to submit requests to delete, correct, or access the
  information they have shared?** (free-text).
- **Do you disclose sensitive information for purposes beyond listed exemptions?** (Yes/No, with
  a static list of 8 exemption categories).
- **Have you disclosed any of the information collected to third parties for business purposes in
  the past 12 months?** (Yes/No).

**Plan gating (Free plan):** the entire step is Pro+-gated — every field shows a "Pro+" badge,
inline "Upgrade to Pro or higher to add this clause." text, and disabled controls. Clicking
"Upgrade to Pro" opens the same shared upgrade modal used by the Business Details for-profit gate
(see Plan gating patterns).

**Open issue — not yet root-caused:** several free-text fields on this step have been observed
containing the literal string "yes" as their stored value during testing (opt-in/opt-out process
fields, sensitive-info-disclosure purposes, categories/third-parties disclosed). This is most
likely leftover dirty test data from earlier sessions on a shared test account rather than a
genuine app bug (if the *stored* value is literally "yes", the generated-policy Preview correctly
echoing "yes" is not itself a defect) — flagged for a clean-data retest to confirm one way or the
other, not asserted as confirmed either way.

## 6. Data Retention

- **How long do you retain the information you collect?** — options: "6 months", "12 months",
  "As long as it is necessary", "Add your own retention period" (reveals a free-text duration
  field), and "Not yet decided" (Pro+ — see Plan gating patterns; on Free plan this renders as a
  visibly disabled chip with no click interaction, a third distinct gating presentation from the
  other two patterns in this feature).
- Appears to be **purely plan-tier-gated, not regulation-gated** — no case here references EU/CA
  toggles at all, unlike almost every other step.

## 7. Miscellaneous Disclosures

- **Do you transfer data collected to a non-adequate country or region outside the EU?** (Yes/No)
  — **GDPR-gated**, only appears when EU/EEA = Yes. Yes reveals a safeguards chip-select
  ("Standard contractual clauses", "Binding corporate rules", "Add your own").
- **Do you automatically process the data that you have collected?** (Yes/No) — **GDPR-gated**
  identically. Answering Yes produces the generated policy's "GDPR Disclosures > Automatic
  processing of data" clause verbatim: "We use automated processing of the personal information we
  collect to personalise our services for you and others."
- **Provide the contact details of the Data Protection Officer (DPO).** (free-text) —
  **GDPR-gated**, correctly hides when EU/EEA = No.
- **Provide the details of the data controller/representative if applicable.** (free-text) —
  unlike its sibling DPO field right above it (which the source doc also claims is "Shown if:
  EU/EEA = Yes", same as this one), this field is never actually gated for visibility — it stays
  visible and editable regardless of the EU/EEA answer or any other toggle state. Its *value* only
  ever renders into the generated policy's Contact section when EU/EEA = Yes; with EU/EEA = No
  (confirmed via a hard reload, not a caching artifact) the value is not applied, with no
  indication to the user that their entry isn't being used. Confirmed tied purely to the current
  EU/EEA state, not the direction of a toggle transition — reproduced identically starting from a
  California-only state, not just an EU-then-toggled-off state. **Not treated as a defect** — the
  underlying requirement is undefined rather than broken; see "Improvements" below.
- **Do you process the personal information of 10 million or more California residents?** (Yes/No)
  — **CCPA-gated**: requires California = Yes AND (thresholds = Yes OR include-clauses = Yes).
  Yes reveals "Provide a link to the page that shows the metrics." Produces the generated policy's
  "Metrics" section, linking to the exact URL entered.
- **Do you give financial incentives in exchange for their personal information?** (Yes/No) —
  gated identically to the 10M-residents question. Produces a "Financial incentives" section in
  the generated policy.
- **At true baseline (no EU/EEA, no California CCPA-trigger), this step shows only the (buggy,
  always-visible) data-controller field** — none of DPO, transfer, automatic-processing, or either
  CCPA field render at all. Confirmed this holds even with for-profit = Yes alone (the no-op case
  above) — the CCPA fields require the actual trigger (thresholds/include-clauses), not just
  California + for-profit.
- With EU/EEA = Yes alone, all four GDPR-side fields unlock (transfer, automatic-processing, DPO,
  controller) with no CCPA fields. With the CCPA trigger met alone, both CCPA fields unlock
  alongside the always-visible controller field, with no GDPR fields. With both conditions met,
  all six fields appear together, in that order — confirmed additive with no interaction
  conflicts between the two rule sets.

## 8. Preview & Add Policy

Renders the fully-generated policy from every prior answer.

- Heading "Preview", subtext "Review your answers and generate your privacy policy.", followed
  by a fixed legal disclaimer (not app-content — boilerplate, do not treat as user-entered).
- A language control shows the current primary language (e.g. "English (Primary)") plus a
  "Language options" button.
  - With no secondary languages enabled, "Language options" shows a single menu item: "Edit
    policy".
  - With one or more secondary languages selected (Basic+), each gets its own button in the
    language row alongside the primary. Clicking a secondary-language button re-renders the
    **entire** generated policy fully translated (heading, every section heading, every fixed
    body paragraph, and the footer credit line) — user-entered free text with no fixed
    translation (e.g. categories-sold-or-shared text) stays in whatever language it was typed in.
  - On a secondary-language tab, "Language options" instead shows two items: "Edit policy" and
    "Delete language". Delete language opens a confirmation dialog ("Are you sure you want to
    remove the [language] draft of your privacy policy?", buttons "Keep version"/"Delete") —
    "Keep version" confirmed to cancel cleanly; the actual "Delete" path has not been exercised
    live (destructive, held back to avoid disrupting other in-progress test state). A rendering
    oddity was observed where the dialog's title text appeared to render twice in sequence — not
    yet confirmed via direct DOM inspection, so treat as unconfirmed rather than a settled defect.
- **Verbatim clause mapping, confirmed exact-match (not paraphrased) between wizard answers and
  generated text:**
  - Cookie policy URL → "Cookies and similar technologies" section links to the exact URL entered.
  - Do-Not-Track response text → "Do not track requests" section, verbatim.
  - Categories sold/shared + third-parties text → "Sale/sharing of information" section, verbatim,
    under fixed lead-in sentences.
  - Review/update-process description → "Review and change information" section, verbatim.
  - CCPA metrics URL → "Metrics" section, linking to the exact URL.
- **"Do we share your information?" — GDPR-only section, previously undocumented.** Renders only
  when EU/EEA = Yes, with three fixed sharing-basis bullets: "Sharing with your consent:",
  "Legal Obligations:", "For business transfers:". Confirmed absent when EU/EEA = No.
- **Children's privacy clauses — two distinct, independently-triggered structures:**
  - The standalone GDPR "Privacy of children" section (always renders once any policy is
    generated — presence isn't gated, only its wording is) states that data of children under 16
    is only collected/processed after verified parental/guardian consent, once the under-16
    question has been answered Yes.
  - A separate, **two-tier** CCPA "Children's privacy" subsection inside "CCPA disclosures" (gated
    by CCPA applicability): ages 13–16 require the user's own explicit consent; under 13 requires
    parental/legal-guardian consent — this is not documented in either internal source doc, found
    via a footnote cross-reference and confirmed live.
- **[APP DEFECT — confirmed pattern, PM confirmation pending on intended-vs-bug]** Toggling an
  answer back to "No" can leave that answer's prior "Yes"-state content **stale** in the generated
  Preview instead of reverting or removing it. Two confirmed instances:
  - The "Privacy of children" clause keeps showing its parental-consent wording after the under-16
    question is cleared (by setting EU/EEA = No, which removes the question from the wizard) —
    the baseline (never-answered) state correctly shows the default no-consent-required wording,
    and answering under-16 = Yes correctly switches it, but clearing the answer afterward doesn't
    revert it.
  - The "Sale/sharing of information in the past 12 months" section renders **simultaneously**
    with its sibling "Sale/sharing of information" section (which correctly states "We do not sell
    or share...") even when sell/share is currently set to No — reconfirmed at every regulatory
    state tested. The section's presence, independent of whatever text is inside it, is the
    defect.
- Bottom action bar shows "Previous", "Save draft", "Generate privacy policy" (not "Publish" or
  "Add policy" — those labels belong to the post-generation state below).

### Post-generation: adding the policy to the site

Exercised once, end-to-end, on a disposable test account/site specifically because this action is
irreversible:

1. **"Generate privacy policy"** navigates to the generated-policy view: a dismissible success
   banner ("Your privacy policy has been generated successfully."), a version label ("Version:
   V1.0 (<date>)") with a "Version history" link, the same legal disclaimer, and the same
   language control/content as Preview. The wizard's bottom action bar is replaced by a single
   "Add policy to site" button.
2. **"Add policy to site"** opens a method-selection modal ("Add privacy policy to your website")
   with two options: "Code snippet" ("Automatically update your privacy policy each time you
   modify the generated policy.") and "HTML format" ("Manually update the code on your site each
   time you modify the generated policy."). "Complete generation" starts disabled.
3. Selecting **"Code snippet"** (confirmed — must be actively clicked even though it appears
   visually pre-highlighted as default; the visual highlight alone does not enable "Complete
   generation") reveals a two-step install block: a read-only JavaScript snippet wrapped in HTML
   comments, "Copy code" / "Send code to a teammate" buttons, then instructions to paste it into
   the site. "Complete generation" becomes enabled. (The "HTML format" path has not been exercised
   live.)
4. **"Complete generation"** opens a second dialog, "Policy installed?": "You have generated a
   completed privacy policy for your website <site>. Have you installed the policy code to your
   website yet?" with "Yes, I have installed" and "Install code" (the latter not exercised live).
5. **"Yes, I have installed"** closes both dialogs, returning to the generated-policy view with
   "Add policy to site" now replaced by a code-icon button and a "Publish changes" button
   (disabled, since no further edits have been made yet). This is the wizard's true terminal
   happy-path state.

**Not yet exercised at all:** the post-generation editing surface — Version history, the
generated-policy Options menu, and "Publish changes" itself (republishing after an edit) are a
distinct feature surface from everything above and remain undocumented.

## Plan gating patterns

Three visually distinct gating presentations coexist in this one feature — do not assume they're
interchangeable when reading a case or filing a bug:

1. **Disabled control + upgrade modal** (Business Details "for-profit organisation?", the entire
   Disclosure of data step). The control itself renders disabled with a "Pro+" badge and inline
   upgrade text; clicking the upgrade CTA opens a modal with a bulleted feature list, a single Pro
   plan card, and "Get started with Pro plan" / "Continue with limited policy" / "Close". This
   same modal is shared byte-identical across both of these gates. Clicking "Next" with only this
   locked field remaining also surfaces the same modal (but only when it's the *sole* remaining
   gap — if another required field is also incomplete, the generic "fields not completely filled
   out" banner shows instead).
2. **Clickable-but-locked chip + inline toast** (CCPA-gated data-category chips on Collection of
   data > Personal information, Free/Basic plan — confirmed identical on both tiers via the
   2026-07-23 Plan Gates re-sweep). The chip renders visually locked — greyed label, lock icon,
   amber Pro+ badge — but remains natively clickable; clicking it doesn't select it but surfaces
   an inline toast below it: "CCPA/CPRA-related clauses are available on the Pro plan and above."
   with an "Upgrade now" link.
3. **Visibly-disabled chip, no interaction** (Data retention's "Not yet decided" option, Free
   plan). Renders disabled up front with an inline "Pro+" label directly on the chip — no click
   response, no toast, no modal.

The Basic+ multi-language gate (Language preferences) uses a variant of pattern 1's modal but with
**two** plan cards (Basic $10/mo and Pro $25/mo, Pro labeled "Recommended") instead of one, and
different button labels ("Get started with Basic plan" / "Get started with Pro plan" / "Continue
without multi-lingual privacy policy").

Full plan-by-plan matrix: [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md).

## Known open issues (consolidated)

- **"Back to Dashboard" > Discard reverts the entire draft**, not just the current step's unsaved
  edit — see Wizard shell above.
- **Persistent "fields not completely filled out" banner** on Additional information that doesn't
  clear even once every visible required field is filled — root cause unresolved.
- **Stale content survives a toggle flip to "No"** in the generated Preview — two confirmed
  instances (Privacy of children clause, Sale/sharing-in-past-12-months section) — pending PM
  confirmation on intended-vs-defect.
- **"yes"-placeholder values** in several Disclosure of data free-text fields — likely dirty test
  data rather than a templating bug; not yet isolated either way.
- **Delete-language dialog title possibly rendering twice** — seen once via accessibility-tree
  snapshot, not yet confirmed via direct DOM inspection.
- **for-profit = Yes alone is a confirmed no-op**, not a defect — documented above because it was
  an open question, now resolved (not a bug report item).

## Improvements (product decision needed, not a defect)

Behavior that works as currently implemented but reflects an undefined requirement rather than a
broken one — worth product/PM input, not an app defect to fix blindly.

- **Data controller/representative field's EU/EEA gating is undefined.** The field (Miscellaneous
  disclosures) stays visible and editable regardless of the EU/EEA answer, unlike its sibling DPO
  field (which correctly hides on EU/EEA = No, per the source doc's "Shown if: EU/EEA = Yes" rule
  stated for both fields identically). Its value only renders into the generated policy's Contact
  section when EU/EEA = Yes; with EU/EEA = No, the field remains visible and editable but its value
  is not applied, with no UI indication that the entry no longer counts. Two possible intended
  behaviors, and nothing currently establishes which one is correct:
  1. Hide the field entirely on EU/EEA = No, matching DPO's behavior exactly — treating
     "controller/representative" as a strictly GDPR-scoped concept, same as DPO.
  2. Keep the field visible regardless of EU/EEA state, and always include its value in the
     generated policy's Contact section when filled in — treating it as a general-purpose contact
     field that isn't GDPR-specific.
  Needs a product decision on which of these is the intended requirement before this becomes a
  regression case either way.

## Related pages

- [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) — full plan-gating
  CTA/tooltip matrix for every locked control referenced above.

## Source

Derived from `ai-context/cases-privacy-policy-generator.json` (84 TestRail cases as of
2026-07-16, plus 7 unpublished draft cases in `ai-context/draft-privacy-policy-generator.json` as
of 2026-07-17). Most of the wizard has been live-verified across at least a Free and a Pro/Ultimate
account; **Use of Data and Data Retention are thin** (1–3 cases each) and have not been swept for
regulatory or plan-tier gating the way every other step has. The post-generation Add-to-site flow
was verified once, end-to-end, on a disposable account. Not yet touched at all: the "HTML format"
add-to-site method, the "Install code" alternate confirmation path, and the post-generation
editing surface (Version history, Options menu, Publish changes).

A character-limit audit (2026-07-17, tracked in `BACKLOG.md`) swept Company Details, Collection of
Data, and Use of Data for the same stale-doc-current-column pattern already seen elsewhere in this
feature. Three new mismatches were found (cookie policy URL, DNT response, review/change-process
description — all documented above); everything else in those three steps either already matched
the doc or was already flagged in a prior pass.
