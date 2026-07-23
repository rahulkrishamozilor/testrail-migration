# Billing & Upgrade — Plan Gates

**Nav path:** Billing & Upgrade > Plan Gates
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner only manages billing/subscription; Admin and Editor can generally still USE gated features per their plan tier, they just can't change the plan — see docs/wiki/permissions.md
**Plan gating:** This page IS the plan-gating reference for the whole app.

## Purpose

Plan-gated features across CookieYes follow a two-layer test model (per `testrail-suite-v2.md`,
"Plan-gated features"):

- **Layer 1 — Functional cases, live in each feature section.** Each feature section (Cookie
  Banner > General, Colours, Custom CSS, etc.) tests only that its own locked entry point (icon,
  dropdown option, toggle) correctly opens an upgrade nudge for the plan tiers it's gated on.
  The feature section does not re-test the nudge or CTA button behavior itself — it just asserts
  "clicking this locked control opens a nudge" and points here for the rest.
- **Layer 2 — Plan Gates, this section.** Asserts that each plan tier is correctly configured
  across *all* gated touchpoints in the app, one case per plan, walking through every gated
  control on every page. These cases are tagged `smoke` and are automation candidates — the
  Playwright test gives per-gate assertion granularity, and the TestRail case is the coverage
  marker.

This page is therefore meant to be the answer to "what is gated at which plan, and what happens
when a user without that plan tries to use it" for the entire app — every feature page with a
plan-gated element links here instead of duplicating the matrix locally.

## Page structure

This section does not own a dedicated "Plan Gates" settings page in the app UI — there is no
single screen listing every gate at once. Instead, this wiki section aggregates the **Layer 2**
consolidated per-plan walkthroughs described in Purpose above. Individual gated controls (a
locked dropdown option, a disabled field, a premium icon) live and render inside their own
feature pages (Cookie Banner, Cookie Manager, Advanced Settings, Languages, Organisations &
Sites, Cookie Policy Generator, etc.) — those pages describe the control itself and link here
for the full per-tier verification, rather than this page describing controls it doesn't render.

As of the most recent gate sweep, one feature area has a complete Layer 2 matrix: the **Privacy
Policy Generator** wizard, verified across Free, Basic, and Pro/Ultimate plans. See Workflows
below.

## Workflows

**Privacy Policy Generator — full plan-gate matrix (Free / Basic / Pro & Ultimate)**

Six touchpoints inside the Privacy Policy Generator wizard are plan-gated, all at the same
"Pro+" tier boundary (Basic does not unlock any of them — only Pro and above do), with Pro and
Ultimate confirmed behaviorally identical across every touchpoint:

1. **Multi-language generation** — the secondary-language buttons (French, German, Italian,
   Spanish) on the Language preferences step. Locked on Free and Basic with an "Upgrade to
   Basic" button; a dialog opens comparing a Basic plan card ($10/mo) and a Pro plan card
   ($25/mo, marked "Recommended"), each with a feature-gap list (CCPA/CPRA clauses,
   multi-language, auto-translation) and its own "Get started with Basic/Pro plan" button, plus
   "Continue without multi-lingual privacy policy" and "Close". Fully enabled on Pro/Ultimate.
