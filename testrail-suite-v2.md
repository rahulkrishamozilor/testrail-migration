# CookieYes TestRail Suite v2 — Source of Truth

> This document defines the structure, rules, and conventions for the new CookieYes TestRail test suite.
> It is the authoritative reference for the QA team and for the agentic workflow that writes new cases.

---

## Why a new suite

The legacy suite (Suite 6 — "Functional Cases") grew to ~12,000 cases across 570 sections by cloning every feature area for each plan variant (Webapp Free, Agency, Trial with card, Trial without card, Plugin, Shopify, Wix) and then tripling each clone for roles (Account Owner, Admin, Editor).

The actual behavioral differences between most of these variants are minimal — billing/upgrade flows and platform-specific onboarding differ; Cookie Banner, Cookie Manager, Consent Log, Languages, and Advanced Settings are identical across all of them. The result was 10–15 copies of every case, meaning a single feature change required updating the same test in up to 15 places.

**Suite 6 is archived as read-only.** The new suite is the single source of truth going forward.

---

## Guiding principles

1. **Organize by what you are testing, not by who is signed in or how they pay.**
   Plan variants and roles are test *preconditions*, not structural axes.
   *Exception: Authentication sub-sections are split by plan variant because each signup flow has a distinct URL and page surface. A change to one flow does not imply testing all flows.*

2. **One canonical case per scenario.**
   If the steps and expected result are identical across plans or roles, there is one case. Preconditions note the required state.

3. **Plan-specific behavior lives in one place.**
   Billing, upgrade flows, trial state display, and plan-gated UI belong in section 11 (Billing & Upgrade) and section 12 (Agency). Nowhere else.
   *Exception: credit-card entry that is part of **account creation** stays in `01. Authentication > Sign Up > Checkout` — the checkout page is part of the signup surface (same rationale as the Principle 1 signup exception). Card entry to change the plan on an **existing** account belongs in section 11.*

4. **Role differences belong in Permissions, not everywhere.**
   The default role for all cases outside section 14 is Account Owner. Admin and Editor cases exist only where their permissions actually diverge.

5. **Platform differences belong in Platforms, not everywhere.**
   Core features (Cookie Banner, Cookie Manager, etc.) are tested against Webapp. Platform-specific behavior (Plugin connection, Shopify native app, Wix iframe) lives in section 13.

6. **Cases are automation-ready by design.**
   Test *behavior*, not UI copy or layout. Cases that verify static text or pixel alignment are manual-only (there is no `automation_type` field in v2 — see open issue M4; they are simply not given a Playwright test).

---

## Suite details

| Field | Value |
|---|---|
| Suite name | CookieYes Functional Test Suite v2 |
| TestRail project | CookieYes (project ID 1) |
| Legacy suite | Suite 6 — archived, read-only |
| Custom field required | `run_type` — see below |

---

## Section structure

Maximum depth rule: **4 levels** (Suite → Section → Sub-section → Sub-sub-section). Cases always live at the leaf.
The 4th level is used only when a sub-section has a natural grouping need (e.g. multiple variants of the same flow). Default to 3 levels — do not add a 4th level just to mirror the UI structure.

**Intentionally flat sections.** `06. Consent Log`, `07. Languages`, and `08. Advanced Settings`
are single-surface feature areas — they are deliberately flat, with cases living directly at the
section leaf and the standard `[Feature Area] …` title format. Do **not** add sub-sections to
them unless the section grows large enough that cases fall into natural groups.
`05. Cookie Manager > Cookie List & Categories` is flat for the same reason: it once had a
per-category sub-section (Necessary/Functional/Analytics/Performance/Advertisement/Uncategorised)
mirroring the app's category tabs, but category behavior is identical across categories (see the
tree entry above), so all but one sub-section sat permanently empty. Removed 2026-07-13.

**Miscellaneous (16).** Reserved for cases that genuinely fit no other section. Prefer filing in
a real section; reach for Miscellaneous only as a last resort. If a cluster of related cases
accumulates in Miscellaneous, promote it into its own named section.

