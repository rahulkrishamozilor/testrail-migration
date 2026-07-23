# Cookie Banner — Content (GDPR)

**Nav path:** Cookie Banner > Customization > Content > GDPR (Content is the third of five sidebar tabs — General, Layout, Content, Colours, Custom CSS — see [display-layout.md](display-layout.md) for the shell; GDPR is the default Law selector state)
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Partial — the Content tab itself is not plan-gated. Individual controls within it are:
- Cookie Notice: **Custom logo** and **Disable CookieYes branding** require an Ultimate plan (orange crown icon when locked).
- Revisit Consent Button: **Custom icon** requires an Ultimate plan (shared with the US State Laws view — see [content-us-state-laws.md](content-us-state-laws.md)).
- The **GDPR & US State Laws** combined Consent Template option requires a Pro plan or higher.
Full lock-state/tooltip/CTA matrix: [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md).

## Purpose
The GDPR view of the Content tab configures the on-banner text and controls used when the site's Consent Template (Law selector) is set to GDPR, or the GDPR half of the combined GDPR & US State Laws template. It governs the wording, toggles, and cookie-table labels for the opt-in banner's first layer (Cookie Notice) and second layer (Preference Centre), plus the Cookie List embed and the two law-agnostic accordions (Revisit Consent Button, Blocked Content) that appear identically regardless of law state.

## Page structure
The Content tab opens on a **Consent Template card** at the top, containing a Law selector dropdown with three options — **GDPR**, **US State Laws**, **GDPR & US State Laws** — each with a help icon. GDPR is selected by default. Below the card, five collapsible accordions are listed, collapsed by default:

1. **Cookie Notice** — the banner first layer.
2. **Preference Centre** — the banner second layer (GDPR-only label; replaced by "Opt-out Center" under US State Laws).
3. **Cookie List** — the cookie audit table shown inside the Preference Centre.
4. **Revisit Consent Button** — the floating widget that lets a visitor reopen the banner after consenting. Identical under both law states.
5. **Blocked Content** — alt text shown on embedded third-party content (e.g. YouTube iframes) before consent. Identical under both law states.

When the Law selector is set to **GDPR & US State Laws** (Pro plan or higher required), a **Customise** sub-selector appears below the Consent Template row, defaulting to **GDPR**. With Customise set to GDPR, this page's accordion set (Cookie Notice, Preference Centre, Cookie List, Revisit Consent Button, Blocked Content) is what renders; switching Customise to **US State Laws** swaps in the accordion set described in [content-us-state-laws.md](content-us-state-laws.md) (Cookie Notice, Opt-out Center, Cookie List, Revisit Consent Button, Blocked Content) and updates the description text to reference CCPA/CPRA and related US state laws.

The banner preview panel (part of the page shell — see [display-layout.md](display-layout.md)) reflects edits in real time: Cookie Notice edits update the banner first layer preview; Preference Centre and Cookie List edits update the banner second layer preview.

## Workflows

1. **View the Content section with GDPR active**
   1. With GDPR selected in the Law selector (the default), observe the five accordions below the Consent Template card.
   2. All five — Cookie Notice, Preference Centre, Cookie List, Revisit Consent Button, Blocked Content — are visible and collapsed.

2. **Expand the Cookie Notice accordion**
   1. Click "Cookie Notice" to expand it.
   2. The following are revealed: Title text field, Message text field (rich text editor), Close [X] button toggle, "Accept All" button text field, "Reject All" button toggle with text field, "Customise" button toggle with text field, "Cookie Policy" link toggle with URL text field, Custom logo text field, Disable CookieYes branding toggle. The Custom logo and Disable CookieYes branding controls each display an orange-crown upgrade icon, confirming they require an Ultimate plan.

