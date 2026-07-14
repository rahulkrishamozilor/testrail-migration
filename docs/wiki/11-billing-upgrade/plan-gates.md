# Billing & Upgrade — Plan Gates

**Nav path:** Billing & Upgrade > Plan Gates
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner only manages billing/subscription; Admin and Editor can generally still USE gated features per their plan tier, they just can't change the plan — see docs/wiki/14-permissions.md
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

The single case on file so far exercises the **Cookie Banner > Layout tab (or General tab)
Consent Template selector**, not a dedicated "Plan Gates" page UI. No distinct Plan Gates page
layout (e.g. a settings page listing all gates at once) is described in the source case — the
one case that exists is a Layer-1-shaped functional check for the Consent Template dropdown,
filed under this section per the "Plan Gates" TestRail placement.

- **Consent Template dropdown** — opened from the Layout tab (or the General tab, where the
  Consent Template selector is also visible). Lists three options: **GDPR**, **US State Laws**,
  **GDPR & US State Laws**.

## Workflows

1. **Attempt to select "GDPR & US State Laws" on a Free or Basic plan**
   - **Precondition:** account is on a Free or Basic plan; the Consent Template is currently set
     to GDPR or US State Laws.
   1. Click the Consent Template dropdown to open the template switcher. A dropdown appears
      listing GDPR, US State Laws, and GDPR & US State Laws.
   2. Click the "GDPR & US State Laws" option. An upgrade nudge appears. The active consent
      template does **not** change — it remains at its previous value, and no banner preview
      update occurs.
   3. Verify the nudge content and CTA: the nudge states that GDPR & US State Laws requires a
      higher-tier plan, and an upgrade CTA button is visible.

This confirms, for this one control: on Free/Basic, "GDPR & US State Laws" is gated, selecting
it is a no-op on the underlying setting, and it surfaces a nudge with an upgrade CTA rather than
silently failing or partially applying.

## Validation & edge cases

Full per-plan gate matrix (Free/Basic/Pro/Ultimate) is NOT YET covered — only 1 TestRail case
exists for this section as of 2026-07-14. Needs a live-crawl pass logging into each plan tier
from `qa-accounts.json` (free/basic/pro/ultimate accounts) to build out the complete matrix of
which features are gated at which tier and what nudge each shows.

Specifically still unknown and NOT to be guessed:
- Whether Pro and Ultimate both unlock "GDPR & US State Laws" on this control, or only one of
  them (the case only confirms Free/Basic are gated).
- Exact nudge headline/body copy and CTA label for this control (the case describes the nudge's
  required content — "requires a higher-tier plan" + upgrade CTA — but does not quote verbatim
  copy).
- Whether the CTA destination differs between Free and Basic (elsewhere in the wiki, e.g.
  `04-cookie-banner/general.md`, Free-tier CTAs are documented as "Try Pro for free" and
  Basic-tier as "Upgrade now" for other gated controls — not yet confirmed for this specific
  Consent Template nudge).
- Every other gated touchpoint in the app outside this one Consent Template control (Colours,
  Custom CSS, Languages, Cookie List/Categories, Scan & Scan History, Organisations & Sites site
  management, etc.) — those pages currently document their own gating locally with a forward
  link to this page, but the authoritative matrix does not exist here yet.

## Related pages

This page is meant to be linked FROM every other feature page that has a plan-gated element,
including:
- `docs/wiki/04-cookie-banner/general.md`
- `docs/wiki/04-cookie-banner/colours.md`
- `docs/wiki/04-cookie-banner/custom-css.md`
- `docs/wiki/04-cookie-banner/languages.md` (if/when written)
- `docs/wiki/05-cookie-manager/cookie-list-categories.md` (if/when written)
- `docs/wiki/05-cookie-manager/scan-and-scan-history.md` (if/when written)
- `docs/wiki/organisations-and-sites/site-management.md` (if/when written)

Those pages should describe *that* a control is gated and note the observed behavior for the
plan tiers their own source cases cover, then link here rather than re-deriving the full matrix.

## Source

Derived from `ai-context/cases-plan-gates-new.json` (1 TestRail case — thin, flagged for a
live-crawl follow-up pass across all plan tiers). Drafted 2026-07-14, not yet live-verified
against the QA app.
