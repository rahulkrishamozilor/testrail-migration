# Cookie Manager — Cookie List & Categories

**Nav path:** Cookie Manager > Cookie List tab (default active tab) > category sidebar
**Route:** (not captured in source data — needs live verification; the Cookie Manager page's base path is inferred to be `/manage-cookies` from the Detailed Scan History page's URL pattern `/manage-cookies/scan-history/{id}`, see [scan-and-scan-history.md](scan-and-scan-history.md))
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Not itself plan-gated in the source cases (no case here carries a `plan_gate_flag`). See [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) for gates elsewhere in Cookie Manager (e.g. Schedule Scan, covered in [scan-and-scan-history.md](scan-and-scan-history.md)).

## Purpose
The Cookie List tab is where a site owner reviews the cookies CookieYes has discovered (or that were added manually), organized into categories, and configures per-category consent behavior via the Edit Category popup. It is also where missing-Script-URL-Pattern warnings surface, since blocking a cookie prior to consent depends on that pattern being set.

## Page structure

The Cookie List tab (one of two tabs alongside Scan History — see [scan-and-scan-history.md](scan-and-scan-history.md) for the page-level shell) shows:

- A **language selector** at the top left, defaulting to "English [Default]" — the currently selected language's name in the dropdown trigger, with "[Default]" appended only when it is the site's default language.
- A **"Publish changes"** button at the top right. Category/cookie edits are saved as drafts first (via "Save draft" in a popup) and only take effect on the live site once "Publish changes" is clicked.
- A **category sidebar** listing the categories as tabs: **Necessary, Functional, Analytics, Performance, Advertisement**, and **Uncategorised** (for discovered cookies CookieYes could not confidently classify). **Necessary** is selected by default.
- Each category tab shows a **⚠️ warning icon** next to its name when at least one of its cookies is missing a Script URL Pattern — **except Necessary**, which never shows this icon even if its cookies lack a pattern.
- Selecting a category opens its panel, containing:
  - An **edit (pencil) icon** next to the category name, opening the **Edit Category** popup. Per an explicit correction in `testrail-suite-v2.md`, **Uncategorised has this same edit pencil like every other category** — it is not missing one, contrary to an earlier draft of that doc.
  - A **"+ Add Cookie"** button in the panel's top-right (see [edit-add-cookies.md](edit-add-cookies.md)).
  - Cookie cards/rows for that category, including a **"Manually Added Cookies"** sub-section for cookies added by hand (see [edit-add-cookies.md](edit-add-cookies.md)).

### Edit Category popup
Opened via the pencil icon on any category (including Uncategorised). Contains three toggles, identical in every category:

| Toggle | Default state |
|---|---|
| "Sells or shares personal data" | **On** by default |
| "Load cookies prior to consent" | **Off** by default |
| "Hide category from banner" | **Off** by default |

The popup has a **"Save draft"** action; the page-level **"Publish changes"** button must also be clicked afterward to make the change live (both steps are required — see Workflows below).

### Category behavior is canonical, not per-category
Per `testrail-suite-v2.md`'s editorial note for this section: category behavior (the toggles above, the warning-icon logic, the Edit Category popup itself) is identical across Necessary, Functional, Analytics, Performance, and Advertisement. It is documented once, here, rather than duplicated per category. **Uncategorised is the only category whose behavior genuinely diverges** in the source cases — specifically the warning-icon / missing-Script-URL-Pattern presentation described below — and that divergence is called out explicitly where it applies.

### Uncategorised-specific: missing Script URL Pattern presentation
On the Uncategorised panel, a cookie card that has no Script URL Pattern shows:
- A **⚠️ icon** in the Script URL Pattern column header for that cookie, with the value shown as **"Not available"**.
- A **warning row** below the cookie card reading: *"This cookie does not have a script URL pattern. It is required for blocking the cookie prior to obtaining user consent"*, with a separate **"Add now"** button (not glued to the sentence — the two are distinct elements).

Clicking "Add now" opens the **Edit Cookie** popup for that cookie with the Script URL Pattern field editable (Cookie ID, Domain, and Duration are disabled for discovered cookies — see [edit-add-cookies.md](edit-add-cookies.md)). After saving, the warning row disappears from that cookie's card. The category-level ⚠️ warning icon on the sidebar only clears once **every** cookie in that category has a Script URL Pattern set.

## Workflows

1. **Switch between categories**
   1. Click a category tab in the sidebar (Necessary, Functional, Analytics, Performance, Advertisement, or Uncategorised).
   2. The panel for that category opens, showing its cookie cards and the "+ Add Cookie" button.

