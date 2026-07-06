# CookieYes TestRail Migration — Conventions

> Migration playbook for transforming Suite 6 cases into v2. Read alongside
> `testrail-suite-v2.md` (the v2 end-state spec). When the two conflict, the v2 spec wins.
>
> Cases in v2 serve three consumers equally: a newcomer who has never used CookieYes, a QA
> agent formulating a Playwright test plan, and a RAG retrieval system that reads each case
> in isolation. **Completeness takes priority over brevity.** A case that is short but
> ambiguous fails all three consumers. A case that is longer but self-contained serves all
> three.

---

## 0. Completeness standard

Every case must pass the following three checks before it is published. These checks override
all brevity rules in later sections.

### 0a — The newcomer test

Read the case as if you have never used CookieYes. Ask:
- Do the Preconditions tell me enough about the page I am starting on to find my way?
- Does each step tell me exactly what to interact with and where it is on the page?
- Does each expected result tell me exactly what I should see, not just that "something changed"?

If the answer to any of these is no, the case is incomplete. Add the missing context.

### 0b — The isolation test

Remove the case from its section and read it standalone. Ask:
- Does this case make sense without reading any surrounding cases?
- Does the Precondition describe the page state and structure well enough that the tester
  does not need to look at the app first?

Cases that depend on implicit knowledge ("you know the Dashboard, so you know where the card
is") fail the isolation test. Make the context explicit.

### 0c — The RAG accuracy test

This suite will be indexed for semantic search. Each case is a retrieval unit. Ask:
- Is the title specific enough to distinguish this case from similar cases in the section?
- Do the expected results name specific UI elements, exact labels, and exact states — not
  generic outcomes?
- Would an AI reading only this case understand what feature is being tested, what the page
  looks like, and what the correct outcome is?

Generic expected results ("the page should update", "changes should reflect") fail this test.
Name the element, the label, and the state.

### Structural context is not the same as alignment

Section 4 says to drop layout and position steps. That rule targets pixel-level alignment
checks ("the button is left-aligned", "the card is at the top of the sidebar"). It does **not**
mean dropping structural context that helps a reader orient themselves on the page.

**Drop — pure alignment:**
- "The Submit button should be displayed as centre-aligned."
- "The Consent Template card should be displayed at the top of the sidebar."

**Keep — structural context:**
- "The card should display the website URL at the top, with a banner status sub-section on
  the left and Regulation and Targeted location fields on the right."
- "The modal should contain two tabs: Install manually on website and Install with Google
  Tag Manager."

The distinction: alignment describes *where* something sits in pixels. Structural context
describes *what the page is made of* so the tester knows what they are looking at.

---

## 1. Title format

```
[Feature Area] Verify that <component> <expected behaviour> <under condition>
```

- **Feature area** — top-level product feature in brackets: `[Cookie Banner]`, `[Sign Up]`,
  `[Consent Log]`. Not a sidebar tab name, not a plan tier.
- **Verify that** — standard QA assertion verb. Makes the test objective unambiguous.
- **Under condition** — only include when it distinguishes this case from others in the same
  section (e.g. "when no countries are selected").

### Prefixes to strip

| Prefix | Why |
|---|---|
| `[Account Owner]` | Default role in v2 — implied |
| `[Admin]`, `[Editor]` | Strip and collapse — most feature areas are identical across all roles (see role routing rule below) |
| `[General]`, `[Layout]`, `[Content]`, `[Colours]` | Sidebar tab names — become v2 sub-section names, not title prefixes |
| `[Webapp Free]`, `[Agency]`, `[Trial with card/without card]` | Plan state — goes in Preconditions |
| `[Plugin]`, `[Shopify]`, `[Wix]` | Platform cases go to section 13 |
| `[GDPR]`, `[US State Laws]`, `[GDPR & US State Laws]` | Law context — see section 10 for placement rules |

### Role routing rule

Suite 6 prefixed every case with `[Account Owner]`, `[Admin]`, or `[Editor]` even when all three roles behave identically. **Do not route a role-prefixed case to section 14 unless the role's access genuinely diverges.**

The divergence points are narrow. For every feature area, ask: does the role have different access according to the table in `testrail-suite-v2.md`?

| Suite 6 prefix | Feature area | Action |
|---|---|---|
| `[Admin]` or `[Editor]` | Cookie Banner, Cookie Manager, Consent Log, Languages, Advanced Settings, Reports, Dashboard | Collapse into canonical Account Owner case — **do not** create a section 14 case |
| `[Editor]` | Team management (add/invite/remove members, change roles) | Route to `14. Permissions > Editor` |
| `[Editor]` | Organisation name / Site name & URL editing | Route to `14. Permissions > Editor` |
| `[Admin]` or `[Editor]` | Billing, subscription, org creation/deletion, site add/transfer/delete, ownership transfer | Route to `14. Permissions > Admin` |

### Examples

| Suite 6 title | v2 title |
|---|---|
| `[Account Owner] [General] Display of "General" Section by default.` | `[Cookie Banner] Verify that the General section is active by default in the Customization Sidebar` |
| `[Account Owner] [General] Display and functionality of Law selector drop-down by default.` | `[Cookie Banner] Verify that the Law selector defaults to GDPR` |
| `[Account Owner] [General] [GDPR] Functionality of "EU Countries & UK" option under "Geo-target banner" card` | `[Cookie Banner] Verify that selecting EU Countries & UK restricts the banner to EU/UK regions` |
| `[Account Owner] [General] Functionality of empty "Select Countries" option notification` | `[Cookie Banner] Verify that publishing with no countries selected shows a validation error` |

---

## 2. Preconditions

Preconditions define everything the tester must set up before step 1. They are not steps.
They must be written to pass the newcomer test (section 0a) and the isolation test (section
0b) — a tester reading only the Preconditions should know exactly where they are in the app
and what the page looks like before they begin.

### 2a — Navigation is a precondition, not a step

Suite 6 cases open with 2–4 navigation steps repeated identically across every case.
Collapse these to a single precondition line.

**Drop these opening step patterns:**
- `Navigate to "Cookie Banner" tab. Expected: "Cookie Banner" page should be displayed.`
- `Verify whether below sections are displayed in LHS of the customize sidebar: General / Layout / Content / Colours / Custom CSS`

**Write as precondition instead:**
```
User is on Cookie Banner > General tab.
```

The first step of the case should begin at the feature under test, not at the login screen
or the dashboard.

### 2d — Page structure context in Preconditions

For cases that test a specific card, modal, or section, add one sentence describing the
relevant structure of the page. This is the structural context a newcomer needs to orient
themselves before step 1.

**Minimal (fails isolation test):**
```
User is on the Dashboard.
```

**Complete (passes isolation and newcomer tests):**
```
User is on the Dashboard. The Cookie Banner Status card is visible in the main content area.
The card shows the website URL at the top, a banner status sub-section on the left (showing
Active/Inactive, a status message, and a contextual action link), and Regulation and
Targeted location fields on the right. A "Customise banner" link sits at the bottom of the card.
```

The amount of structural context needed scales with the complexity of the component:
- Simple page (login form): one sentence naming the fields is enough
- Complex card with multiple sub-sections: describe each sub-section and what it contains
- Modal: name the tabs, the primary content, and the action buttons

### 2b — Chained case references

Suite 6 uses `Go to [CXXX]` as step 1. Derive the actual app state from the referenced
case and write it as a precondition. Keep the reference ID for traceability.

| Suite 6 step 1 | v2 Precondition |
|---|---|
| `Go to [C205]` | `User is logged in as Account Owner on a Free plan. [C205]` |
| `Go to [C268]` | `User is logged in as Account Owner on a paid plan. [C268]` |

### 2c — Upgrade flows embedded as steps

Suite 6 cases for paid-plan features open with a full Stripe upgrade sequence (verify plan
label → click Upgrade → enter card → subscribe → return to Dashboard). This is setup, not
the test. Collapse the entire sequence to a precondition.

```
User is on a paid plan (Pro or higher).
```

*Example: C312 steps 2–8 (Stripe card entry, subscription, back to Dashboard) become this
one line. The case then starts at the Cookie Banner feature.*

---

## 3. Step writing

### Format

Each step has two parts:

**Action** — what the tester does. One action per step, imperative mood.
```
Navigate to Cookie Banner from the left sidebar.
Click the Law selector dropdown in the Consent Template card.
Select "US State Laws".
Click "Publish Changes".
```

**Expected result** — the specific, observable system response. Use "should be" — it is the
standard QA assertion phrasing and signals a requirement clearly to both humans and agents.
```
The Law selector should be open with GDPR, US State Laws, and GDPR & US State Laws options.
The dropdown label should be updated to "US State Laws".
The banner preview in the sidebar should reflect the opt-out template.
Changes should be saved and the opt-out banner should display on the website.
```

**The rule on "should be": keep it — but the assertion must name a specific, observable
outcome.** The problem in Suite 6 was not the phrase "should be" — it was the vagueness
of what was being asserted.

| ❌ Vague — drop | ✅ Specific — keep |
|---|---|
| `Corresponding changes should occur in each section` | `Each sidebar section should display US State Laws customization options` |
| `Appropriate changes should reflect on the sidebar` | `The banner preview in the sidebar should update to the opt-out template` |
| `Changes should be reflected` | `The banner should display only in EU Countries & UK regions on the website` |

### Step count

Target **4–8 steps** per case — but this is a smell indicator, not a hard limit. Cases
shorter than 4 steps usually lack a verification step or still have navigation sitting in
step 1 instead of Preconditions. Cases longer than 8 steps usually contain repeated
assertions or redundant confirmation steps (verifying the previous step worked) that should
be dropped.

Extra steps are legitimate when the scenario genuinely requires them. Multi-phase flows
often exceed 8 — a full password reset walks through submitting the form, checking the
inbox, clicking the link, landing on the reset page, submitting a new password, landing on
confirmation, and verifying the notification email. Each phase is a distinct, observable
outcome and must not be compressed.

The test: *does removing this step hide a real failure point?* If yes, keep it. If the
step only confirms the previous step worked, drop it.

### One behaviour per step

If a step produces multiple independent outcomes, split it.

**Before (C302 step 8):**
> Click "GDPR & US State Laws".
> Expected: Dropdown name should be displayed as "GDPR & US State Laws" **and** "Customize"
> drop-down should be displayed on the Consent Template card.

**After:**
> 8. Select "GDPR & US State Laws" from the Law selector.
>    → The dropdown label should update to "GDPR & US State Laws".
> 9. Observe the Consent Template card.
>    → A Customize sub-dropdown should appear with GDPR and US State Laws options.

---

## 4. Steps to drop

### Layout and position checks

Drop any step that only verifies visual position, alignment, or the static presence of a
UI element whose location never changes based on application logic.

| Drop this | Why |
|---|---|
| `Verify the display of "Consent Template" card title as left aligned` | Alignment check |
| `Verify the display of "X" card in top of the Customize sidebar` | Static position |
| `Verify whether "X" card is displayed in top of the sidebar for General / Layout / Content / Colours / Custom CSS` | Repeated presence check |
| `Verify the display of "X" drop-down in RHS of the "Y" card-title` | Static position |

**Keep a display step when** the presence or absence of an element signals a logic state
— e.g. the Customize sub-dropdown that appears only after selecting GDPR & US State Laws.

**Do not confuse alignment drops with structural context.** Structural context (what the
page is made of, what sections exist, what each section contains) belongs in Preconditions
per section 2d — not as steps, but it must appear somewhere in the case. See section 0 for
the distinction.

### Copy and tooltip text

Drop any step that verifies exact tooltip text, help text, or informational label copy.

| Drop this | Why |
|---|---|
| `Verify the text when hovering the help icon: "The selected template (opt-in banner) supports GDPR (EU & UK), LGPD (Brazil)..."` | Static copy — not a logic regression |
| `Verify the text when hovering the upgrade icon: "Upgrade to Pro or a higher plan..."` | Static copy |

### Duplicate assertions within a case

When the same assertion appears more than once (common in Suite 6), keep the first
occurrence and drop the repeats.

*Example: C299 asserts "Consent Template card is displayed in top of the Customize
sidebar" at steps 4, 6, and 7. Keep step 4, drop 6 and 7.*

### Display-of cases — rewrite as element-presence checks

Suite 6 "Display of X page" cases are almost entirely layout/copy checks. After stripping
those steps the case appears empty — but do **not** drop it entirely. Rewrite it as a
structural presence check: one step per interactive control, following the page's
top-to-bottom structure.

**Preconditions:** apply section 2a — the navigation to the page goes in Preconditions, not
step 1. Step 1 should begin at the first interactive element on the page.

**Step count:** display cases for simple pages (e.g. a confirmation screen) may have fewer
than 4 steps. This is expected — the 4-step floor in section 3 does not apply when there are
genuinely fewer interactive controls to verify.

**Drop from display cases:**
- Title and subtitle alignment / positioning
- Placeholder text content (e.g. "name@company.com")
- Static informational copy and help text
- Logo positions and marketing imagery

**Keep in display cases:**
- Each input field — one step per field, confirming it is visible and marked mandatory where applicable
- Password show/hide toggle
- Checkboxes (e.g. Terms and Conditions)
- Buttons (primary actions)
- Navigation links (e.g. "Forgot your password?", "Back to Login")
- State indicators whose presence signals a logic outcome (e.g. green tick on a success page, red cross on a failure page)

**Title pattern for rewritten display cases:**
```
[Feature Area] Verify that the <page name> renders with all required fields and controls
```

Each kept element becomes one step written in the standard action + expected format from
section 3:

| ❌ Drop (source step) | ✅ Action | ✅ Expected result |
|---|---|---|
| `Verify title "CookieYes" as centre-aligned` | | |
| `Verify subtitle "Welcome back" below title` | | |
| `Verify placeholder "name@company.com" below Email label` | | |
| `Verify placeholder of 8 dots below Password label` | | |
| `Verify logos (IAB, Google CMP, G2)` | | |
| `Verify Email address field displayed as mandatory` | Verify the Email address field is present and marked as mandatory. | Email address field should be visible and marked as a required field. |
| `Verify show password button in RHS of password field` | Verify the eye icon is present on the Password field. | The show/hide toggle should be visible on the right side of the Password field. |
| `Verify display of "Log In" button` | Verify the "Log In" button is present. | "Log In" button should be visible and interactive. |
| `Verify display of "Forgot your password?" link` | Verify the "Forgot your password?" link is present. | "Forgot your password?" link should be visible and interactive. |
| `Verify display of "Sign Up" link` | Verify the "Sign Up" link is present. | "Sign Up" link should be visible and interactive. |

---

## 5. Behavioural variants vs. style duplicates

### Collapse (style duplicate)

Two Suite 6 cases are style duplicates if, after stripping prefixes and dropping
layout/copy steps, their remaining steps and expected results are identical. Collapse to one
v2 case. Record all source case IDs in `source_case_ids`.

### Keep separate (genuine behavioural variant)

Keep cases separate when a different input produces a genuinely different system output:
different UI state, different destination, different product behaviour.

**Law selector — three genuine variants:**

| Law | Distinct behaviour |
|---|---|
| GDPR | Opt-in banner template, GDPR options in each sidebar section |
| US State Laws | Opt-out banner template, US State Laws options in each sidebar section |
| GDPR & US State Laws | Opt-in/opt-out dual template **+ Customize sub-dropdown appears** — structurally different UI |

**Geo-target — four genuine variants:**

| Option | Distinct behaviour |
|---|---|
| Worldwide | Banner displays globally |
| EU Countries & UK | Banner restricted to EU/UK regions |
| Select Countries | Banner restricted to user-chosen countries |
| Select Countries with no selection | Validation error on publish |

---

## 6. Plan Gates and nudge routing

When a Suite 6 case tests that an upgrade icon or locked state appears on a feature, do not
include it as a step in the feature section case. Extract it.

- Upgrade icon / premium badge visible in feature UI → `11. Billing & Upgrade > Plan Gates`
- Nudge button destination (clicking opens trial/pricing page) → `11. Billing & Upgrade > Free Plan` or `Paid Plan`

**Examples extracted from this section:**
- Upgrade icon on "GDPR & US State Laws" law option (C299 step 11) → Plan Gates
- Upgrade icons on EU Countries & UK and Select Countries geo-target options (C306 step 9) → Plan Gates

The feature section case tests only the behaviour available to a user who has access.

---

## 7. Complete case example

Applying all conventions to C308:

---
**[Cookie Banner] Verify that selecting specific countries restricts the banner to those countries**

**Preconditions:**
- User is on a paid plan (Pro or higher)
- No prior geo-targeting configuration exists

**Steps:**
1. Navigate to Cookie Banner from the left sidebar.
   → The Cookie Banner Customization page should be displayed with the General section active.
2. Confirm the Law selector in the Consent Template card shows GDPR.
   → GDPR should be selected by default in the Law selector.
3. Under the Geo-target banner card, select "Select Countries".
   → A country selection dropdown should be displayed with a list of countries and checkboxes.
4. Select one or more countries from the dropdown.
   → The selected countries should be checked in the dropdown.
5. Click "Publish Changes".
   → Changes should be saved and the banner should display only in the selected countries on the website.

**run_type:** `regression`
**automation_type:** `Playwright`

---

## 8. run_type assignment

`smoke` is a subset of `regression`. Valid case-level values are `smoke`, `regression`, and
empty (no value). `full` is a run mode, not a case-level value — do not assign it to cases.

| run_type | Included in | When to use |
|---|---|---|
| `smoke` | Smoke run, Regression run, Full run | Single most critical happy-path check per section — at most one per section |
| `regression` | Regression run, Full run | Breaking this would affect a real user on a common path |
| *(empty)* | Full run only | Exhaustive edge cases, boundary values, low-traffic paths that rarely regress |

When in doubt, use `regression`.

---

## 9. automation_type assignment

| Scenario | automation_type |
|---|---|
| Feature behaviour testable via user action → state change → observable result | `Playwright` |
| Layout, alignment, or visual position verification | `None` |
| Static copy or tooltip text verification | `None` |
| Third-party payment or checkout flow | `None` |

---

## 10. Law selector — section placement and precondition rules

The Law selector (GDPR / US State Laws / GDPR & US State Laws) affects every tab in the
Customization Sidebar, but not equally. The placement rule depends on whether the law
selection changes the **UI structure** or just the **available options**.

### Rule

| Tab | Law effect | Placement |
|---|---|---|
| General | Law selector lives here; Geo-target options differ per law | Cases in `Customization Sidebar > General`; law state in Preconditions |
| Layout | Available layout combinations differ (GDPR has more) | Cases in `Customization Sidebar > Layout`; law state in Preconditions |
| Content | Completely different UI components per law (Preference Center vs Opt-out Center) | Separate sub-sections: `Content > GDPR` and `Content > US State Laws` |
| Colours | Same color pickers; law determines which banner is being styled | Cases in `Customization Sidebar > Colours`; law state in Preconditions |
| Custom CSS | Law-agnostic | Cases in `Customization Sidebar > Custom CSS`; no law precondition needed |

Content is the only tab that warrants sub-sections by law because "Preference Center"
(GDPR) and "Opt-out Center" (US State Laws) are structurally different UI components —
not the same component with different data.

### GDPR & US State Laws — not a third sub-section

GDPR & US State Laws mode does not introduce new UI components. It makes both the GDPR
and US State Laws panels available simultaneously, switchable via the Customize sub-dropdown.

- In Content: run the `Content > GDPR` cases with precondition "Law selector set to
  GDPR & US State Laws, Customize set to GDPR", then the `Content > US State Laws` cases
  with "Customize set to US State Laws". No separate sub-section.
- In Layout and Colours: add precondition "Law selector set to GDPR & US State Laws,
  Customize set to [GDPR / US State Laws]" where the law context is relevant.

### Precondition wording

| Law state | Precondition line |
|---|---|
| GDPR (default) | *(omit — GDPR is the default assumption)* |
| US State Laws | `Law selector set to US State Laws.` |
| GDPR & US State Laws, viewing GDPR panel | `Law selector set to GDPR & US State Laws. Customize sub-dropdown set to GDPR.` |
| GDPR & US State Laws, viewing US State Laws panel | `Law selector set to GDPR & US State Laws. Customize sub-dropdown set to US State Laws.` |
