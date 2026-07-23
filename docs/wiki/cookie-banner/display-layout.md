# Cookie Banner > Display & Layout (Customization page shell)

**Nav path:** Cookie Banner > Customization (page shell surrounding all five sidebar tabs)
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** see [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) (no plan-gating specific to the shell itself is captured in the source case)

## Purpose
This page is the outer shell of the Cookie Banner Customization experience: the sidebar that switches between the five settings tabs, the live banner preview panel, and the Publish Changes control that commits changes across all tabs. It is distinct from the tab content itself (General, Layout, Content, Colours, Custom CSS each have their own page).

## Page structure
Confirmed from source data:

- **Customization sidebar** on the left, containing exactly five tabs, in order: **General**, **Layout**, **Content**, **Colours**, **Custom CSS**.
- **General** is the default/selected tab on page load — it is highlighted and its section content is displayed.
- **Banner preview panel** to the right of the sidebar, showing a live preview of the banner as configured.
- **Publish Changes button** at the bottom of the sidebar. It is present but **disabled by default**, and only becomes enabled once changes are made somewhere in the Customization settings.

(not captured in source data — needs live verification): the visual layout/styling of the sidebar and preview panel beyond the above (e.g. sidebar width, whether tabs show icons, whether the preview panel is scrollable or has its own toolbar).

## Workflows

1. **Land on the Customization page**
   1. Navigate to Cookie Banner > Customization.
   2. The General tab is selected and highlighted by default, showing the General section content (see [general.md](general.md)).
   3. The banner preview panel is visible to the right, showing a live preview.
   4. The Publish Changes button is visible at the bottom of the sidebar and is disabled (no pending changes yet).

All other workflows for this page — switching tabs, collapsing/expanding the sidebar, using Device Preview, and the actual publish flow once Publish Changes is enabled — are **gaps**; see below.

## Validation & edge cases
(not captured in source data — needs live verification): no validation or edge-case behavior for the shell itself was present in the single available case.

## Gaps — needs live-crawl completion

Only one seed case was available for this page (the page-shell case from the older `cases-general.json` draft), which covers the initial-load state only. The following are explicitly **not** covered and should not be assumed:

- **Sidebar collapse/expand behavior** — whether the Customization sidebar can be collapsed, and what that does to the preview panel's width/visibility. (not captured in source data — needs live verification)
- **Tab navigation transitions** — what happens when switching between General / Layout / Content / Colours / Custom CSS: whether unsaved changes carry over, whether there's a confirmation prompt, and how the preview panel updates on tab switch. (not captured in source data — needs live verification)
- **Device Preview** — testrail-suite-v2.md lists "Device Preview" as its own sub-section under Display & Layout, but no case data on it exists in either source file: no controls, breakpoints, or toggle names are known. (not captured in source data — needs live verification)
- **Publishing flow specifics** — testrail-suite-v2.md also lists "Publishing" as its own sub-section. The seed case only confirms the button starts disabled; the enabled state, the click behavior, any confirmation dialog, success/error states, and propagation timing to the live site are unknown. (not captured in source data — needs live verification)
- **The live banner's own on-page display/layout** — testrail-suite-v2.md's description of this section explicitly includes "the live banner's own display/layout on-page" (i.e., how the banner actually renders and positions itself on the end-visitor's site), separate from the Customization page's preview panel. No case data on this exists in either source file. (not captured in source data — needs live verification)

## Related pages
- [general.md](general.md) — General tab content (Law selector, Geo-target, IAB TCF v2.3, Show Advance Settings), the tab selected by default in this shell.
- [layout.md](layout.md) — Layout tab.
- [colours.md](colours.md) — Colours tab.
- [custom-css.md](custom-css.md) — Custom CSS tab.
- [content-gdpr.md](content-gdpr.md) — Content tab, GDPR variant.
- [content-us-state-laws.md](content-us-state-laws.md) — Content tab, US State Laws variant.

## Source
Derived from a single page-shell case in `ai-context/cases-general.json` (older draft file). Largely incomplete — needs a live-crawl pass to cover sidebar collapse/expand, tab navigation, Device Preview, Publishing, and the live banner's on-page display. Drafted 2026-07-14.
