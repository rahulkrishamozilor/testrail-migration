# Plan Gates + nudge behaviour re-sweep — Privacy Policy Generator

**Status: COMPLETE (2026-07-23).** Recommendation approved and authored — 3 feature-scoped
Layer 2 cases published to `11. Billing & Upgrade > Plan Gates`: cases 39738 (Free plan), 39739
(Basic plan), 39740 (Pro plan, precondition covers Pro or Ultimate since the sweep found no
behavioral difference between those two tiers). See `coverage-gaps.md`'s "Layer 2 Plan Gates
cases missing for this feature" entry for the closure note and the still-open suite-wide
question this doesn't resolve. Rest of this file kept as-is for historical context on the sweep
itself.

Full live re-sweep across Free / Basic / Pro / Ultimate for all 6 known PPG plan-gated
touchpoints (existing cases 39493-39498, all currently Free-plan-only) plus nudge button
destinations. Requested to verify BACKLOG.md's "Plan Gates — Layer 2 suite-wide check" item
for PPG specifically, and to close the Basic/Pro/Ultimate coverage gap.

## Touchpoints being swept

1. Multi-language gate (Language preferences) — Basic+ gated
2. "for-profit organisation" question (Business details, needs California=Yes) — Pro+ gated
3. Next-with-locked-field modal (same precondition as #2) — Pro+ gated
4. CCPA-gated data-category chips (Collection of data > Personal information) — Pro+ gated,
   reachability precondition TBD (thresholds itself is Pro+-gated — need to verify whether
   Free/Basic can even see the chips, since case 39496 says Free plan shows them locked)
5. Disclosure of data step (needs sell/share=Yes) — entirely Pro+ gated
6. "Not yet decided" retention option (Data retention step) — Pro+ gated (disabled chip)

## Accounts

- Free: rahulkrishna+freeplansite@mozilor.com — site hd.com
- Basic: rahulkrishna+basicuser@mozilor.com — site TBD
- Pro: jacksnickel+protest@gmail.com — site hi.com
- Ultimate: jacksnickel+ultimatetest@gmail.com — site TBD

## Findings log

(filled in as swept)

### Free plan

- **Touchpoint 1 (multi-language gate): CONFIRMED matches case 39493.** Secondary-language
  buttons disabled, "Upgrade to Basic" button shown. Clicking it opens a modal titled "Your
  Privacy Policy is incomplete" listing CCPA/CPRA clauses, multi-language, and auto-translation
  as missing features, with "Get started with Basic plan" / "Get started with Pro plan" /
  "Continue without multi-lingual privacy policy" / Close options. Matches spec.
- **Touchpoint 2 (for-profit question): CONFIRMED matches case 39494.** With California=Yes,
  question shows Pro+ badge, "Upgrade to Pro" button, both Yes/No disabled. Clicking "Upgrade to
  Pro" opens a Pro-only modal (not Basic/Pro comparison — makes sense, Basic doesn't unlock this)
  titled "Your Privacy Policy is incomplete" listing CCPA/CPRA clauses, multi-language,
  auto-translation, with "Get started with Pro plan" / "Continue with limited policy" / Close.
- **Touchpoint 3 (Next-with-locked-field modal): CONFIRMED matches case 39495.** Clicking Next
  with for-profit unanswered (all other fields on the tab filled, including the two sell/share
  free-text follow-ups) surfaces the identical modal to touchpoint 2. "Continue with limited
  policy" correctly proceeds to Collection of data.
- **Touchpoint 4 (CCPA-gated data-category chips): CONFIRMED matches case 39496.** With
  California=Yes (for-profit still unanswered — thresholds unreachable), the CCPA-gated groups
  ("Accounts & authentication", "Location tracking", "Communications & financial data") ARE
  visible on Personal information with a padlock icon + orange crown "Pro+" badge on each chip
  (screenshot-verified). **Resolves the earlier open question from the wiki doc/business-details
  sweep**: visibility of these chip groups is gated on California=Yes alone, NOT on the deeper
  thresholds=Yes condition — the plan-tier lock is a separate, additional visual layer on top.
  Clicking a locked chip (e.g. "State ID number") shows an inline toast: "CCPA/CPRA-related
  clauses are available on the Pro plan and above." + "Upgrade now" button. Chip does not
  toggle selected.
- **Touchpoint 5 (Disclosure of data step): CONFIRMED matches case 39497.** With sell/share=Yes
  (step visible in sidebar), all 4 field groups ("sell/share in these categories", "process for
  delete/correct/access requests", "disclose sensitive info beyond exemptions", "disclosed to
  third parties in past 12mo") show a Pro+ badge, disabled controls, and their own "Upgrade to
  Pro" button/text ("... or higher to add this clause").
- **Touchpoint 6 ("Not yet decided" retention): CONFIRMED matches case 39498.** Chip renders
  disabled with a "Pro+" badge; other retention options (6 months / 12 months / as long as
  necessary / custom period) are fully enabled.

**Free plan: all 6 touchpoints confirmed correct, no defects found.**

### Basic plan

- **Touchpoint 1 (multi-language gate): CONFIRMED unlocked as expected.** After selecting a
  primary language, the "Generate policy in multiple languages" secondary-language buttons
  (Français, Deutsch, Italiano, Español) are fully enabled — no Basic+ badge, no upgrade prompt.
  (Note: the *primary* language selector at the top is always enabled for every plan — the gate
  only applies to the secondary "Generate policy in multiple languages" section below it, which
  only renders after a primary language is picked.)
- **Touchpoint 2 (for-profit question): CONFIRMED still Pro+-locked, as expected** (Basic does
  not unlock Pro+ features). Same Pro-only "Your Privacy Policy is incomplete" modal as Free
  plan (Get started with Pro plan / Continue with limited policy / Close).
- **Touchpoint 3 (Next-with-locked-field modal): CONFIRMED identical to Free plan.**
- **Touchpoint 4 (CCPA-gated chips): CONFIRMED identical to Free plan** — locked chips
  (padlock + crown "Pro+" badge), clicking one shows the same "CCPA/CPRA-related clauses are
  available on the Pro plan and above." + "Upgrade now" toast. Matches the existing
  coverage-gaps.md note that Basic ≡ Free for every CCPA touchpoint in Collection of Data.
- **Touchpoint 5 (Disclosure of data step): CONFIRMED identical to Free plan** — all 4 field
  groups Pro+-gated with disabled controls and "Upgrade to Pro" prompts.
- **Touchpoint 6 ("Not yet decided" retention): CONFIRMED identical to Free plan** — disabled
  chip with Pro+ badge.

**Basic plan: all 6 touchpoints confirmed correct, no defects found. Basic behaves identically
to Free for every Pro+-gated touchpoint (expected, since Basic doesn't unlock Pro+ features) —
the only touchpoint where Basic differs from Free is touchpoint 1 (Basic+ gate), which is
correctly unlocked.**

### Pro plan

- **Touchpoint 1 (multi-language gate): CONFIRMED unlocked.** Secondary-language buttons fully
  enabled, no badge/prompt.
- **Touchpoint 2/3 (for-profit question + Next-modal): CONFIRMED unlocked.** With
  California=Yes, "Are you a for-profit organisation?" shows no Pro+ badge, both Yes/No enabled.
  Setting for-profit=Yes correctly reveals the "thresholds" question (also unlocked); setting
  thresholds=Yes correctly unlocks full CCPA content downstream (confirms `for-profit=Yes AND
  thresholds=Yes` is reachable and functions as expected on Pro). Clicking Next with everything
  answered advanced straight to Collection of data with **no upgrade modal at all** — correct,
  since nothing was locked/unanswered this time.
- **Touchpoint 4 (CCPA-gated chips): CONFIRMED unlocked.** Screenshot-verified: chips render as
  fully normal (checkmark icon, no padlock, no crown/Pro+ badge) — matches the wiki doc's
  existing claim exactly ("CCPA-specific chips render as fully normal, unlocked, selectable
  chips — no lock icon, no Pro+ badge").
- **Touchpoint 5 (Disclosure of data step): CONFIRMED unlocked.** All 4 field groups fully
  enabled, no Pro+ badges. (One field already had leftover data from a prior session on this
  shared account — expected dirty-data artifact, not a defect; confirms the field is genuinely
  editable.)
- **Touchpoint 6 ("Not yet decided" retention): CONFIRMED unlocked.** Chip enabled, no Pro+
  badge, no "disabled" attribute.

**Pro plan: all 6 touchpoints confirmed correct, no defects found.**

### Ultimate plan

- **Touchpoint 1 (multi-language gate): CONFIRMED unlocked.**
- **Touchpoint 2/3 (for-profit question + Next-modal): CONFIRMED unlocked.** No Pro+ badge;
  for-profit=Yes correctly reveals thresholds question (also unlocked); thresholds=Yes correctly
  unlocks CCPA content. Next with everything answered advanced with no modal.
- **Touchpoint 4 (CCPA-gated chips): CONFIRMED unlocked** (screenshot-verified, identical to Pro).
- **Touchpoint 5 (Disclosure of data step): CONFIRMED unlocked** — no Pro+ text anywhere on
  the page.
- **Touchpoint 6 ("Not yet decided" retention): CONFIRMED unlocked** — plain enabled button,
  no disabled attribute, no Pro+ text.

**Ultimate plan: all 6 touchpoints confirmed correct, no defects found. Ultimate behaves
identically to Pro for every touchpoint — expected, since all 6 gates are "Pro+" (Pro and
above), not Pro-exclusive.**

## Synthesis / gaps found

**Result: zero defects found across all 4 plans × 6 touchpoints (24 checks total).** Every
existing case (39493-39498) holds up exactly as written, and the previously-untested Basic/Pro/
Ultimate states behave exactly as the "Pro+" gating label promises — Basic ≡ Free for every
Pro+-gated touchpoint (only touchpoint 1's Basic+ gate differs), and Pro ≡ Ultimate for all 6.

**Two side-findings worth carrying forward (not defects, but corrections/clarifications to
existing documentation):**

1. **Resolved the CCPA-chip visibility precondition ambiguity** flagged in both the wiki doc and
   the original business-details-matrix-sweep-progress.md: the CCPA-gated chip *groups*
   ("Accounts & authentication", "Location tracking", "Communications & financial data") become
   visible once **California=Yes alone** — not the deeper `thresholds=Yes OR include-clauses=Yes`
   condition, which is unreachable on Free/Basic anyway since for-profit itself is Pro+-locked
   there. The plan-tier lock (padlock+crown, inline toast) is a separate visual/interaction layer
   applied on top of that baseline visibility. This should be corrected in the wiki doc's
   footnote at the "Sensitive personal information" section (currently reads "CCPA-gated
   (thresholds = Yes OR include-clauses = Yes, Pro+)" without distinguishing visibility from
   plan-lock).
2. Confirmed the primary-language selector (always enabled, every plan) and the secondary
   "Generate policy in multiple languages" gate (Basic+) are two distinct, separately-rendered
   sections — worth being precise about this distinction in any future case/doc wording, since
   they're easy to conflate (both list the same 5 languages).

**Recommendation for BACKLOG.md's "Plan Gates — Layer 2 suite-wide check" item, PPG-specific
part:** the 6 existing cases (39493-39498) are solid Layer-1-in-the-right-section touchpoint
verifications, now confirmed accurate for Free and (newly) implicitly correct for Basic/Pro/
Ultimate by the behavior pattern found (Basic≡Free, Pro≡Ultimate for every Pro+ gate). Rather
than authoring 18 new near-duplicate per-touchpoint cases for the other 3 plans, the cleanest
fix consistent with `testrail-suite-v2.md`'s stated Layer 2 shape is to author the **feature-
scoped consolidated cases** it specifically calls for: `[Plan Gates] Privacy Policy Generator —
Free plan`, `... — Basic plan`, `... — Pro plan` (steps walk through all 6 touchpoints per plan;
Ultimate can share the Pro plan case's precondition per the pattern found, or get its own if the
team wants explicit Ultimate coverage). This closes the doc-mandated Layer 2 shape gap without
throwing away the existing granular cases. **Not authored — awaiting user approval per
CLAUDE.md's "cases are never created without explicit user approval."**
