# CookieYes App Wiki

An LLM-readable knowledge base of the CookieYes web app — one page per feature area, each
self-contained (newcomer test / isolation test / RAG accuracy test, per
`migration-conventions.md` §0). Structure mirrors the 17-section app map in
`testrail-suite-v2.md` (read that file for the canonical section tree).

**Coverage as of 2026-07-15:** 23 pages drafted from the existing `ai-context/cases-*.json`
TestRail export files. Most of these have not been live-verified against the running QA app yet —
each page's own **Source** section says so explicitly where that's still true. The
[Privacy Policy Generator](09-legal-policies/privacy-policy-generator.md) page is the first
exception: most of its wizard has been live-verified across a Free and a Pro/Ultimate account.
Roughly half the app's sections have **no page yet at all** (see "Not yet documented" below)
because no TestRail case data exists for them — they need a first live-crawl pass through
`qa-accounts.json`, which was deliberately deferred rather than run automatically. See the plan at
the bottom of this file for what that follow-up pass would cover.

---

## 01. Authentication

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Sign Up — Core](01-authentication/signup-core.md) | `cases-signup-core.json` | 17 | Drafted 2026-07-14, not live-verified |
| [Sign Up — Standard (Free)](01-authentication/signup-standard-free.md) | `cases-signup-standard-free.json` | 3 (thin) | Drafted 2026-07-14, not live-verified |
| [Log In](01-authentication/login.md) | `cases-login.json` | 10 | Drafted 2026-07-14, not live-verified |
| [Password Reset](01-authentication/password-reset.md) | `cases-forgot-password.json` | 21 | Drafted 2026-07-14, not live-verified |

Not yet documented: Sign Up > Trial without card, Trial with card (Checkout), Agency.

## 02. Onboarding

Not yet documented: Banner Setup, Banner Installation — no case file exists yet.

## 03. Dashboard

Not yet documented: Alert Banners, Header, Add a New Site, Cookie Banner Status Card, Cookie
Summary Card, Consent Trends Card, Pageviews Card, Recent Consent Logs Card — no case file exists
yet.

## 04. Cookie Banner

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Display & Layout (page shell)](04-cookie-banner/display-layout.md) | single case in `cases-general.json` (older draft) | 1 (largely incomplete) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — General](04-cookie-banner/general.md) | `cases-cookie-banner-general.json` | 26 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Layout](04-cookie-banner/layout.md) | `cases-cookie-banner-layout.json` | 23 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Content (GDPR)](04-cookie-banner/content-gdpr.md) | `cases-cookie-banner-content.json` | 22 of 31 (11 shared with US State Laws) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Content (US State Laws)](04-cookie-banner/content-us-state-laws.md) | `cases-cookie-banner-content.json` | 20 of 31 (11 shared with GDPR) | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Colours](04-cookie-banner/colours.md) | `cases-colours.json` | 12 | Drafted 2026-07-14, not live-verified |
| [Customization Sidebar — Custom CSS](04-cookie-banner/custom-css.md) | `cases-custom-css.json` | 5 (thin) | Drafted 2026-07-14, not live-verified |

Not yet documented within this section: Device Preview, Publishing (also flagged as gaps inside
`display-layout.md`) — no case file exists yet.

## 05. Cookie Manager

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Cookie List & Categories](05-cookie-manager/cookie-list-categories.md) | `cases-cookie-manager.json` | 6 of 34 | Drafted 2026-07-14, not live-verified |
| [Scan & Scan History](05-cookie-manager/scan-and-scan-history.md) | `cases-cookie-manager.json` | 23 of 34 | Drafted 2026-07-14, not live-verified |
| [Edit & Add Cookies](05-cookie-manager/edit-add-cookies.md) | `cases-cookie-manager.json` | 5 of 34 | Drafted 2026-07-14, not live-verified |

## 06. Consent Log

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Consent Log](06-consent-log.md) | `cases-consent-log.json` | 23 | Drafted 2026-07-14, not live-verified |

