# Cookie Banner — Colours

**Nav path:** Cookie Banner > Customization > Colours
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Partial — gating is specific to sub-features here, not the whole tab. The "Auto-generated" colour scheme option is locked on Free (unlocked Basic and higher). The per-component colour pickers ("Customise light/dark colours") also require Basic or higher on a Free account (see Validation & edge cases). For the general Free/paid plan model, see docs/wiki/billing-upgrade/plan-gates.md.

## Purpose
The Colours tab lets a user pick an overall colour scheme for the cookie banner (Light, Dark, or
Auto-generated from the connected website's own colours) and, on paid plans, override the colour
of individual banner components. Available colour components differ depending on which law/region
template (GDPR vs. US State Laws) is currently selected in the Consent Template card.

## Page structure
- **Consent Template card** at the top of the Colours tab, containing a law selector. It defaults
  to **GDPR**. Switching this selector to **US State Laws** changes which sub-components appear
  further down (see Workflows 4 vs. 6/7).
- **Colour scheme options**, directly below the Consent Template card: three choices — **Light**
  (selected by default), **Dark**, **Auto-generated**.
  - Auto-generated shows a premium/lock icon on Free plan; unlocked on Basic and higher.
- **Contextual "Customise ... colours" link**, shown below the scheme options and changing label
  with the active scheme: "Customise light colours", "Customise dark colours", or "Customise
  auto-generated colours".
- **"Customise colours" section** (revealed after clicking the contextual link above): activates
  a "Custom" sub-option and shows an accordion list of banner components to recolour. The
  accordion set depends on the active law template:
  - **Under GDPR:** Cookie Notice, Preference Center, Revisit Consent Button, Alt Text for Blocked
    Content.
  - **Under US State Laws:** Cookie Notice, Opt-out Center, Revisit Consent Button, Alt Text for
    Blocked Content (Opt-out Center replaces Preference Center and has 4 sub-sections: Checkbox,
    "Cancel" button, "Save My Preferences" button, "Opt-out confirmation message").
  - Each accordion item exposes per-element colour pickers (background/border/text, as applicable
    per element) with hex-value defaults — see Workflows for exact values.
- **Banner preview** in the sidebar updates live as scheme or individual colours change.
- **"Publish Changes" button**: commits the current colour configuration to the live banner.

## Workflows

1. **View default Colours tab state** *(smoke)*
   - Land on Cookie Banner > Customisation sidebar > Colours tab.
   - "Light", "Dark", "Auto-generated" scheme options are visible; **Light** is selected by
     default.
   - The Consent Template card's law selector shows **GDPR** by default.
   - With Light selected, a **"Customise light colours"** link is visible below the scheme
     options.
   - Auto-generated is locked (premium icon) on Free plan; unlocked on Basic+.

2. **Switch to Dark scheme**
   - Click the **"Dark"** colour option.
   - Dark is selected; the banner preview updates to the dark colour scheme.
   - The link below the scheme options changes to **"Customise dark colours"**.

3. **Switch to Auto-generated scheme**
   - Precondition: the account's connected domain has been scanned and website colours are
     available. Without scan data, selecting Auto-generated silently reverts to the Dark scheme.
   - Click **"Auto-generated"**.
   - Auto-generated is selected; the banner preview updates to a scheme derived from the
     connected website's colours.
   - A **"Customise auto-generated colours"** link appears below the scheme options.

4. **Customise light colours under GDPR** (requires Basic plan or higher — see Validation & edge
   cases)
   - Precondition: law is GDPR (default), Light is selected (default), "Customise light colours"
     link visible.
   - Click **"Customise light colours"**. The "Custom" sub-option activates; a "Customise
     colours" section appears with four accordions: **Cookie Notice, Preference Center, Revisit
     Consent Button, Alt Text for Blocked Content**.
   - Expand **Cookie Notice** — default light values:
     - Banner: Background `#FFFFFF`, Border `#F4F4F4`, Title `#212121`, Message `#212121`
     - "Accept All" button: Background `#1863DC`, Border `#1863DC`, Text `#FFFFFF`
     - "Reject All" button: Background `#1863DC`, Border `#1863DC`, Text `#FFFFFF`
     - "Customise" button: Background `TRANSPARENT`, Border `#1863DC`, Text `#1863DC`
   - Changing a value under Cookie Notice updates the banner preview for that element.
   - Expand **Preference Center** — default values:
     - Toggle switch: Enabled `#1863DC`, Disabled `#D0D5D2`
     - "Save My Preferences" button: Background `#1863DC`, Border `#1863DC`, Text `#FFFFFF`
   - Changing a value under Preference Center updates the preview accordingly.
   - Expand **Revisit Consent Button** — "Floating button": Background `#0056A7`.
   - Expand **Alt Text for Blocked Content** — Background `#000000`, Border `#000000`, Text
     `#FFFFFF`.
   - Click **"Publish Changes"** — the customised colours are saved and applied to the live
     banner.

5. **Customise dark colours under GDPR** (requires Basic plan or higher)
   - Same flow as Workflow 4 but with Dark selected and "Customise dark colours" clicked.
     Default dark values:
     - Banner: Background `#121212`, Border `#2A2A2A`, Title `#D0D0D0`, Message `#D0D0D0`
     - "Accept All" / "Reject All" buttons: Background `#1578F7`, Border `#1578F7`, Text `#FFFFFF`
     - "Customise" button: Background `TRANSPARENT`, Border `#D0D0D0`, Text `#D0D0D0`
     - Preference Center toggle: Enabled `#1578F7`, Disabled `#D0D5D2`; "Save My Preferences":
       Background `#1578F7`, Border `#1578F7`, Text `#FFFFFF`
     - Revisit Consent Button floating button: Background `#0056A7` (same as light)
     - Alt Text for Blocked Content: Background `#000000`, Border `#000000`, Text `#FFFFFF`
       (same as light)
   - Publish Changes saves and applies the customised dark colours.

6. **Customise light colours under US State Laws** (requires Basic plan or higher)
   - Precondition: law selector set to **US State Laws**, Light selected, "Customise light
     colours" link visible.
   - Click **"Customise light colours"** — accordions are **Cookie Notice, Opt-out Center,
     Revisit Consent Button, Alt Text for Blocked Content** (Opt-out Center replaces Preference
     Center; Cookie Notice shows a "Do Not Sell" link instead of a "Customise" button).
   - Expand **Cookie Notice** — Banner: Background `#FFFFFF`, Border `#F4F4F4`, Title `#212121`,
     Message `#212121`; "Do Not Sell" link Text `#1863DC`.
   - Expand **Opt-out Center** — Checkbox: Enabled `#1863DC`, Disabled `#FFFFFF`; "Cancel"
     button: Background `#FFFFFF`, Border `#949494`, Text `#595959`; "Save My Preferences":
     Background `#1863DC`, Border `#1863DC`, Text `#FFFFFF`.
   - Expand **Revisit Consent Button** — Floating button: Background `#0056A7`.
   - Expand **Alt Text for Blocked Content** — Background `#000000`, Border `#000000`, Text
     `#FFFFFF`.
   - Click **"Publish Changes"** to save.

7. **Customise dark colours under US State Laws** (requires Basic plan or higher)
   - Same accordions as Workflow 6 but Dark selected. Values differ from light:
     - Cookie Notice: Banner Background `#121212`, Border `#2A2A2A`, Title `#D0D0D0`, Message
       `#D0D0D0`; "Do Not Sell" link Text `#609FFF`.
     - Opt-out Center: Checkbox Enabled `#1578F7`, Disabled `#FFFFFF`; "Cancel" button Background
       `TRANSPARENT` (differs from light's `#FFFFFF`), Border `#949494`, Text `#A1A1A1`; "Save My
       Preferences" Background `#1578F7`, Border `#1578F7`, Text `#FFFFFF`.
     - Revisit Consent Button / Alt Text for Blocked Content: same as light (`#0056A7`;
       `#000000`/`#000000`/`#FFFFFF`).
   - Publish Changes saves the customised dark colours.

8. **Customise auto-generated colours**
   - Precondition: "Auto-generated" selected, "Customise auto-generated colours" link visible.
   - Click the link — the "Custom" sub-option activates and a "Customise colours" section
     appears pre-populated with the auto-detected colour values (no fixed hex defaults — values
     are dynamically derived from the connected website, unlike Light/Dark).
   - Change one or more values — the override is accepted and the banner preview updates.
   - Click "Publish Changes" — the overridden colours (not the auto-detected values) are applied
     to the live banner.

9. **Configure Opt-out confirmation message colours (US State Laws only)**
   - Precondition: law is US State Laws; "Customise light colours" or "Customise dark colours"
     has been clicked so the "Customise colours" section is visible.
   - Expand **Opt-out Center** — it has four sub-sections: Checkbox, "Cancel" button, "Save My
     Preferences" button, and **"Opt-out confirmation message"**.
   - Scroll to "Opt-out confirmation message" — default colours: Background `#E5F4EF`, Icon
     `#00754E`, Text `#14142A`, Subtext `#4E4B66`. These values are identical in both Light and
     Dark custom modes.
   - Changing a value updates the preview for the confirmation message element.

## Validation & edge cases
- **Auto-generated without scan data**: if the connected domain hasn't been scanned (no website
  colours available), selecting "Auto-generated" silently reverts to the Dark scheme — no error
  is shown.
- **Auto-generated locked on Free plan**: shown with a premium icon; unlocked Basic and higher.
  See docs/wiki/billing-upgrade/plan-gates.md.
- **Per-component pickers require Basic+ (undocumented precondition gap)**: on a Free-plan
  account, clicking "Customise light/dark colours" does **not** open the per-component picker at
  all. Instead a different upgrade modal appears — headline "Design a banner that blends
  perfectly with your site", "Available in: Basic, Pro and Ultimate plans", CTA "Try Pro for
  free". This applies to Workflows 4, 5, 6, and 7 (GDPR/US State Laws, Light/Dark) uniformly; the
  source test cases for these workflows do not name a plan tier in their preconditions, so treat
  "Basic or higher" as an implicit requirement whenever driving this flow on an unverified account.
- **Custom CSS upgrade nudge on Free plan (known documentation/scope issue — do not treat as
  verified Colours-tab behavior)**: Two source cases describe a nudge — feature illustration,
  headline "Put your banner in the spotlight with custom CSS", "Available in: All premium plans",
  buttons "Try Pro for free" and "Dismiss" — as appearing on the Colours tab when "Dark" is
  selected on a Free plan, and as dismissible for the rest of the browser session. Live
  verification (2026-07-13) confirmed the nudge's copy/buttons are real and accurate, but found
  the *trigger and location claimed by these cases are wrong*: the nudge does not appear on the
  Colours tab at all (neither Light nor Dark), regardless of selection. It actually lives on the
  Custom CSS tab (see docs/wiki/cookie-banner/custom-css.md), shown unconditionally to Free
  accounts there. This is tracked as a known bug/scope question, not resolved as of this writing —
  do not cite "selecting Dark shows the Custom CSS nudge" as confirmed Colours-tab behavior.
- **Role permission on the (misattributed) nudge**: for Admin/Editor, the nudge's "Try it now"
  button is disabled with tooltip "Only account owner can change plan" (Account Owner can click
  it). This divergence is a Permissions-section (14) case, not Colours-specific — same caveat
  about the nudge's real location/trigger applies.
- **Colour components differ by law template**: do not assume the same accordion set applies
  under GDPR and US State Laws — Preference Center (GDPR) vs. Opt-out Center (US State Laws) are
  distinct components with different default hex values and different sub-elements ("Customise"
  button vs. "Do Not Sell" link; Toggle switch vs. Checkbox). See Workflows 4/5 vs. 6/7.
- **Dark-mode "Cancel" button background differs from light-mode**: under US State Laws, the
  Opt-out Center "Cancel" button is Background `#FFFFFF` in Light custom mode but Background
  `TRANSPARENT` in Dark custom mode (Border/Text also differ: `#949494`/`#595959` light vs.
  `#949494`/`#A1A1A1` dark).
- No invalid-hex-input or colour-picker-validation-error case exists in the source data (not
  captured in source data — needs live verification).

## Related pages
- docs/wiki/cookie-banner/general.md
- docs/wiki/cookie-banner/layout.md
- docs/wiki/cookie-banner/custom-css.md
- docs/wiki/billing-upgrade/plan-gates.md

## Source
Derived from `ai-context/cases-colours.json` (12 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
