# CookieYes App Wiki

An LLM-readable knowledge base of the CookieYes web app — one page per feature area, each
self-contained (newcomer test / isolation test / RAG accuracy test, per
`migration-conventions.md` §0). Structure mirrors the 17-section app map in
`testrail-suite-v2.md` (read that file for the canonical section tree). See `CONVENTIONS.md` for
this knowledge base's own writing standard (perspective, no inline case-ID references, page
skeleton, etc.) — a separate concern from `migration-conventions.md`, which governs TestRail case
authoring, not wiki page authoring.

**Coverage as of 2026-07-23:** 26 pages drafted from the existing `ai-context/cases-*.json`
TestRail export files. Most of these have not been live-verified against the running QA app yet —
each page's own **Source** section says so explicitly where that's still true. The
[Privacy Policy Generator](legal-policies/privacy-policy-generator.md) page is the first
exception: most of its wizard has been live-verified across a Free and a Pro/Ultimate account. The
[Dashboard](dashboard.md) page (added 2026-07-23 via `/wiki-sync`) is partially live-verified —
about 20 of its 88 backing cases, concentrated on empty/default states. The
[Plan Gates](billing-upgrade/plan-gates.md) page was corrected 2026-07-23 via `/wiki-sync`: its
prior source citation (`cases-plan-gates-new.json`) pointed to a file that doesn't exist, and its
one-case description was stale — it now documents Privacy Policy Generator's fully live-verified
Free/Basic/Pro/Ultimate gate matrix, the only complete Layer 2 walkthrough in the app so far. The
[Permissions](permissions.md) page (added 2026-07-23 via `/wiki-sync`) is new — it did not
exist before this pass, despite 13 already-verified permission-divergence cases sitting unused
across three other sections' case files. The [My Account](profile-account/my-account.md) page
(added 2026-07-23 via `/wiki-sync`) is also new; it surfaced a confirmed, reproducible defect in
the Change password flow (see the page's Known gaps) that had no prior documentation anywhere.
Roughly half the app's sections have **no page yet at all** (see "Not yet documented" below)
because no TestRail case data exists for them — they need a first live-crawl pass through
`qa-accounts.json`, which was deliberately deferred rather than run automatically. See the plan at
the bottom of this file for what that follow-up pass would cover.

---

## 01. Authentication

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Sign Up — Core](authentication/signup-core.md) | `cases-signup-core.json` | 17 | Drafted 2026-07-14, not live-verified |
| [Sign Up — Standard (Free)](authentication/signup-standard-free.md) | `cases-signup-standard-free.json` | 3 (thin) | Drafted 2026-07-14, not live-verified |
| [Log In](authentication/login.md) | `cases-login.json` | 10 | Drafted 2026-07-14, not live-verified |
| [Password Reset](authentication/password-reset.md) | `cases-forgot-password.json` | 21 | Drafted 2026-07-14, not live-verified |

Not yet documented: Sign Up > Trial without card, Trial with card (Checkout), Agency.

## 02. Onboarding

Not yet documented: Banner Setup, Banner Installation — no case file exists yet.

## 03. Dashboard

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Dashboard](dashboard.md) | 9 files: `cases-dashboard-header.json`, `-alert-banners.json`, `-cookie-banner-status-card.json`, `-cookie-summary-card.json`, `-consent-trends-card.json`, `-pageviews-card.json`, `-recent-consent-logs-card.json`, `-add-a-new-site.json`, `-states.json` | 88 (published outside this repo's pipeline; `grill_status: not-tracked-by-repo`) | Drafted 2026-07-23; ~20 of 88 cases live-verified via `/wiki-sync` (empty/default states only) — see page's Known gaps |

Not yet documented within this section: most of the Add a New Site creation flow, Active/verified
banner and card states, paid-plan variants, populated chart/log states — see the page's own Known
gaps section.

## 04. Cookie Banner

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Display & Layout (page shell)](cookie-banner/display-layout.md) | single case in `cases-general.json` (older draft) | 1 (largely incomplete) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — General](cookie-banner/general.md) | `cases-cookie-banner-general.json` | 26 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Layout](cookie-banner/layout.md) | `cases-cookie-banner-layout.json` | 23 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Content (GDPR)](cookie-banner/content-gdpr.md) | `cases-cookie-banner-content.json` | 22 of 31 (11 shared with US State Laws) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Content (US State Laws)](cookie-banner/content-us-state-laws.md) | `cases-cookie-banner-content.json` | 20 of 31 (11 shared with GDPR) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Colours](cookie-banner/colours.md) | `cases-colours.json` | 12 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Custom CSS](cookie-banner/custom-css.md) | `cases-custom-css.json` | 5 (thin) | Drafted 2026-07-14, not live-verified |

Not yet documented within this section: Device Preview, Publishing (also flagged as gaps inside
`display-layout.md`) — no case file exists yet.

## 05. Cookie Manager

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Cookie List & Categories](cookie-manager/cookie-list-categories.md) | `cases-cookie-manager.json` | 6 of 34 | Drafted 2026-07-14, not live-verified |
| [Scan & Scan History](cookie-manager/scan-and-scan-history.md) | `cases-cookie-manager.json` | 23 of 34 | Drafted 2026-07-14, not live-verified |
| [Edit & Add Cookies](cookie-manager/edit-add-cookies.md) | `cases-cookie-manager.json` | 5 of 34 | Drafted 2026-07-14, not live-verified |