```
CookieYes Functional Test Suite v2
│
├── 01. Authentication
│   ├── Sign Up
│   │   ├── Core                        ← form validation + email verification cases (shared across all signup pages)
│   │   ├── Standard (Free)
│   │   ├── Trial without card
│   │   ├── Trial with card (Checkout)
│   │   └── Agency
│   ├── Log In
│   └── Password Reset
│
├── 02. Onboarding
│   ├── Banner Setup
│   └── Banner Installation
│
├── 03. Dashboard
│   ├── Alert Banners                   ← email verify, onboarding pending, compliance, pageview overage
│   ├── Header
│   ├── Add a New Site
│   ├── Cookie Banner Status Card
│   ├── Cookie Summary Card
│   ├── Consent Trends Card
│   ├── Pageviews Card
│   └── Recent Consent Logs Card
│
├── 04. Cookie Banner
│   ├── Display & Layout                ← page shell: Customization page loads, sidebar collapse/expand, tab navigation; also the live banner's own display/layout on-page
│   ├── Customization Sidebar           ← each tab's own settings behavior, incl. that tab's "renders correctly" case
│   │   ├── General                     ← Law selector, Geo-target, IAB TCF v2.2, Show Advance Settings
│   │   ├── Layout                      ← layout options differ per law; law state in Preconditions
│   │   ├── Content
│   │   │   ├── GDPR                    ← Preference Center, Cookie Notice, Cookie List
│   │   │   └── US State Laws           ← Opt-out Center, Cookie Notice, Cookie List
│   │   ├── Colours                     ← color scheme; law state in Preconditions when relevant
│   │   └── Custom CSS                  ← law-agnostic
│   ├── Device Preview
│   └── Publishing
│
├── 05. Cookie Manager
│   ├── Cookie List & Categories             ← flat (deliberately, like 06/07/08 below): category panel, cookie
│   │                                          cards, Edit Category popup, category description text, and the
│   │                                          Uncategorised-specific warning-icon/⚠️ script-URL-warning behavior.
│   │                                          Category behavior is identical across Necessary/Functional/
│   │                                          Analytics/Performance/Advertisement (equivalence partitioning —
│   │                                          see Guiding Principle 2), so cases live here as canonical cases
│   │                                          rather than duplicated per category. Do not recreate per-category
│   │                                          sub-sections — one existed for each category in TestRail and all
│   │                                          but one sat empty, since only Uncategorised's behavior actually
│   │                                          diverges (has an edit pencil like every other category, unlike
│   │                                          what an earlier draft of this doc claimed).
│   ├── Scan & Scan History                 ← scan cards, Scan History tab, Detailed scan history page
│   │                                          AI Cookie Classifier (plan-gated, opt-in; cases flat in this section)
│   └── Edit & Add Cookies                  ← Edit Cookie popup, Add Cookie popup (shared across all categories)
│
├── 06. Consent Log
│
├── 07. Languages
│
├── 08. Advanced Settings
│
├── 09. Legal Policies                 ← document generators (matches the app's "Legal Policies" nav)
│   ├── Cookie Policy Generator
│   └── Privacy Policy Generator
│
├── 10. Profile & Account
│   ├── My Account
│   ├── Team
│   ├── Organisations & Sites
│   │   ├── Organisation Management   ← create org, org card, More menu, rename, delete, pagination
│   │   ├── Site Management           ← add site, website-details row, plan-label column, subscription
│   │   │                                statuses (Banner disabled / Payment failed / Suspended), and
│   │   │                                billing entry points (Change Plan, Switch to Annual, Reactivate)
│   │   └── Site Transfer             ← transfer modal, destination dropdown, cancel request, email,
│   │                                    accept/reject page, 7-day expiry, payment/suspension
│   └── Notifications
│
├── 11. Billing & Upgrade
│   ├── Free Plan
│   ├── Trial — without card
│   ├── Trial — with card
│   ├── Paid Plan
│   └── Plan Gates                      ← plan-gated feature configuration checks across all plans
│
├── 12. Agency
│   ├── Agency Dashboard
│   └── Agency Billing & Upgrade
│
├── 13. Platforms
│   ├── Plugin (WordPress)
│   ├── Shopify (Native App)
│   └── Wix
│
├── 14. Permissions
│   ├── Admin
│   └── Editor
│
├── 15. Internal Tools
│   ├── Maintenance Page
│   └── CKY-Admin
│
├── 16. Miscellaneous
│
└── 17. Reports                         ← analytics & reporting (distinct from Legal Policies)
```

> Section ordering is indicative. `17. Reports` is numbered last so it does not renumber the
> existing sections 10–16, which are referenced by number throughout this document and the
> migration conventions.

---

## Custom field: `run_type`

The field controls which TestRail test runs pick a case up. Valid values are `smoke`,
`regression`, and empty (no value). `full` is a run mode, not a case-level value — do not
assign it to cases.

