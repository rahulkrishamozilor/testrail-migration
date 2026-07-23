# Cookie Banner — Layout

**Nav path:** Cookie Banner > Customization > Layout
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Popup layout (Cookie Notice sub-section, GDPR only) requires Pro or higher — see
docs/wiki/billing-upgrade/plan-gates.md for the full gate matrix. All other Layout controls
(Box, Banner, position options, Preference Centre / Opt-out Center styles, Categories on first
layer toggle) are available on every plan.

## Purpose
The Layout tab controls the cookie banner's shape (Box / Banner / Popup), its screen position,
and the style of the secondary consent panel it opens (Preference Centre under GDPR, Opt-out
Center under US State Laws). Which controls appear, and which combinations are legal, depends on
the Law selector set elsewhere in Cookie Banner > Customization — GDPR unlocks a third layout
(Popup) and a third preference-centre style (Pushdown) that US State Laws does not offer.

## Page structure

The tab is organized into two stacked sub-sections whose contents change with the active law
state. Law state is read from the Preconditions of each case, not chosen on this tab itself.

### Under GDPR (law selector = GDPR, default)

- **Cookie Notice sub-section** — three layout options with preview icons: **Box** (selected by
  default), **Banner**, **Popup**. Popup displays a crown icon indicating it requires a paid plan
  (Pro or higher).
  - Box position options (shown below the layout icons when Box is selected): **Bottom left**
    (default), **Bottom right**, **Top left**, **Top right**.
  - Banner position options (shown when Banner is selected): **Bottom** (default), **Top**.
  - Popup has no position choice — a **Center** position indicator is shown below the layout
    icons in place of selectable options (Popup supports Center only).
- **Preference Centre sub-section** — appears below the position options: **Center** (selected by
  default), **Sidebar**, **Pushdown**. Pushdown is disabled (greyed out) unless Banner layout is
  selected; selecting Box resets the Preference Centre choice back to Center and disables
  Pushdown again.
  - Sidebar sub-position: **Left** (default), **Right**.
  - Pushdown has no sub-position; selecting it turns the "Customise" button in the banner preview
    into a dropdown-chevron trigger instead of opening an overlay.
- **Categories on first layer** toggle — sits below the Preference Centre sub-section. Visible
  but disabled (greyed out, non-interactive) unless Banner + Pushdown is the active combination;
  it becomes enabled the moment Pushdown is selected under Banner.

### Under US State Laws (law selector = US State Laws)

- **Cookie Notice sub-section** — only two layout options: **Box** (default), **Banner**. Popup
  does not appear at all.
  - Position options for Box and Banner are identical to GDPR (Bottom left/Bottom right/Top
    left/Top right for Box; Bottom/Top for Banner).
- **Opt-out Center sub-section** — replaces the Preference Centre sub-section by name and by
  scope: only **Center** (default) and **Sidebar** styles are offered. Pushdown is not available
  under US State Laws, and consequently the Categories on first layer toggle does not appear in
  this law state.
  - Sidebar sub-position: **Left** (default), **Right**.
- The trigger control on the banner preview also differs from GDPR: opening the Opt-out Center is
  done via the **"Do Not Sell or Share My Personal Information"** link on the banner, not a
  "Customise" button.

### Combined "GDPR & US State Laws" template

When the Law selector is set to **GDPR & US State Laws**, a **Customize** sub-dropdown appears in
the Consent Template card (owned by the General tab; see docs/wiki/cookie-banner/general.md).
Switching that sub-dropdown between GDPR and US State Laws live-updates which of the two Layout
tab structures above is displayed — see Workflow 3 below.

## Workflows

### GDPR

1. **View default Layout controls.** Precondition: law selector = GDPR (default). Open Cookie
   Banner > Layout. Expect Box/Banner/Popup listed with preview icons, Popup showing a crown
   icon; Box selected by default; Bottom left/Bottom right/Top left/Top right position options
   with Bottom left selected; Center/Sidebar/Pushdown listed with Center selected and Pushdown
   disabled; Categories on first layer toggle visible and disabled.
