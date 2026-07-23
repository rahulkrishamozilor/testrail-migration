# Cookie Manager — Edit & Add Cookies

**Nav path:** Cookie Manager > Cookie List tab > any category panel > "+ Add Cookie" button, or a cookie's "..." menu > "Edit cookie" / "Delete cookie"
**Route:** (not captured in source data — needs live verification). These are modal popups/dialogs layered over the Cookie List tab, not separate pages.
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** None indicated in the source cases (no case here carries a `plan_gate_flag`). See [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) if gating is found elsewhere in Cookie Manager.

## Purpose
These popups let a site owner manually add a cookie CookieYes didn't discover, or edit/delete a cookie (discovered or manually added) within any category. Behavior is shared identically across all categories, including Uncategorised.

## Page structure

- **"+ Add Cookie"** button — top-right of every category panel (see [cookie-list-categories.md](cookie-list-categories.md)).
- **Add Cookie popup** — required fields **Cookie ID**, **Domain**, **Duration**, **Description**; an optional **Script URL Pattern** field. A **"Save draft"** button commits the entry.
- Cookies added this way appear in the category's list under a **"Manually Added Cookies"** sub-section, distinct from discovered cookies.
- Each cookie's table/card has a **"..."** menu at its top-right with **"Edit cookie"** and **"Delete cookie"** options.
- **Edit Cookie popup** — pre-filled with the cookie's **Cookie ID, Domain, Duration, Category, Script URL Pattern,** and **Description**. For a **discovered** cookie (not manually added), the **Cookie ID, Domain, and Duration** fields are disabled; **Category, Script URL Pattern,** and **Description** remain editable. A **"Save draft"** button commits changes.
- Focusing the **Script URL Pattern** field on a discovered cookie that has a CookieYes-provided pattern shows a warning alert below the field (trigger is field *focus*, not popup open) containing two items:
  1. *"Changing the URL pattern provided by us may affect the blocking behavior of all cookies set by this script. Hence, we recommend that you do not change this unless you are fully aware of the consequences."* — with a **"Learn more about adding script URL pattern"** link to CookieYes documentation.
  2. *"Adding your website URL as the script URL pattern may disrupt your website's functionality."*

  Both items appear together in one alert; they are not conditional on what is typed into the field.
- **Delete cookie confirmation dialog** ("Delete cookie?") — heading **"Delete cookie?"**, message *"The cookie [cookie ID] will be permanently deleted. This cookie will no longer be displayed on your cookie list nor be blocked prior to receiving user consent."*, and two buttons: **"Cancel"** and **"Delete cookie."**
- After any Save draft (add, edit) or a confirmed delete, the page-level **"Publish changes"** button becomes active — the change is not live until that is clicked (see [cookie-list-categories.md](cookie-list-categories.md)).

## Workflows

1. **Add a cookie manually, with a Script URL Pattern**
   1. In any category panel, click "+ Add Cookie." The Add Cookie popup opens with Cookie ID, Domain, Duration, Description required and Script URL Pattern optional.
   2. Fill in Cookie ID, Domain, Duration, Description, and a Script URL Pattern value (e.g. "analytics.com").
   3. Click "Save draft." The popup closes and the cookie appears under that category's "Manually Added Cookies" section.

2. **Add a cookie manually, without a Script URL Pattern**
   1. Click "+ Add Cookie," fill in Cookie ID, Domain, Duration, and Description, and leave Script URL Pattern empty.
   2. Click "Save draft." The cookie appears under "Manually Added Cookies," and a ⚠️ warning icon appears next to that category's name in the sidebar (see [cookie-list-categories.md](cookie-list-categories.md) for the warning-icon mechanics).

3. **Edit a cookie's fields**
   1. On a category tab, open the "..." menu on a cookie's table and select "Edit cookie." The Edit Cookie popup opens pre-filled; for a discovered cookie, Cookie ID/Domain/Duration are disabled while Category/Script URL Pattern/Description remain editable.
   2. Update a field (e.g. Description) and click "Save draft."
   3. The popup closes, the updated value appears on the cookie's card, and "Publish changes" becomes active.

4. **Resolve a missing Script URL Pattern via Edit Cookie**
   1. Open "Edit cookie" (or reach the popup via "Add now" from a warning row — see [cookie-list-categories.md](cookie-list-categories.md)) for a cookie missing a pattern.
   2. Enter a valid Script URL Pattern and click "Save draft."
   3. The cookie's warning state clears; the category's sidebar ⚠️ icon clears once no cookie in the category is missing a pattern.

5. **Change a CookieYes-provided Script URL Pattern (with warning)**
   1. Open "Edit cookie" on a discovered cookie that has a CookieYes-provided Script URL Pattern. The popup opens with the field pre-filled and no warning visible yet.
   2. Click into (focus) the Script URL Pattern field — a warning alert appears with the two messages above.
   3. Optionally click "Learn more about adding script URL pattern" to open CookieYes documentation on prior consent / auto-blocking.

6. **Delete a cookie**
   1. On a category tab, open the "..." menu on a cookie and select "Delete cookie." The "Delete cookie?" confirmation dialog appears with the cookie's ID named in the message and Cancel/"Delete cookie" buttons.
   2. Click "Delete cookie." The dialog closes, the cookie no longer appears in the category's list, and "Publish changes" becomes active.

## Validation & edge cases

- **Required vs. optional fields in Add Cookie**: Cookie ID, Domain, Duration, and Description are required; Script URL Pattern is optional but its absence triggers the category-level ⚠️ warning icon (see [cookie-list-categories.md](cookie-list-categories.md)).
- **Discovered vs. manually-added cookies differ in editability**: only discovered cookies have Cookie ID/Domain/Duration locked in Edit Cookie; manually-added cookies' full editability beyond these three fields is (not captured in source data — needs live verification).
- **Script URL Pattern change warning triggers on field focus**, not on popup open — do not test for the warning immediately after opening Edit Cookie; it only appears once the field is focused.
- **Delete is destructive but confirmed**: the dialog explicitly warns the cookie "will no longer be displayed on your cookie list nor be blocked prior to receiving user consent" — confirming without reading is a foot-gun the copy is designed to prevent.
- **Save draft vs. Publish changes**: every add/edit/delete flow above only stages the change; "Publish changes" on the page (outside these popups) is required to make it live.

## Related pages
- [cookie-list-categories.md](cookie-list-categories.md) — category sidebar, Edit Category popup, and the Uncategorised warning-row/"Add now" entry point into Edit Cookie.
- [scan-and-scan-history.md](scan-and-scan-history.md) — scans that discover the cookies edited/deleted here.
- [../consent-log.md](../consent-log.md) — consent proof tied to cookies managed here.
- [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) — plan-gating matrix for other Cookie Manager features.

## Source
Derived from `ai-context/cases-cookie-manager.json` (34 TestRail cases total, split by sub-topic — 5 cases feed this file: 37275, 37276, 39427, 37289, 37292). Drafted 2026-07-14, not yet live-verified against the QA app.
