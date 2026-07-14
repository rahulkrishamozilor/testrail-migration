# Cookie Banner — Content (US State Laws)

**Nav path:** Cookie Banner > Customization > Content > US State Laws (Content is the third of five sidebar tabs — General, Layout, Content, Colours, Custom CSS — see [display-layout.md](display-layout.md) for the shell; US State Laws is a non-default Law selector state, set from the General tab or the Consent Template card)
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Partial — the Content tab itself is not plan-gated. Individual controls within it are:
- Opt-out Center: **Respect Global Privacy Control** toggle and its notice field require a Pro plan or higher (unlocked with no upgrade icon on Pro+; locked with an orange-crown icon on Free/Basic).
- Cookie Notice: **Custom logo** and **Disable CookieYes branding** require an Ultimate plan (shared with the GDPR view — see [content-gdpr.md](content-gdpr.md)).
- Revisit Consent Button: **Custom icon** requires an Ultimate plan (shared with the GDPR view).
- The **GDPR & US State Laws** combined Consent Template option requires a Pro plan or higher.
Full lock-state/tooltip/CTA matrix: [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md).

## Purpose
The US State Laws view of the Content tab configures the on-banner text and controls used when the site's Consent Template (Law selector) is set to US State Laws, or the US State Laws half of the combined GDPR & US State Laws template. It governs the wording, toggles, and cookie-table labels for the opt-out banner's first layer (Cookie Notice) and second layer (Opt-out Center) — including Global Privacy Control (GPC) signal handling — plus the Cookie List embed and the two law-agnostic accordions (Revisit Consent Button, Blocked Content) that appear identically regardless of law state.

## Page structure
The Content tab opens on a **Consent Template card** at the top, containing a Law selector dropdown with three options — **GDPR**, **US State Laws**, **GDPR & US State Laws** — each with a help icon. Below the card, with US State Laws selected, five collapsible accordions are listed, collapsed by default:

1. **Cookie Notice** — the banner first layer (US State Laws variant — fewer controls than the GDPR variant; see Validation & edge cases).
2. **Opt-out Center** — the banner second layer. Replaces "Preference Centre" (the GDPR-only label) in the accordion list.
3. **Cookie List** — the cookie audit table shown inside the Opt-out Center (US State Laws variant — fewer controls than the GDPR variant).
4. **Revisit Consent Button** — the floating widget that lets a visitor reopen the banner after consenting. Identical under both law states.
5. **Blocked Content** — alt text shown on embedded third-party content (e.g. YouTube iframes) before consent. Identical under both law states.

When the Law selector is set to **GDPR & US State Laws** (Pro plan or higher required), a **Customise** sub-selector appears below the Consent Template row, defaulting to **GDPR**. Switching Customise to **US State Laws** swaps in this page's accordion set (Cookie Notice, Opt-out Center, Cookie List, Revisit Consent Button, Blocked Content) and updates the description text to reference CCPA/CPRA and related US state laws; switching back to GDPR restores the accordion set described in [content-gdpr.md](content-gdpr.md).

The banner preview panel (part of the page shell — see [display-layout.md](display-layout.md)) reflects edits in real time: Cookie Notice edits update the banner first layer preview; Opt-out Center and Cookie List edits update the banner second layer preview.

## Workflows

1. **View the Content section with US State Laws active**
   1. With Law selector set to US State Laws, observe the five accordions below the Consent Template card.
   2. All five — Cookie Notice, Opt-out Center, Cookie List, Revisit Consent Button, Blocked Content — are visible and collapsed. The "Preference Center" accordion present under GDPR is replaced by "Opt-out Center".

2. **Expand the Cookie Notice accordion (US State Laws variant)**
   1. Click "Cookie Notice" to expand it.
   2. The following are revealed: Title text field, Message text field (rich text editor), "Close [X] button" toggle (enabled by default — differs from the GDPR variant, where it is off by default), "Do Not Sell" link text field, "Cookie Policy" link toggle with URL text field, Custom logo text field (with upgrade icon), Disable CookieYes branding toggle (with upgrade icon). Unlike the GDPR Cookie Notice, there are no "Reject All" or "Customise" button toggles.
   3. Custom logo and Disable CookieYes branding both display an orange-crown upgrade icon, confirming they require an Ultimate plan.