2. **Select Box layout.** Click Box (or confirm the default). Preview shows the Box banner at
   Bottom left. Click "Publish Changes" — Box layout goes live on the website.
3. **Select Banner layout.** Click the Banner layout option. Bottom/Top position options appear
   and Pushdown (previously disabled under Box) becomes selectable in the Preference Centre
   sub-section. Bottom is selected by default. Click "Publish Changes" — Banner layout goes live
   at Bottom.
4. **Select Popup layout (paid plan precondition: Pro or higher).** Click the Popup layout
   option. A Center position indicator appears (no other position offered). Click "Publish
   Changes" — Popup layout goes live.
5. **Reposition a Box banner.** With Box active, select Bottom right, then Top left, then Top
   right in turn — preview updates to the corresponding corner after each selection. Click
   "Publish Changes" — the last-selected position (Top right) goes live.
6. **Reposition a Banner banner.** With Banner active (Bottom by default), select Top — preview
   moves to the top. Click "Publish Changes" — Top position goes live.
7. **Box + Center Preference Centre.** With Box active and Center selected (default), click
   "Customise" on the banner in the preview — the Preference Centre opens in Center style,
   overlaying the preview. Click "Publish Changes."
8. **Box + Sidebar Preference Centre.** With Box active, click "Sidebar" — Left/Right position
   options appear, Left selected by default. Click "Customise" — sidebar opens on the left.
   Publish. Then select "Right" — click "Customise" again — sidebar opens on the right. Publish.
9. **Banner + Center Preference Centre.** With Banner active (Bottom position), Center is
   selected by default — click "Customise" to confirm it opens centered, then Publish.
10. **Banner + Sidebar Preference Centre.** With Banner active, click "Sidebar" — Left/Right
    options appear (same Left-default → Right flow as workflow 8). Publish after each side.
11. **Banner + Pushdown.** With Banner active, click "Pushdown" in the Preference Centre
    sub-section — Pushdown is selected, the "Customise" button in the preview becomes a dropdown
    chevron (content does not expand until clicked), and the Categories on first layer toggle
    becomes enabled. Click the chevron/"Customise" — Pushdown content expands below the banner.
    Publish.
12. **Enable Categories on first layer.** Precondition: Banner + Pushdown active, toggle enabled.
    Turn the toggle on — cookie categories appear on the banner's first layer in the preview.
    Publish — categories go live on the first layer.
13. **Disable Categories on first layer.** Precondition: Banner + Pushdown active, toggle on
    (categories visible, e.g. "Necessary"). Turn the toggle off — categories disappear, leaving
    only the standard Accept All / Customise / Reject All buttons on the first layer. Publish.
14. **Switch away from Banner + Pushdown back to Box.** Precondition: Banner + Pushdown active,
    Categories toggle interactive. Click Box — position options change to the four Box corners;
    Preference Centre resets to Center and Pushdown becomes unavailable (greyed out); Categories
    on first layer toggle becomes disabled (greyed out, non-interactive). Publish — Box + Center
    goes live.
15. **Popup + Center Preference Centre (paid plan precondition).** With Popup active, Center is
    selected by default — "Customise" opens it centered. Publish.
16. **Popup + Sidebar Preference Centre (paid plan precondition).** With Popup active, click
    "Sidebar" — same Left-default → Right flow as workflows 8/10. Publish after each side.
17. **Open the Popup upgrade nudge (Free/Basic plan).** Click the Popup layout option while it
    shows the crown icon. An in-app nudge appears headlined **"Use a popup layout to boost opt-in
    rates,"** stating availability on Pro and Ultimate plans, with an upgrade CTA reading **"Try
    Pro for Free"** (Free plan) or **"Upgrade now"** (Basic plan). See
    docs/wiki/billing-upgrade/plan-gates.md for destination behavior of the CTA.

### US State Laws