| Value | When to use | Included in |
|---|---|---|
| `smoke` | Single most critical happy-path check per section — at most one per section | Smoke run, Regression run, Full run |
| `regression` | Breaking this would affect a real user on a common path | Regression run, Full run |
| *(empty)* | Exhaustive edge cases, boundary values, low-traffic paths that rarely regress | Full run only |

### Run filters

| Run | TestRail filter |
|---|---|
| Smoke run | `run_type = smoke` |
| Regression run | `run_type IN (smoke, regression)` |
| Full run | No filter — entire suite |

`smoke` is a strict subset of `regression`. When in doubt, use `regression` rather than `smoke`.

---

## Case writing conventions

### Role

- Default role for all cases outside section 14: **Account Owner**. Do not add a role prefix to the case title.
- Role prefix (`[Admin]`, `[Editor]`) is used only in section 14 (Permissions) where the role's specific access or restriction is what is being tested.

#### Permission hierarchy

CookieYes has three roles. The hierarchy is Editor ⊂ Admin ⊂ Account Owner.

| Feature area | Account Owner | Admin | Editor |
|---|---|---|---|
| Cookie Banner, Cookie Manager, Consent Log, Languages, Advanced Settings, Reports | ✓ | ✓ | ✓ |
| Dashboard, Onboarding | ✓ | ✓ | ✓ |
| Team management (add/remove members, invite, modify roles) | ✓ | ✓ | ✗ |
| Organisation name / Site name & URL editing | ✓ | ✓ | ✗ |
| Organisation creation/deletion | ✓ | ✗ | ✗ |
| Site add / transfer / delete | ✓ | ✗ | ✗ |
| Account ownership transfer | ✓ | ✗ | ✗ |
| Billing & subscription management | ✓ | ✗ | ✗ |

**Consequence for migration:** Suite 6 cases prefixed `[Admin]` or `[Editor]` that fall in a shared feature area (Cookie Banner, Cookie Manager, Consent Log, etc.) are **identical** to Account Owner cases. Collapse them into the canonical case — do not route to section 14.

Only route to section 14 when the role's access genuinely diverges from the table above.

#### Section 14 sub-section meanings

- **14. Permissions > Editor** — cases where **Editor is blocked** from something that Admin and Account Owner can do (team management, org/site name editing).
- **14. Permissions > Admin** — cases where **Admin (and Editor) are blocked** from something only Account Owner can do (billing, org/site creation/deletion, ownership transfer).

### Platform

- Default platform: **Webapp**. Do not add a platform prefix.
- Platform-specific cases live in section 13 only. If a case in section 13 needs a platform label for clarity, prefix the title with the platform name.

### Plan state

- Default assumption: user is on an active paid plan (or active trial). Do not state this in the case.
- Only note the plan state in the **Preconditions** field when the test requires a specific billing state (e.g. "User is on Free plan", "Trial with card, day 3").

### Plan-gated features

When a feature is locked behind a paid plan (premium icon, in-app nudge), apply a two-layer approach:

**Layer 1 — Functional cases (live in the feature section)**
Test that the feature behaviour works correctly for the relevant plan state. Use equivalence partitioning — write one case per distinct behaviour, not one case per plan.

- Write separate cases only when behaviour actually differs between plans (different destination, different UI state, different outcome).
- Use a shared precondition (e.g. "Free or Basic plan") only when the behaviour is triggered identically on both plans.
- Each feature section tests only that its entry point (link, button, icon) correctly opens the nudge. The nudge button behaviour is not re-tested in the feature section.
- If the feature section owns a page or card of its own, its render/display case (`migration-conventions.md` §11) notes the plan-gating as a fact and points to Plan Gates for the full verification — see §11 "Plan-gated render cases". This keeps the gating discoverable to anyone browsing the feature section without duplicating Layer 2's verification.

**Layer 2 — Plan Gates (live in `11. Billing & Upgrade > Plan Gates`)**
Assert that each plan is correctly configured. One case per plan, steps walk through all gated touchpoints across all pages. Tag as `smoke`.

- These cases are automation candidates. The Playwright test provides per-gate assertion granularity; the TestRail case is the coverage marker.

**Nudge button behaviour (live in `11. Billing & Upgrade`)**
Test the upgrade button destination once per plan state that has a distinct destination. Do not re-test the button in every feature section.

