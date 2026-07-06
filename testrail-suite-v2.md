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

4. **Role differences belong in Permissions, not everywhere.**
   The default role for all cases outside section 14 is Account Owner. Admin and Editor cases exist only where their permissions actually diverge.

5. **Platform differences belong in Platforms, not everywhere.**
   Core features (Cookie Banner, Cookie Manager, etc.) are tested against Webapp. Platform-specific behavior (Plugin connection, Shopify native app, Wix iframe) lives in section 13.

6. **Cases are automation-ready by design.**
   Test *behavior*, not UI copy or layout. Cases that verify static text or pixel alignment are manual-only and should not receive `automation_type = Playwright`.

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
│   ├── Display & Layout
│   ├── Customization Sidebar
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
│   ├── Cookie List & Categories
│   ├── Scan & Scan History
│   └── Edit & Add Cookies
│
├── 06. Consent Log
│
├── 07. Languages
│
├── 08. Advanced Settings
│
├── 09. Reports
│   ├── Cookie Policy Generator
│   └── Privacy Policy Generator
│
├── 10. Profile & Account
│   ├── My Account
│   ├── Team
│   ├── Organisations & Sites
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
└── 16. Miscellaneous
```

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

**Layer 2 — Plan Gates (live in `11. Billing & Upgrade > Plan Gates`)**
Assert that each plan is correctly configured. One case per plan, steps walk through all gated touchpoints across all pages. Tag as `smoke`.

- These cases are automation candidates. The Playwright test provides per-gate assertion granularity; the TestRail case is the coverage marker.

**Nudge button behaviour (live in `11. Billing & Upgrade`)**
Test the upgrade button destination once per plan state that has a distinct destination. Do not re-test the button in every feature section.

- Free plan → "Try Pro for Free" → trial signup page → `11. Billing & Upgrade > Free Plan`
- Basic plan (distinct upgrade path) → pricing/plans page → `11. Billing & Upgrade > Paid Plan`

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

- Set `automation_type = Playwright` when a Playwright test covers this case.
- Reference the TestRail case ID in the Playwright test file using the `@C1234` tag in the test title.
- Do not set `automation_type = Playwright` on layout/display verification cases — these should remain manual.

---

## Where specific scenario types live

| Scenario | Lives in |
|---|---|
| Form field validation (email, password, website URL) | 01. Authentication > Sign Up > Core |
| Email verification flow | 01. Authentication > Sign Up > Core |
| Credit card entry during trial signup | 01. Authentication > Sign Up > Trial with card (Checkout) |
| "Try Pro for free" button (Free plan) | 11. Billing & Upgrade > Free Plan |
| Upgrade button from nudge (Basic plan) | 11. Billing & Upgrade > Paid Plan |
| Plan-gated feature configuration (all plans) | 11. Billing & Upgrade > Plan Gates |
| In-app nudge opens from a feature entry point | Feature section where the entry point lives (e.g. 03. Dashboard > Cookie Banner Status Card) |
| "Ends in N days" trial display | 11. Billing & Upgrade > Trial — with card |
| "Buy Pro" / "Switch to Pro trial?" | 11. Billing & Upgrade > Trial — with card |
| Agency license purchase | 12. Agency > Agency Dashboard |
| Editor cannot access a feature that Admin and AO can | 14. Permissions > Editor |
| Admin (and Editor) cannot access an Account Owner-only feature | 14. Permissions > Admin |
| Shopify native app installation | 13. Platforms > Shopify (Native App) |
| Cookie Banner behavior | 04. Cookie Banner — tested once for Webapp |
| Cookie Manager behavior | 05. Cookie Manager — tested once for Webapp |

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
4. **Set `automation_type = Playwright`** if the scenario is behavior-testable and a Playwright test will be written to cover it.
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

- [ ] **[M1] Credit card entry during signup belongs in Billing, not Authentication** — The scenario table places "Credit card entry during trial signup" in `01. Authentication > Sign Up — Trial with card`. Principle 3 says billing flows belong in section 11. Either move these cases to `11. Billing & Upgrade > Trial — with card` or document why signup-time card entry is an exception.

- [ ] **[M2] Sections 06, 07, 08, and 16 have no sub-sections defined** — `06. Consent Log`, `07. Languages`, `08. Advanced Settings`, and `16. Miscellaneous` appear as flat leaves in the tree. The document gives no guidance on whether these are intentionally flat, how to title cases without a sub-section, or what qualifies as Miscellaneous.

- [x] **[M3] `run_type = full` cannot be run in isolation** — Resolved. `full` is no longer a case-level value. Valid values are `smoke` and `regression` only. Edge cases and error paths use `regression`. Full run = no filter, entire suite.

- [x] **[M4] `automation_type` is not listed as a required field** — Resolved. `automation_type` does not exist as a custom field in the v2 suite and is not written to TestRail. The migration workflow does not include it in case payloads.

- [ ] **[L1] Billing boundary between section 11 and section 12 is undefined** — Principle 3 says billing behavior belongs in sections 11 and 12, but does not define the split. Section 12 has an `Agency Billing & Upgrade` sub-section that overlaps with section 11's scope. Define which billing cases go in 11 vs 12.

- [ ] **[L2] Suite 16 legacy entry is unexplained** — The legacy table lists `Suite 16 — CookieYes Functional Test Suite` with no context on how it relates to the new v2 suite. Add a one-line note clarifying the lineage.

- [ ] **[L3] "Reports" is a misleading section name** — Section 09 contains `Cookie Policy Generator` and `Privacy Policy Generator`. These are document generators, not analytics reports. Rename the section to avoid misfiled cases from the agentic workflow.