## 07. Languages

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Languages](07-languages.md) | `cases-languages.json` | 23 | Drafted 2026-07-14, not live-verified |

## 08. Advanced Settings

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Advanced Settings](08-advanced-settings.md) | `cases-advanced-settings.json` | 35 | Drafted 2026-07-14, not live-verified |

## 09. Legal Policies

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Privacy Policy Generator](09-legal-policies/privacy-policy-generator.md) | `cases-privacy-policy-generator.json` | 75 | Drafted 2026-07-15; most steps live-verified across Free and Pro/Ultimate accounts, Use of Data and Data Retention still thin |

Not yet documented: Cookie Policy Generator — no case file exists yet.

## 10. Profile & Account

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Team](10-profile-account/team.md) | `cases-team.json` | 17 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Organisation Management](10-profile-account/organisations-and-sites/organisation-management.md) | `cases-organisation-and-sites.json` | 17 of 66 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Site Management](10-profile-account/organisations-and-sites/site-management.md) | `cases-organisation-and-sites.json` | 33 of 66 | Drafted 2026-07-14, not live-verified |
| [Organisations & Sites — Site Transfer](10-profile-account/organisations-and-sites/site-transfer.md) | `cases-organisation-and-sites.json` | 16 of 66 | Drafted 2026-07-14, not live-verified |

Not yet documented: My Account, Notifications — no case file exists yet.

## 11. Billing & Upgrade

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Plan Gates](11-billing-upgrade/plan-gates.md) | `cases-plan-gates-new.json` | 1 (very thin — index page only) | Drafted 2026-07-14, not live-verified |

Not yet documented: Free Plan, Trial — without card, Trial — with card, Paid Plan — no case file
exists yet. `plan-gates.md` is linked from most other pages as the plan-gating reference but does
not yet contain the actual per-tier gate matrix.

## 12. Agency

Not yet documented — no case file exists yet.

## 13. Platforms

Not yet documented: Plugin (WordPress), Shopify (Native App), Wix — no case file exists yet.

## 14. Permissions

Not yet documented as a standalone cross-cutting page yet, though the role hierarchy (Editor ⊂
Admin ⊂ Account Owner) is already reflected inline in `10-profile-account/team.md` and all three
`organisations-and-sites/*.md` pages, each of which links to a not-yet-existing
`14-permissions.md` — that page still needs to be written and would mostly synthesize
`testrail-suite-v2.md`'s permission table plus live verification with the admin/editor QA
accounts.

## 15. Internal Tools

Not yet documented: Maintenance Page, CKY-Admin — no case file exists, and these may not be
reachable via the accounts in `qa-accounts.json` at all.

## 16. Miscellaneous

Not a real page area — intentionally skipped.

## 17. Reports

| Page | Source | Cases | Freshness |
|---|---|---|---|
| [Reports](17-reports.md) | `cases-reports.json` | 6 (thin) | Drafted 2026-07-14, not live-verified |

---

## Known gaps / next pass

This first pass deliberately used only existing TestRail case data (`ai-context/cases-*.json`) —
no live browsing of the QA app yet. Two follow-up passes remain, both deferred for now at the
user's request:

1. **Live crawl for sections with no case file** — Onboarding, Dashboard, Cookie Policy Generator,
   My Account, Notifications, Billing (Free/Trial/Paid Plan), Agency, Platforms, Permissions,
   Internal Tools. Requires logging into the live app via the `playwright` MCP with the accounts in
   `qa-accounts.json` (free/basic/pro/ultimate/admin/editor as appropriate per page).
2. **Spot-check verification of the other pages** against the live app, to confirm the
   case-derived content still matches current UI and to fill the explicit "(not captured in
   source data — needs live verification)" gaps each page already flags (exact routes, thin
   pages like `signup-standard-free.md`, `custom-css.md`, `plan-gates.md`, `reports.md`,
   `display-layout.md`, and the Use of Data / Data Retention sections of
   `privacy-policy-generator.md`).