3. **Edit Cookie Notice text fields (Ultimate plan, so Custom logo/branding are unlocked)**
   1. Title field is pre-filled with **"We value your privacy"** (same default as GDPR); edits appear on the banner first layer preview in real time.
   2. Message field is pre-filled with: *"This website or its third-party tools process personal data. You can opt out of the sale of your personal information by clicking on the 'Do Not Sell or Share My Personal Information' link."* Edits appear on the preview in real time.
   3. "Do Not Sell" link text field is pre-filled with **"Do Not Sell or Share My Personal Information"**; edits appear in real time.
   4. "Cookie Policy" link field (toggle enabled) is pre-filled with **"Cookie Policy"**; its URL field is empty with placeholder **"URL of your Cookie Policy"**.
   5. Custom logo field is pre-filled with **"#"**; entering a valid image URL displays the custom logo on the banner first layer preview.
   6. Click "Publish Changes" — all edits are saved and reflected on the live website.

4. **Toggle Cookie Notice links and branding on/off (US State Laws)**
   1. "Cookie Policy" link toggle is off by default; enabling it (with a valid URL) shows a "Cookie Policy" link that opens the cookie policy page in a new tab.
   2. "Disable CookieYes branding" toggle is off by default; enabling it removes the "Powered by CookieYes" branding from the banner second layer.
   3. Click "Publish Changes" — all toggle changes are saved and reflected on the live website.

5. **Expand the Opt-out Center accordion**
   1. Click "Opt-out Center" to expand it.
   2. The following are revealed: Title text field, Privacy overview text field (rich text editor), "Show more" button text field, "Show less" button text field, "Cancel" button text field, "Save My Preferences" button text field, "Respect Global Privacy Control" toggle, Global Privacy Control notice text field (rich text editor), "Opt out confirmation message" text field (rich text editor).
   3. On a Free or Basic plan, both the "Respect Global Privacy Control" toggle and the GPC notice field display an orange-crown upgrade icon, requiring a Pro plan or higher. On Pro or higher, both are unlocked with no upgrade icon.

6. **Edit Opt-out Center text fields (Pro plan or higher)**
   1. Title field is pre-filled with **"Opt-out Preferences"**; edits appear on the banner second layer preview in real time.
   2. Privacy overview field is pre-filled with: *"We use third-party cookies that help us analyse how you use this website, store your preferences, and provide the content and advertisements that are relevant to you. However, you can opt out of these cookies by checking "Do Not Sell or Share My Personal Information" and clicking the "Save My Preferences" button. Once you opt out, you can opt in again at any time by unchecking "Do Not Sell or Share My Personal Information" and clicking the "Save My Preferences" button."*
   3. "Show more" and "Show less" button fields are pre-filled with **"Show more"** and **"Show less"** respectively.
   4. "Cancel" button field is pre-filled with **"Cancel"**.
   5. "Save My Preferences" button field is pre-filled with **"Save My Preferences"**.
   6. "Opt out confirmation message" field is pre-filled with **"Your opt-out preference has been honored."**
   7. Click "Publish Changes" — all edits are saved and reflected on the live website.

7. **Enable "Respect Global Privacy Control" and configure the GPC notice**
   1. Toggle is off by default; while off, the Global Privacy Control notice text field is also disabled.
   2. The notice field is pre-filled with: *"Your opt-out settings for this website have been respected since we detected a Global Privacy Control signal from your browser and, therefore, you cannot change this setting."*
   3. Enabling the toggle turns it on and enables the notice field for editing.
   4. Click "Publish Changes" — on the live website, visitors whose browser sends a GPC signal see the "Do Not Sell or Share My Personal Information" checkbox pre-checked, with the GPC notice text displayed below it on the banner second layer.
   5. Editing the notice field and republishing updates the notice text shown to GPC-signaling visitors.

