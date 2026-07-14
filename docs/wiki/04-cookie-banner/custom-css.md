# Cookie Banner — Custom CSS

**Nav path:** Cookie Banner > Customization > Custom CSS
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Gated. The custom CSS editor is available on Basic, Pro, and Ultimate plans and is
locked on the Free plan. See "Validation & edge cases" below for the exact locked-state behavior,
and docs/wiki/11-billing-upgrade/plan-gates.md for the general upgrade-nudge/CTA pattern shared
across gated features.

## Purpose
The Custom CSS section lets a user inject their own CSS to style the cookie consent banner beyond
the built-in Colours/Layout options. Entered CSS applies live to the banner preview and, once
published, to the live banner on the user's website.

## Page structure
The Custom CSS section (under Cookie Banner > Customization sidebar) displays, top to bottom:

- **Consent Template card** — sits at the top of the section (its own content is out of scope for
  this page; not captured in source data — needs live verification).
- **"Add your custom css here" card** — below the Consent Template card, containing a CSS text
  area:
  - **Basic plan and higher:** the text area is enabled and editable, and the card label carries
    no premium/upgrade icon.
  - **Free plan:** the text area is disabled (cannot accept input) and a premium/upgrade icon is
    displayed next to the "Add your custom css here" label.
- **Banner preview canvas** — a live preview (right-hand main canvas, not a sidebar panel) that
  reflects entered custom CSS immediately, before publishing.
- **"Publish Changes" button** — enabled once valid custom CSS has been entered; saves the CSS to
  the live banner when clicked, then becomes disabled again.

Note: a separate side upgrade-nudge panel is known to also appear on this page but is a
confirmed/tracked bug and is intentionally not documented as expected behavior here.

## Workflows

**1. Viewing the Custom CSS section (paid plan)**
1. Start on Cookie Banner > Custom CSS section on a paid plan (Basic or higher).
2. Result: the "Add your custom css here" card is displayed with an editable CSS text area and no
   premium/upgrade icon on the label.

**2. Entering and applying custom CSS**
1. Start on Cookie Banner > Custom CSS section on a paid plan, with the "Add your custom css here"
   text area enabled.
2. Enter valid custom CSS into the text area.
3. Result: the banner preview canvas updates immediately to reflect the entered CSS, and the
   "Publish Changes" button becomes enabled.
4. Click "Publish Changes".
5. Result: the "Publish Changes" button becomes disabled (indicating the save succeeded) and the
   custom CSS is applied to the banner on the live website. A "Publishing Cookie Banner" dialog may
   appear afterward prompting script installation if the site's tracking script is not yet
   installed.

**3. Confirming custom CSS persists after reload**
1. Complete workflow 2 (enter custom CSS and click "Publish Changes") so the change is saved.
2. Reload the Cookie Banner page (or log out and log back in) and open the Custom CSS section
   again.
3. Result: the previously saved custom CSS is still present in the "Add your custom css here" text
   area, and the text area remains enabled.

## Validation & edge cases

- **Free plan — locked editor:** On the Free plan, the "Add your custom css here" card shows a
  premium/upgrade icon next to its label, and the CSS text area is disabled and does not accept any
  input.
- **Free plan — upgrade prompt:** Clicking the premium/upgrade icon opens an upgrade popover
  reading "Style your banner with custom CSS", "Available in: Basic, Pro and Ultimate plans", and a
  "Try Pro for free" call-to-action. (The CTA's destination/checkout flow is owned by
  docs/wiki/11-billing-upgrade/plan-gates.md — not exercised here to avoid starting a trial.)
- **Invalid CSS handling:** not captured in source data — needs live verification. No case in the
  source set exercises malformed/invalid CSS input or documents an error state for it.
- **Consent Template card contents/interaction:** not captured in source data — needs live
  verification.

## Related pages
- [Cookie Banner — General](general.md)
- [Cookie Banner — Colours](colours.md)
- [Plan Gates](../11-billing-upgrade/plan-gates.md)

## Source
Derived from `ai-context/cases-custom-css.json` (5 TestRail cases — thin, may need a live-crawl
follow-up). Drafted 2026-07-14, not yet live-verified against the QA app.