3. **Edit Cookie Notice text fields (Ultimate plan, so Custom logo/branding are unlocked)**
   1. Title field is pre-filled with **"We value your privacy"**; edits appear on the banner first layer preview in real time.
   2. Message field is pre-filled with: *"We use cookies to enhance your browsing experience, serve personalised ads or content, and analyse our traffic. By clicking 'Accept All', you consent to our use of cookies."* Edits appear on the preview in real time.
   3. "Accept All" button field is pre-filled with **"Accept All"**.
   4. "Reject All" button field (toggle on by default) is pre-filled with **"Reject All"**.
   5. "Customise" button field (toggle on by default) is pre-filled with **"Customise"**.
   6. "Cookie Policy" link field (toggle off by default) is pre-filled with **"Cookie Policy"**; its URL field is empty with placeholder **"URL of your Cookie Policy"**.
   7. Custom logo field is pre-filled with **"#"**; entering a valid image URL displays the custom logo on the banner first layer preview.
   8. Click "Publish Changes" — all edits are saved and reflected on the live website.

4. **Enable "Support IAB TCF v2.3" and observe the Message field lock**
   1. With "Support IAB TCF v2.3" enabled (General tab), the Message field in Cookie Notice becomes disabled (non-editable) and is pre-filled with the IAB TCF-approved text: *"We and our {{count}} partners use cookies and other tracking technologies to improve your experience on our website. We may store and/or access information on a device and process personal data, such as your IP address and browsing data, for personalised advertising and content, advertising and content measurement, audience research and services development. Additionally, we may utilize precise geolocation data and identification through device scanning.*

      *Please note that your choices apply across all our subdomains. Once you give consent, a floating button will appear at the bottom of your screen, allowing you to change or withdraw your consent at any time. We respect your choices and are committed to providing you with a transparent and secure browsing experience."* — rendered as a read-only rich text (Quill) editor.
   2. Attempting to click inside the field and type has no effect — no input is accepted while IAB TCF v2.3 is active.

5. **Toggle Cookie Notice buttons and links on/off**
   1. "Close [X] button" toggle is off by default; enabling it shows an "X" close button in the top-left corner of the banner first layer preview.
   2. "Reject All" toggle is on by default; disabling it removes the "Reject All" button from the preview.
   3. "Customise" toggle is on by default; disabling it removes the "Customise" button from the preview.
   4. "Cookie Policy" link toggle is off by default; enabling it (with a valid URL entered) shows a "Cookie Policy" link that opens the cookie policy page in a new tab.
   5. "Disable CookieYes branding" toggle is off by default; enabling it removes the "Powered by CookieYes" branding from the banner second layer preview.
   6. Click "Publish Changes" — all toggle changes are saved and reflected on the live website.

6. **Expand the Preference Centre accordion**
   1. Click "Preference Centre" to expand it.
   2. The following are revealed: Title text field, Privacy overview text field, Show Google Privacy Policy toggle, "Save My Preferences" button text field, "Show more" button text field, "Show less" button text field.

7. **Edit Preference Centre text fields**
   1. Title field is pre-filled with **"Customise Consent Preferences"**; edits appear on the banner second layer preview in real time.
   2. Privacy overview field is pre-filled with: *"We use cookies to help you navigate efficiently and perform certain functions. You will find detailed information about all cookies under each consent category below.*

      *The cookies that are categorised as "Necessary" are stored on your browser as they are essential for enabling the basic functionalities of the site.*

      *We also use third-party cookies that help us analyse how you use this website, store your preferences, and provide the content and advertisements that are relevant to you. These cookies will only be stored in your browser with your prior consent.*

      *You can choose to enable or disable some or all of these cookies but disabling some of them may affect your browsing experience."*
   3. "Save My Preferences" button field is pre-filled with **"Save My Preferences"**.
   4. "Show more" and "Show less" button fields are pre-filled with **"Show more"** and **"Show less"** respectively.
   5. Click "Publish Changes" — all edits are saved and reflected on the live website.