8. **Expand the Cookie List accordion (US State Laws variant)**
   1. Click "Cookie List" to expand it.
   2. The following are revealed: Embed code section with a Copy button, Cookie label text field, Duration label text field, Description label text field. Unlike the GDPR Cookie List, there is no "Show cookie list on banner" toggle, "Always Active" label field, or "No cookies to display" label field.

9. **Edit Cookie List table-header labels (US State Laws)**
   1. Cookie label field is pre-filled with **"Cookie"**.
   2. Duration field is pre-filled with **"Duration"**.
   3. Description field is pre-filled with **"Description"**.
   4. Click "Publish Changes" — all edits are saved and reflected on the live website's cookie table display.

10. **Copy the Cookie List embed code** *(shared behavior — identical under GDPR, see [content-gdpr.md](content-gdpr.md))*
    1. The Embed code section displays an HTML snippet, `<div class="cky-audit-table-element"></div>`, with a Copy button above it.
    2. Clicking the icon-only "Copy code" button copies the snippet to the clipboard.
    3. Pasting the snippet inside the `<body>` tag of a website page and saving it, then visiting that page live, displays a cookie audit table listing all cookies grouped by category. *(Confirmed directly in source case data for the GDPR view; the US State Laws Cookie List accordion also has an Embed code section per its own render case, so this behavior is treated as shared rather than re-verified separately.)*

11. **Edit the Blocked Content alt text** *(shared behavior — identical under GDPR)*
    1. Click "Blocked Content" to expand it — an "Alt text for blocked content" label with a help icon and a text field are displayed.
    2. The field is pre-filled with **"Please accept cookies to access this content"**.
    3. Editing and publishing updates the alt text shown on embedded content (e.g. YouTube iframes) on the live website before a visitor has given consent.

12. **Configure the Revisit Consent Button** *(shared behavior — identical under GDPR)*
    1. Click "Revisit Consent Button" to expand it — "Floating button" toggle, Position options (Left / Right), "Custom icon" text field with a premium icon, and "Text on hover" text field are revealed.
    2. "Floating button" toggle is on by default. With it on, accepting cookie consent on the live banner shows a floating revisit-consent button in the bottom-left corner of the website; clicking it reopens the banner second layer (Opt-out Center here, Preference Centre under GDPR) so the visitor can update their choices. Disabling the toggle and publishing removes the floating button from the live website.
    3. Position defaults to "Left"; selecting "Right" and publishing moves the floating button to the bottom-right corner on the live site.
    4. Custom icon field is pre-filled with **"#"** (placeholder) and requires an Ultimate plan to unlock; entering a valid image URL replaces the default revisit-button icon on the site after publishing.
    5. "Text on hover" field is pre-filled with **"Consent Preferences"** — this is the tooltip text shown on hover over the floating button on the live site.
    6. Click "Publish Changes" to save any edits made above.

13. **View premium-feature upgrade tooltips (below Ultimate plan)** *(shared behavior for Custom logo/branding — identical under GDPR; Custom icon tooltip is fully shared)*
    - Clicking the orange-crown upgrade icon on **Custom logo** (Cookie Notice) opens a tooltip: headline *"Make your banner uniquely yours with a custom brand logo"*, body *"Personalise your cookie banner with your brand logo for a seamless user experience."*, an "Available in: Ultimate plan" label, and a single "Upgrade now" button (no "Try Pro for Free" option, since this feature requires Ultimate specifically). Clicking "Upgrade now" navigates to the Plans/payment page.
    - Clicking the upgrade icon on **Disable CookieYes branding** (Cookie Notice) opens a tooltip: headline *"Remove CookieYes branding for a white-labeled banner"*, body *"Make your cookie banner fully white-labeled by removing the "Powered by CookieYes" tag."*, "Available in: Ultimate plan" label, and "Upgrade now" button, navigating to Plans on click.
    - Clicking the upgrade icon on **Custom icon** (Revisit Consent Button) opens a tooltip: headline *"Use a custom icon for your consent revisit widget"*, body *"Replace the default icon with a custom one that matches your website's design."*, "Available in: Ultimate plan" label, and "Upgrade now" button, navigating to Plans on click.