2. **"Are you a 'for-profit' organisation?"** (Business details, shown after answering "Do you
   have users in California?" = Yes) — disabled with a "Pro+" badge and inline "Upgrade to Pro or
   higher..." text on Free and Basic (identical on both — Basic does not unlock this). Clicking
   its upgrade prompt opens a single-Pro-plan-card dialog ("Get started with Pro plan" /
   "Continue with limited policy" / "Close"). Fully enabled with no badge on Pro/Ultimate, and
   answering it unlocks a downstream "thresholds" question that in turn unlocks full CCPA
   content.
3. **Advancing past the wizard with the for-profit question unanswered** — clicking "Next" with
   every other required field filled but the locked for-profit question still open reopens the
   same upgrade dialog; "Continue with limited policy" advances to Collection of data leaving it
   unanswered. On Pro/Ultimate this never triggers — nothing is locked.
4. **CCPA-gated data-category chips** (Collection of data > Personal information, e.g.
   "Birthday") — render visually locked (greyed label, lock icon, amber "Pro+"/crown badge) but
   remain clickable without selecting on Free and Basic, surfacing an inline toast:
   "CCPA/CPRA-related clauses are available on the Pro plan and above." with an "Upgrade now"
   link. Fully selectable with a plain checkmark icon, no badge, on Pro/Ultimate.
5. **Disclosure of data step** (after setting "Do you sell or share the personal information of
   users?" = Yes) — all four field groups (sell/share categories, delete/correct/access process,
   sensitive-info disclosure, third-party disclosure) show a "Pro+" badge with disabled controls
   and an "Upgrade to Pro" prompt on Free and Basic. Fully enabled with no badges on Pro/Ultimate.
6. **Data retention step's "Not yet decided" option** — renders as a visibly disabled chip with
   an inline "Pro+" label on Free and Basic, with no click interaction available (no toast, no
   modal). Renders as a plain enabled button on Pro/Ultimate.

## Validation & edge cases

The Privacy Policy Generator matrix above is the only feature area in the app with a complete,
live-verified Layer 2 walkthrough as of the most recent sweep — confirmed with zero defects
across all four plan tiers, and Basic confirmed equivalent to Free, Pro confirmed equivalent to
Ultimate, for every one of its six touchpoints.

Every other feature section with a plan-gated control (Cookie Banner's Consent Template
dropdown and Geo-target banner/IAB TCF upgrade icons, Colours, Custom CSS, Languages, Cookie
Manager's Schedule Scan card, Advanced Settings' banner-page/Static IP/subdomain gates,
Organisations & Sites' Add staging site option, Cookie Policy Generator's own paywall flow, etc.)
still only has a scattered **Layer 1** touchpoint case documenting its own locked control and
linking here — none of those has a consolidated Layer 2 walkthrough case yet. Whether each of
those gates independently at the same tier boundaries the Privacy Policy Generator matrix found,
or differs, is not yet confirmed for any of them.

## Known gaps

- No consolidated Layer 2 walkthrough exists yet for any feature section besides Privacy Policy
  Generator — see Validation & edge cases above for the full list of sections still only backed
  by scattered Layer 1 touchpoint cases.
- `docs/wiki/permissions.md`, linked from the Roles line above, does not exist yet.

## Related pages

This page is meant to be linked FROM every other feature page that has a plan-gated element,
including:
- `docs/wiki/cookie-banner/general.md`
- `docs/wiki/cookie-banner/colours.md`
- `docs/wiki/cookie-banner/custom-css.md`
- `docs/wiki/cookie-banner/languages.md` (if/when written)
- `docs/wiki/cookie-manager/cookie-list-categories.md` (if/when written)
- `docs/wiki/cookie-manager/scan-and-scan-history.md` (if/when written)
- `docs/wiki/advanced-settings.md`
- `docs/wiki/legal-policies/privacy-policy-generator.md`
- `docs/wiki/profile-account/organisations-and-sites/site-management.md`

Those pages should describe *that* a control is gated and note the observed behavior for the
plan tiers their own source cases cover, then link here rather than re-deriving the full matrix.

## Source

The Privacy Policy Generator matrix (Workflows section above) is derived from three consolidated
Layer 2 cases in `cases-privacy-policy-generator.json`, authored and live-verified 2026-07-23
across Free, Basic, Pro, and Ultimate plans. No standalone case file exists for this section as a
whole — Layer 1 touchpoint cases for other features remain in their own feature-section case
files (`cases-cookie-banner-general.json`, `cases-advanced-settings.json`,
`cases-cookie-manager.json`, `cases-languages.json`, `cases-organisation-and-sites.json`,
`cases-cookie-policy-generator.json`), each linking back to this page rather than being
duplicated here.