- Free plan → "Try Pro for Free" → trial signup page → `11. Billing & Upgrade > Free Plan`
- Basic plan (distinct upgrade path) → pricing/plans page → `11. Billing & Upgrade > Paid Plan`

### Billing: section 11 vs section 12

Section 12 (Agency) owns **only** billing that is unique to agencies — agency license/seat
purchase, agency-console billing, and client/sub-account allocation. Everything else billing
lives in section 11 (Billing & Upgrade): Free, Trial (with/without card), Paid Plan, and Plan
Gates. When an agency user hits a billing flow that is identical to a non-agency account, the
case belongs in section 11, not section 12 — do not clone it per plan type.

### Title format

```
[Feature Area] Scenario being tested
```

Examples:
- `[Cookie Banner] Functionality of Publish Changes button with installation code`
- `[Sign Up] Functionality of Get Started button with valid credentials`
- `[Billing] Functionality of Try Pro for free button — USD currency`

Do not prefix titles with `[Account Owner]` unless inside section 14.

### Steps

- Write steps that test **behavior**, not UI copy.
- Avoid steps like "Verify the display of subtitle as left aligned" — these are layout checks, not behavior.
- Each step should have a clear expected result that would fail if the product had a logic regression.

### Preconditions

- State only what is genuinely required to run the case that is not obvious from context.
- For chained cases, reference the prerequisite case ID as `[C1234]` in step 1.

### Automation

- `automation_type` is **not** a v2 field and is never set (see open issue M4). Automation
  coverage is tracked by the Playwright test itself, not by a TestRail field.
- Reference the TestRail case ID in the Playwright test file using the `@C1234` tag in the test title.
- Layout/display-only verification cases stay manual — they are simply not given a Playwright test.

---

## Where specific scenario types live

| Scenario | Lives in |
|---|---|
| Form field validation (email, password, website URL) | 01. Authentication > Sign Up > Core |
| Email verification flow | 01. Authentication > Sign Up > Core |
| Credit card entry during trial signup (account creation) | 01. Authentication > Sign Up > Trial with card (Checkout) |
| Credit card entry to change plan on an existing account | 11. Billing & Upgrade > Paid Plan |
| "Try Pro for free" button (Free plan) | 11. Billing & Upgrade > Free Plan |
| Upgrade button from nudge (Basic plan) | 11. Billing & Upgrade > Paid Plan |
| Plan-gated feature configuration (all plans) | 11. Billing & Upgrade > Plan Gates |
| In-app nudge opens from a feature entry point | Feature section where the entry point lives (e.g. 03. Dashboard > Cookie Banner Status Card) |
| "Ends in N days" trial display | 11. Billing & Upgrade > Trial — with card |
| "Buy Pro" / "Switch to Pro trial?" | 11. Billing & Upgrade > Trial — with card |
| Agency license / seat purchase, agency-console billing, client allocation | 12. Agency > Agency Billing & Upgrade |
| Standard billing for an agency user (flow identical to a non-agency account) | 11. Billing & Upgrade |
| Editor cannot access a feature that Admin and AO can | 14. Permissions > Editor |
| Admin (and Editor) cannot access an Account Owner-only feature | 14. Permissions > Admin |
| Shopify native app installation | 13. Platforms > Shopify (Native App) |
| Cookie Banner behavior | 04. Cookie Banner — tested once for Webapp |
| Cookie Manager behavior | 05. Cookie Manager — tested once for Webapp |
| Organisation create / rename / delete, org card, pagination | 10. Profile & Account > Organisations & Sites > Organisation Management |
| Add site, website-details row, plan-label column, subscription statuses | 10. Profile & Account > Organisations & Sites > Site Management |
| Site transfer flow (initiate, accept/reject, expiry, suspension) | 10. Profile & Account > Organisations & Sites > Site Transfer |
| "Change Plan" / "Switch to Annual" / "Reactivate" — button appears and opens correct destination | 10. Profile & Account > Organisations & Sites > Site Management (entry point only) |
| Plans page itself (layout, selecting a tier, checkout) | 11. Billing & Upgrade > Paid Plan |
| Org create/delete, site add/transfer blocked for Admin & Editor | 14. Permissions > Admin |
| Org / site rename blocked for Editor | 14. Permissions > Editor |

---

## What is NOT in this suite