## 06. Consent Log

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Consent Log](consent-log.md) | `cases-consent-log.json` | 23 | Drafted 2026-07-14, not live-verified |

## 07. Languages

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Languages](languages.md) | `cases-languages.json` | 23 | Drafted 2026-07-14, not live-verified |

## 08. Advanced Settings

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Advanced Settings](advanced-settings.md) | `cases-advanced-settings.json` | 35 | Drafted 2026-07-14, not live-verified |

## 09. Legal Policies

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Privacy Policy Generator](legal-policies/privacy-policy-generator.md) | `cases-privacy-policy-generator.json` | 75 | Drafted 2026-07-15; most steps live-verified across Free and Pro/Ultimate accounts, Use of Data and Data Retention still thin |

Not yet documented: Cookie Policy Generator — no case file exists yet.

## 10. Profile & Account

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Team](profile-account/team.md) | `cases-team.json` | 17 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Organisation Management](profile-account/organisations-and-sites/organisation-management.md) | `cases-organisation-and-sites.json` | 17 of 66 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Site Management](profile-account/organisations-and-sites/site-management.md) | `cases-organisation-and-sites.json` | 33 of 66 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Site Transfer](profile-account/organisations-and-sites/site-transfer.md) | `cases-organisation-and-sites.json` | 16 of 66 | Drafted 2026-07-14, not live-verified |
| [My Account](profile-account/my-account.md) | `cases-my-account.json` | 28 | Drafted 2026-07-23 via `/wiki-sync`, spot-checked live same day; all follow-up items resolved except the real-inbox email round-trip and 2FA-disable toaster text (see page's Known gaps) |

Not yet documented: Notifications (no case file exists yet).

## 11. Billing & Upgrade

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Plan Gates](billing-upgrade/plan-gates.md) | `cases-privacy-policy-generator.json` (3 consolidated Layer 2 cases; no standalone case file exists for this section) | 3 (Privacy Policy Generator matrix only) | Updated 2026-07-23 via `/wiki-sync` — Privacy Policy Generator's Free/Basic/Pro+Ultimate matrix live-verified; all other sections' gates still Layer-1-only |

Not yet documented: Free Plan, Trial — without card, Trial — with card, Paid Plan — no case file
exists yet. `plan-gates.md` now contains a complete per-tier gate matrix for Privacy Policy
Generator; every other feature section's gates are still only covered by scattered Layer 1
touchpoint cases with no consolidated Layer 2 case of their own.

## 12. Agency

Not yet documented — no case file exists yet.

## 13. Platforms

Not yet documented: Plugin (WordPress), Shopify (Native App), Wix — no case file exists yet.

## 14. Permissions

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Permissions](permissions.md) | 13 cases across `cases-organisation-and-sites.json` (10), `cases-team.json` (2), `cases-colours.json` (1) | 13 | Drafted 2026-07-23 via `/wiki-sync`; all 13 backing cases already live-verified |

Cross-cutting page synthesizing the role hierarchy (Editor ⊂ Admin ⊂ Account Owner) from
`testrail-suite-v2.md` plus every confirmed permission-divergence case found so far. Already
linked from `profile-account/team.md` and all three `organisations-and-sites/*.md` pages.
Known gap: whether the one confirmed Account-Owner-only plan-upgrade restriction generalizes to
every upgrade nudge app-wide is unconfirmed — see the page's own Known gaps section.

## 15. Internal Tools

Not yet documented: Maintenance Page, CKY-Admin — no case file exists, and these may not be
reachable via the accounts in `qa-accounts.json` at all.

## 16. Miscellaneous

Not a real page area — intentionally skipped.

## 17. Reports

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Reports](reports.md) | `cases-reports.json` | 6 (thin) | Drafted 2026-07-14, not live-verified |

---

## Known gaps / next pass

This first pass deliberately used only existing TestRail case data (`ai-context/cases-*.json`) —
no live browsing of the QA app yet. Two follow-up passes remain, both deferred for now at the
user's request:

1. **Live crawl for sections with no case file** — Onboarding, Cookie Policy Generator,
   Notifications, Billing (Free/Trial/Paid Plan), Agency, Platforms, Internal Tools. Requires
   logging into the live app via the `playwright` MCP with the accounts in `qa-accounts.json`
   (free/basic/pro/ultimate/admin/editor as appropriate per page).
2. **Spot-check verification of the other pages** against the live app, to confirm the
   case-derived content still matches current UI and to fill the explicit "(not captured in
   source data — needs live verification)" gaps each page already flags (exact routes, thin
   pages like `signup-standard-free.md`, `custom-css.md`, `plan-gates.md`, `reports.md`,
   `display-layout.md`, and the Use of Data / Data Retention sections of
   `privacy-policy-generator.md`). `dashboard.md` is a partial case of this already — most of
   its 88 backing cases (active/verified states, paid-plan variants, populated charts, the full
   Add a New Site flow) still need their own live-check pass; see that page's Known gaps section.
   `permissions.md`'s open question (whether the one confirmed plan-upgrade role restriction
   generalizes app-wide) also belongs on this list. `profile-account/my-account.md` was spot-
   checked live 2026-07-23 (account deletion, save preferences, expired verification code, the
   unverified-email 2FA tooltip, and the Change-password post-submit dialog all confirmed); the
   full real-inbox email-update happy path and 2FA-disable toaster text remain unchecked.