2. **Edit a category's consent behavior**
   1. Click the edit (pencil) icon next to the category name.
   2. The Edit Category popup opens showing the three toggles above at their current state.
   3. Toggle "Sells or shares personal data" (default on), "Load cookies prior to consent" (default off), and/or "Hide category from banner" (default off) as needed, and click "Save draft". The popup closes.
   4. Click "Publish changes" on the page. Only after this step does the change take effect on the live banner/site.

3. **Mark a category's cookies as opted out of data sales (US State Laws)**
   1. Set the Law selector to US State Laws (precondition — see [../04-cookie-banner/general.md](../04-cookie-banner/general.md)).
   2. Open Edit Category on a non-Necessary category and confirm "Sells or shares personal data" is enabled (default), then "Save draft" and "Publish changes".
   3. On the live site, click the **"Do Not Sell or Share My Personal Information"** link (capitalization confirmed live) to open the opt-out preference panel, which lists the affected category.
   4. Toggling off the category's consent there and clicking "Save My Preferences" records the category's cookies as rejected in the Consent Log's proof of consent (see [../06-consent-log.md](../06-consent-log.md)).

4. **Load a category's cookies before consent is given**
   1. Open Edit Category on a non-Necessary category, enable "Load cookies prior to consent" (off by default), "Save draft", then "Publish changes".
   2. Visiting the site without giving consent, the affected category's cookies are already present in the browser's storage before any consent action (verifiable via DevTools > Application > Cookies).

5. **Hide a category from the banner's preference panel**
   1. Open Edit Category on a non-Necessary category, enable "Hide category from banner" (off by default), "Save draft", then "Publish changes".
   2. On the live site, opening the preference panel (e.g. via "Customise" on the banner) no longer lists the hidden category.

6. **Switch the Cookie List's display language**
   1. Click the language selector dropdown (top left of the tab), which lists the languages added via the Languages page (e.g. English, Arabic, Spanish) — see [../07-languages.md](../07-languages.md) if present.
   2. Select a non-English language. The dropdown closes and the category names, category descriptions, and duration labels in the panel update to that language.

7. **Resolve a missing Script URL Pattern warning**
   1. On a category showing the ⚠️ warning row (see Uncategorised-specific behavior above, though the underlying mechanism is not category-restricted to Uncategorised — only the row's presentation was captured there in source data), click "Add now".
   2. In the Edit Cookie popup, enter a valid Script URL Pattern and click "Save draft".
   3. The warning row disappears from that cookie's card; the category's sidebar ⚠️ icon clears once no cookie in the category is missing a pattern.

## Validation & edge cases

- The **Necessary** category never shows the ⚠️ warning icon, even if its cookies lack a Script URL Pattern — this is an explicit exception confirmed live.
- Hovering the ⚠️ warning icon on an affected category shows a tooltip: *"The 'Script URL Pattern' is missing for some cookies. Add them now as it's required for cookie compliance. Our auto-blocking mechanism uses this pattern to identify third-party scripts that set cookies and to block them prior to obtaining user consent."* with a **"Learn more about adding script URL pattern"** link to CookieYes documentation on prior consent / auto-blocking.
- Both "Save draft" (in the Edit Category popup) and "Publish changes" (on the page) are required for a category-setting change to reach the live site — saving a draft alone does not publish it.
- Language switching requires at least one additional language to already be configured via the Languages page; the effect is limited to category names/descriptions/duration labels, not cookie data itself.
- Exact per-category description copy (the descriptive text shown for e.g. "Functional" or "Analytics") is (not captured in source data — needs live verification).
- Whether the Uncategorised-specific warning-row presentation (⚠️ column header + "Not available" + separate warning row + "Add now") also appears identically on the other five categories, or is truly unique to Uncategorised's UI, is (not captured in source data — needs live verification); the sidebar-level ⚠️ warning icon and its tooltip are confirmed common to all non-Necessary categories.

## Related pages
- [scan-and-scan-history.md](scan-and-scan-history.md) — scan cards, Scan History tab, Detailed Scan History page, AI Cookie Classifier; also the page-level shell (tabs, title) that this Cookie List tab lives inside.
- [edit-add-cookies.md](edit-add-cookies.md) — Edit Cookie and Add Cookie popups referenced above ("Add now", "+ Add Cookie", the "..." menu's "Edit cookie").
- [../06-consent-log.md](../06-consent-log.md) — where opted-out/rejected consent proof from category toggles (e.g. "Sells or shares personal data") is recorded.
- [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) — plan-gating matrix for other Cookie Manager features.

## Source
Derived from `ai-context/cases-cookie-manager.json` (34 TestRail cases total, split by sub-topic — 6 cases feed this file: 37277, 37278, 37279, 37280, 37281, 37282). Drafted 2026-07-14, not yet live-verified against the QA app.