1. **View default Layout controls under US State Laws.** Precondition: law selector = US State
   Laws. Open Layout tab. Expect only Box and Banner listed (no Popup); Box selected by default;
   Bottom left/Bottom right/Top left/Top right position options with Bottom left selected; an
   Opt-out Center sub-section (not "Preference Centre") listing Center (default) and Sidebar only
   — no Pushdown.
2. **Box + Center Opt-out Center.** With Box active and Center selected (default), click the **"Do
   Not Sell or Share My Personal Information"** link on the banner preview — the Center Opt-out
   Center overlays the preview. Publish.
3. **Box + Sidebar Opt-out Center.** With Box active, click "Sidebar" — Left/Right options
   appear, Left default. Click the DNS link — sidebar opens left. Publish. Select "Right" — click
   the DNS link again — sidebar opens right. Publish.
4. **Banner + Center Opt-out Center.** Click Banner in the Cookie Notice sub-section — Bottom/Top
   options appear; Opt-out Center sub-section shows Center (default) and Sidebar only (no
   Pushdown). Confirm Bottom and Center defaults, click the DNS link to confirm center overlay,
   Publish.
5. **Banner + Sidebar Opt-out Center.** With Banner active (Bottom position), click "Sidebar" —
   same Left-default → Right flow as workflow 3, triggered via the DNS link each time. Publish
   after each side.

### Combined law mode

1. **Switch law context under "GDPR & US State Laws."** Precondition: law selector = GDPR & US
   State Laws; the Customize sub-dropdown in the Consent Template card is set to GDPR. Confirm
   Box/Banner/Popup and the Preference Centre sub-section are visible. Switch the Customize
   sub-dropdown to US State Laws — Popup disappears (Box/Banner only) and the Preference Centre
   sub-section is replaced by an Opt-out Center sub-section. Switch back to GDPR — Box/Banner/
   Popup and the Preference Centre sub-section are restored.

## Validation & edge cases

- **Popup is GDPR-only and plan-gated.** It never appears under US State Laws (workflows US-1,
  Combined-1), and under GDPR it requires Pro or higher — Free/Basic plans see a crown icon that
  opens the upgrade nudge (GDPR workflow 17) rather than applying the layout.
- **Pushdown is GDPR-only and Banner-only.** It is disabled under Box (any law state) and does
  not exist as an option at all under US State Laws — the Opt-out Center sub-section offers only
  Center/Sidebar, never Pushdown.
- **Categories on first layer toggle is a derived state, not an independent control.** It exists
  only under GDPR, stays disabled until Banner + Pushdown is the active combination, and reverts
  to disabled the instant Pushdown is deselected (e.g. by switching back to Box) — see GDPR
  workflow 14. It does not appear at all under US State Laws.
- **Popup has no position options** — unlike Box (4 corners) and Banner (Bottom/Top), Popup shows
  a fixed Center indicator with nothing to select.
- **Terminology and trigger control differ by law state, not just labels:** GDPR's secondary
  panel is the "Preference Centre," opened via a "Customise" button; US State Laws' equivalent is
  the "Opt-out Center," opened via the "Do Not Sell or Share My Personal Information" link. Do not
  treat these as interchangeable when writing or reviewing test cases.
- **Switching Preference Centre style away from Pushdown resets the selection to Center**, it
  does not remember a prior Sidebar/Center choice (GDPR workflow 14).
- (not captured in source data — needs live verification): behavior of Categories on first layer
  toggle state, and Preference Centre/Opt-out Center selection, when switching the Law selector
  itself (not just the Customize sub-dropdown in combined mode) between law states with a
  non-default layout already configured.

## Related pages
- docs/wiki/cookie-banner/general.md
- docs/wiki/cookie-banner/display-layout.md
- docs/wiki/cookie-banner/colours.md
- docs/wiki/cookie-banner/content-gdpr.md
- docs/wiki/cookie-banner/content-us-state-laws.md
- docs/wiki/billing-upgrade/plan-gates.md

## Source
Derived from `ai-context/cases-cookie-banner-layout.json` (23 TestRail cases). Drafted
2026-07-14, not yet live-verified against the QA app.