14. **Attempt to select the Pro-gated combined template (below Pro plan)** *(shared behavior — identical under GDPR)*
    1. Click the Consent Template dropdown — it opens showing GDPR, US State Laws, and GDPR & US State Laws. The "GDPR & US State Laws" option is visually dimmed (opacity-60) with an orange-crown badge next to its label.
    2. Hovering the crown badge shows a dark tooltip: *"Upgrade to Pro or a higher plan to unlock this feature."* (a simple informational tooltip, not the full headline/body/CTA upgrade dialog used for field-level premium features above).
    3. Clicking the "GDPR & US State Laws" option while below Pro does not switch the template — the dropdown closes and the active template is unchanged.

15. **Switch to the combined GDPR & US State Laws template (Pro plan or higher)** *(shared behavior — identical under GDPR)*
    1. Open the Consent Template dropdown and click "GDPR & US State Laws" — the template switches, and a "Customise" sub-selector appears below the Consent Template row, defaulting to "GDPR" (the accordion set in [content-gdpr.md](content-gdpr.md)).
    2. Clicking the Customise sub-selector and choosing "US State Laws" swaps in this page's Opt-out Center accordion set; the description text updates to reference CCPA/CPRA and related US state laws.
    3. Switching Customise back to "GDPR" restores the GDPR accordion set.

## Validation & edge cases
- **Close [X] button toggle default differs by law**: on under US State Laws by default, off under GDPR by default — do not assume shared default state for this control.
- **No Reject All / Customise toggles in US State Laws Cookie Notice**: these two controls exist only in the GDPR Cookie Notice variant; their absence here is expected, not a bug.
- **Cookie List: fewer controls than GDPR**: no "Show cookie list on banner" toggle, "Always Active" label, or "No cookies to display" label under US State Laws — the cookie list visibility and always-active/empty-state labeling are GDPR/Preference-Center-only concepts in the source data.
- **Respect Global Privacy Control plan boundary**: locked (orange-crown icon) on Free and Basic; unlocked with no icon on Pro and Ultimate. This is the only Content-tab control gated at the Pro tier rather than Ultimate.
- **GPC notice field is coupled to the toggle**: the notice text field is disabled whenever "Respect Global Privacy Control" is off, and only becomes editable once the toggle is enabled.
- **Custom logo / Disable CookieYes branding**: gated to Ultimate specifically — Pro plan does not unlock these (the upgrade tooltip omits the "Try Pro for Free" option that other Pro-gated features show).
- **GDPR & US State Laws template**: gated to Pro or higher; clicking the dimmed option below Pro is a no-op, not an error state — no validation message appears, the dropdown simply closes.
- **Revisit Consent Button and Blocked Content accordions are law-agnostic** — their content, controls, and default values are identical whether Law selector is set to GDPR or US State Laws (confirmed explicitly in source case preconditions).

## Related pages
- [content-gdpr.md](content-gdpr.md) — Content tab, GDPR variant (Preference Centre, Cookie Notice, Cookie List).
- [general.md](general.md) — General tab, where the Law selector itself lives.
- [display-layout.md](display-layout.md) — the Customization page shell (sidebar, tab navigation, preview panel, Publish Changes).
- [layout.md](layout.md) — Layout tab.
- [colours.md](colours.md) — Colours tab.
- [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) — full plan-gating CTA/tooltip matrix for the locked controls referenced above.

## Source
Derived from `ai-context/cases-cookie-banner-content.json` (31 TestRail cases total, split by law state). Drafted 2026-07-14, not yet live-verified against the QA app.