8. **Enable "Show Google Privacy Policy" in the Preference Centre**
   1. Toggle is off by default. Enabling it reveals three new fields: Message text field, Link text text field, URL text field.
   2. Message field is pre-filled with **"For more information on how Google's third-party cookies operate and handle your data, see:"** — this message plus the Google Privacy Policy link appears below the privacy overview on the banner second layer preview.
   3. Link text field is pre-filled with **"Google Privacy Policy"**.
   4. URL field is pre-filled with **"https://business.safety.google/privacy"**; editing it and clicking the link in the preview opens the new URL in a new tab.
   5. Click "Publish Changes" — the Google Privacy Policy link appears on the live website's banner second layer.

9. **Expand the Cookie List accordion**
   1. Click "Cookie List" to expand it.
   2. The following are revealed: "Show cookie list on banner" toggle, Embed code section with a Copy button, Cookie label text field, Duration label text field, Description label text field, "Always Active" label text field, "No cookies to display" label text field.

10. **Toggle cookie list visibility in the Preference Centre**
    1. "Show cookie list on banner" toggle is on by default; a cookie list is visible under each cookie category on the banner second layer preview.
    2. Disabling it removes the cookie list from under each category in the preview.
    3. Click "Publish Changes" — the cookie list no longer appears under cookie categories on the live website's banner second layer.

11. **Edit Cookie List table-header labels**
    1. Cookie label field is pre-filled with **"Cookie"**.
    2. Duration field is pre-filled with **"Duration"**.
    3. Description field is pre-filled with **"Description"**.
    4. "Always Active" label field is pre-filled with **"Always Active"** — appears next to non-optional cookie categories on the preview.
    5. "No cookies to display" label field is pre-filled with **"No cookies to display."** (the trailing period is part of the default text).
    6. Click "Publish Changes" — all edits are saved and reflected on the cookie table in the live website's banner second layer.

12. **Copy the Cookie List embed code** *(shared behavior — identical under US State Laws, see [content-us-state-laws.md](content-us-state-laws.md))*
    1. The Embed code section displays an HTML snippet, `<div class="cky-audit-table-element"></div>`, with a Copy button above it.
    2. Clicking the icon-only "Copy code" button copies the snippet to the clipboard.
    3. Pasting the snippet inside the `<body>` tag of a website page and saving it, then visiting that page live, displays a cookie audit table listing all cookies grouped by category.

13. **Edit the Blocked Content alt text** *(shared behavior — identical under US State Laws)*
    1. Click "Blocked Content" to expand it — an "Alt text for blocked content" label with a help icon and a text field are displayed.
    2. The field is pre-filled with **"Please accept cookies to access this content"**.
    3. Editing and publishing updates the alt text shown on embedded content (e.g. YouTube iframes) on the live website before a visitor has given consent.

14. **Configure the Revisit Consent Button** *(shared behavior — identical under US State Laws)*
    1. Click "Revisit Consent Button" to expand it — "Floating button" toggle, Position options (Left / Right), "Custom icon" text field with a premium icon, and "Text on hover" text field are revealed.
    2. "Floating button" toggle is on by default. With it on, accepting cookie consent on the live banner shows a floating revisit-consent button in the bottom-left corner of the website; clicking it reopens the banner second layer (Preference Centre here, Opt-out Center under US State Laws) so the visitor can update their choices. Disabling the toggle and publishing removes the floating button from the live website.
    3. Position defaults to "Left"; selecting "Right" and publishing moves the floating button to the bottom-right corner on the live site.
    4. Custom icon field is pre-filled with **"#"** (placeholder) and requires an Ultimate plan to unlock; entering a valid image URL replaces the default revisit-button icon on the site after publishing.
    5. "Text on hover" field is pre-filled with **"Consent Preferences"** — this is the tooltip text shown on hover over the floating button on the live site.
    6. Click "Publish Changes" to save any edits made above.