- **Shopify old web signup flow** — deprecated, replaced by native Shopify app. Old cases in suite 6 (section 389) are archived.
- **Role-prefixed clones of feature cases** — Admin and Editor do not get their own copies of Cookie Banner, Cookie Manager, etc. Role coverage is in section 14 only.
- **Plan-prefixed clones of feature cases** — Webapp Free, Agency, Trial variants do not each get their own Cookie Banner section. Plan-specific behavior is in section 11 only.
- **Shopify native app cases** — not yet written. Section 13 > Shopify is a placeholder. Cases will be added via the agentic workflow when ready.

---

## Adding new cases (agentic workflow)

When the agentic workflow writes a new case:

1. **Check section placement first.** Use the section structure above and the "Where specific scenario types live" table to determine the correct section before creating the case.
2. **Search for existing coverage** using the TestRail RAG search before creating. If a case already covers the scenario, extend it rather than creating a duplicate.
3. **Set `run_type` at creation.** Default to `regression` if unsure. Use `smoke` only for the single most critical happy-path check in a feature area.
4. **Do not set `automation_type`** — it is not a v2 field (see open issue M4). If the scenario is behavior-testable, cover it with a Playwright test tagged `@C<id>` instead.
5. **Do not create role variants.** Write one case for the scenario. If the Admin or Editor permission for that feature needs testing, add it to section 13.
6. **Do not create plan variants.** Write one case. Note the required plan state in Preconditions if needed.

---

## Legacy suite reference

Suite 6 ("Functional Cases") and Suite 7 ("Cookie Manager Revamp") remain in TestRail as read-only archives. They should not receive new cases. They can be referenced for historical context or to recover case steps during migration, but are not used for active test runs.

| Legacy suite | Status | Notes |
|---|---|---|
| Suite 6 — Functional Cases | Archived, read-only | ~12,042 cases, ~570 sections |
| Suite 7 — Cookie Manager Revamp | Archived, read-only | 19 sections, Cookie Manager feature |
| Suite 16 — CookieYes Functional Test Suite | Archived, read-only | 1 section |

---

## Open issues

- [x] **[H1] Sign-up sub-sections contradict Principle 1** — Resolved: kept the plan-variant sub-sections and added a formal exception to Principle 1. Justification: each signup flow has a distinct URL and page surface; a change to one does not imply testing all flows.

- [x] **[H2] "Permission gates" sub-sub-section violates the depth rule** — Resolved: depth rule updated to 4 levels. `14. Permissions > Admin > Permission gates` is now valid. Authentication also restructured to use the 4th level for Sign Up variants.

- [x] **[M1] Credit card entry during signup belongs in Billing, not Authentication** — Resolved: documented as an exception to Principle 3. Card entry that is part of **account creation** stays in `01. Authentication > Sign Up > Checkout` (the checkout page is part of the signup surface); card entry to change the plan on an **existing** account goes to `11. Billing & Upgrade > Paid Plan`. See Principle 3 and the scenario-placement table.

- [x] **[M2] Sections 06, 07, 08, and 16 have no sub-sections defined** — Resolved: 06/07/08 are intentionally flat (cases at the section leaf, standard title format, no sub-sections unless they grow); Miscellaneous (16) is last-resort only, and a cluster there should be promoted to its own section. See "Intentionally flat sections" under Section structure.

- [x] **[M3] `run_type = full` cannot be run in isolation** — Resolved. `full` is no longer a case-level value. Valid values are `smoke` and `regression` only. Edge cases and error paths use `regression`. Full run = no filter, entire suite.

- [x] **[M4] `automation_type` is not listed as a required field** — Resolved. `automation_type` does not exist as a custom field in the v2 suite and is not written to TestRail. The migration workflow does not include it in case payloads.

- [x] **[L1] Billing boundary between section 11 and section 12 is undefined** — Resolved: section 12 owns only agency-unique billing (license/seat purchase, agency-console billing, client/sub-account allocation); all standard-account billing stays in section 11, even for agency users when the flow is identical. See "Billing: section 11 vs section 12".

- [ ] **[L2] Suite 16 legacy entry is unexplained** — The legacy table lists `Suite 16 — CookieYes Functional Test Suite` with no context on how it relates to the new v2 suite. Add a one-line note clarifying the lineage.

- [x] **[L3] "Reports" is a misleading section name** — Resolved: section 09 is renamed **Legal Policies** (matching the app's left-nav label) and holds Cookie Policy Generator + Privacy Policy Generator. A distinct **Reports** section (analytics & reporting) is added as section 17 — kept last so it does not renumber the referenced sections 10–16.