15. **View premium-feature upgrade tooltips (below Ultimate plan)** *(shared behavior for Custom logo/branding — identical under US State Laws; Custom icon tooltip is fully shared)*
    - Clicking the orange-crown upgrade icon on **Custom logo** (Cookie Notice) opens a tooltip: headline *"Make your banner uniquely yours with a custom brand logo"*, body *"Personalise your cookie banner with your brand logo for a seamless user experience."*, an "Available in: Ultimate plan" label, and a single "Upgrade now" button (no "Try Pro for Free" option, since this feature requires Ultimate specifically). Clicking "Upgrade now" navigates to the Plans/payment page.
    - Clicking the upgrade icon on **Disable CookieYes branding** (Cookie Notice) opens a tooltip: headline *"Remove CookieYes branding for a white-labeled banner"*, body *"Make your cookie banner fully white-labeled by removing the "Powered by CookieYes" tag."*, "Available in: Ultimate plan" label, and "Upgrade now" button, navigating to Plans on click.
    - Clicking the upgrade icon on **Custom icon** (Revisit Consent Button) opens a tooltip: headline *"Use a custom icon for your consent revisit widget"*, body *"Replace the default icon with a custom one that matches your website's design."*, "Available in: Ultimate plan" label, and "Upgrade now" button, navigating to Plans on click.

16. **Attempt to select the Pro-gated combined template (below Pro plan)** *(shared behavior — identical under US State Laws)*
    1. Click the Consent Template dropdown — it opens showing GDPR, US State Laws, and GDPR & US State Laws. The "GDPR & US State Laws" option is visually dimmed (opacity-60) with an orange-crown badge next to its label.
    2. Hovering the crown badge shows a dark tooltip: *"Upgrade to Pro or a higher plan to unlock this feature."* (a simple informational tooltip, not the full headline/body/CTA upgrade dialog used for field-level premium features above).
    3. Clicking the "GDPR & US State Laws" option while below Pro does not switch the template — the dropdown closes and the active template is unchanged.

17. **Switch to the combined GDPR & US State Laws template (Pro plan or higher)** *(shared behavior — identical under US State Laws)*
    1. Open the Consent Template dropdown and click "GDPR & US State Laws" — the template switches, and a "Customise" sub-selector appears below the Consent Template row, defaulting to "GDPR" (this page's accordion set).
    2. Clicking the Customise sub-selector and choosing "US State Laws" swaps in the Opt-out Center accordion set (see [content-us-state-laws.md](content-us-state-laws.md)); the description text updates to reference CCPA/CPRA and related US state laws.
    3. Switching Customise back to "GDPR" restores this page's accordion set.

## Validation & edge cases
- **"No cookies to display." label**: default value includes a trailing period — do not treat it as truncated or as a typo when comparing against live app text.
- **IAB TCF v2.3 lock**: while "Support IAB TCF v2.3" is enabled (General tab), the Cookie Notice Message field is fully non-editable, not just visually greyed — typing inside it has no effect.
- **Custom logo / Disable CookieYes branding**: gated to Ultimate specifically — Pro plan does not unlock these (the upgrade tooltip omits the "Try Pro for Free" option that other Pro-gated features show).
- **GDPR & US State Laws template**: gated to Pro or higher; clicking the dimmed option below Pro is a no-op, not an error state — no validation message appears, the dropdown simply closes.
- **Cookie Policy link toggle**: off by default in Cookie Notice; must be enabled and given a valid URL before the link appears on the live banner.
- **Revisit Consent Button and Blocked Content accordions are law-agnostic** — their content, controls, and default values are identical whether Law selector is set to GDPR or US State Laws (confirmed explicitly in source case preconditions).

## Related pages
- [content-us-state-laws.md](content-us-state-laws.md) — Content tab, US State Laws variant (Opt-out Center, Cookie Notice, Cookie List).
- [general.md](general.md) — General tab, where the Law selector itself lives.
- [display-layout.md](display-layout.md) — the Customization page shell (sidebar, tab navigation, preview panel, Publish Changes).
- [layout.md](layout.md) — Layout tab.
- [colours.md](colours.md) — Colours tab.
- [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) — full plan-gating CTA/tooltip matrix for the locked controls referenced above.

## Source
Derived from `ai-context/cases-cookie-banner-content.json` (31 TestRail cases total, split by law state). Drafted 2026-07-14, not yet live-verified against the QA app.
