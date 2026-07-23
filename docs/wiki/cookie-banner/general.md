# Cookie Banner > Customization Sidebar > General

**Nav path:** Cookie Banner > Customization > General tab (first of five sidebar tabs: General, Layout, Content, Colours, Custom CSS — see [display-layout.md](display-layout.md) for the shell)
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Partial — see below for what the source cases confirm; full CTA/plan matrix at [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md).

- Free and Basic plans: the "GDPR & US State Laws" Law selector option, the "EU Countries & UK" / "Select Countries" (GDPR) or "United States" / "Select Countries" (US State Laws) Geo-target options, and the "Support IAB TCF v2.3" toggle are all locked behind an upgrade icon/crown icon.
- Pro and Ultimate plans: all three are unlocked and interactive.
- Basic-plan upgrade tooltips use an "Upgrade now" CTA; Free-plan tooltips use a "Try Pro for free" CTA (per Plan Gates cases referenced in source notes — exact CTA text differences are tracked in plan-gates.md, not duplicated here).

## Purpose
The General tab is where a site owner picks the legal framework the banner is built on (Consent Template / Law selector), restricts which visitors see it (Geo-target), turns on IAB TCF v2.3 vendor-consent signaling, and tunes advanced behavior like consent expiration and page reload on consent.

## Page structure
The General tab renders four cards/controls, top to bottom:

1. **Consent Template card** — top of the section. Contains the **Law selector** dropdown on its right-hand side with three options, each with a help icon: **GDPR**, **US State Laws**, **GDPR & US State Laws**. Defaults to **GDPR**.
   - When **GDPR & US State Laws** is selected, a **Customize** sub-dropdown appears inside the Consent Template card with two options, **GDPR** and **US State Laws**, defaulting to **GDPR**. This sub-dropdown lets the user preview/configure each half of the combined template independently.
2. **Geo-target banner card** — directly below the Consent Template card. Its option set depends on the active law (see Workflows below), each rendered as a radio button, defaulting to **Worldwide**.
   - Under **US State Laws** only, two additional controls appear below the Geo-target card: a **Show banner** toggle (enabled by default) and a **"Do Not Sell" link card** containing an HTML code snippet in a text area with a **Copy** button at the top-right of the snippet.
3. **Support IAB TCF v2.3 card** — below the Geo-target card. Contains the **Support IAB TCF v2.3** toggle (off by default), plus two dependent toggles rendered below it: **Support Google's Additional Consent Mode** and **Enable Google's Advertiser Consent Mode**. Both dependent toggles are visible but uninteractable while Support IAB TCF v2.3 is off.
4. **Show advanced settings** control — the last item in the section. Expanding it reveals two additional controls: a **Consent expiration (days)** numeric field (defaults to 365) and a **Reload page on consent action** toggle (off by default).

The banner preview panel (to the right of the sidebar, part of the page shell — see [display-layout.md](display-layout.md)) reflects the active Law selector state: it shows the opt-in template under GDPR and the opt-out template under US State Laws, and it displays the IAB TCF v2.3 banner once that toggle is enabled.

## Workflows

1. **Switch the active law to US State Laws**
   1. Click the Law selector dropdown in the Consent Template card.
   2. Select "US State Laws". The Law selector label updates to "US State Laws" and the banner preview switches to the opt-out template.
   3. Click "Publish Changes". The US State Laws opt-out banner becomes active on the live website.

2. **Switch to combined GDPR & US State Laws mode**
   1. Click the Law selector dropdown and select "GDPR & US State Laws". The label updates and a "Customize" sub-dropdown appears.
   2. Open the Customize sub-dropdown — it lists GDPR and US State Laws, defaulting to GDPR (opt-in template shown in preview).
   3. Select "US State Laws" in the Customize sub-dropdown — the preview switches to the opt-out template.
   4. Click "Publish Changes" — both the GDPR and US State Laws banners are activated on the site.
   5. Geo-target options also respond to the Customize sub-dropdown state: with Customize=GDPR, the Geo-target card shows Worldwide / EU Countries & UK / Select countries (no United States); switching Customize to US State Laws changes it to Worldwide / United States / Select countries (no EU Countries & UK). Worldwide stays selected by default in both states. This is a distinct interaction from the plain single-law Geo-target case below — the option set toggles live as the Customize sub-dropdown changes, not a merged list of all four regions.

3. **Restrict the banner by geography (single-law mode)**
   - Under GDPR: Geo-target card offers Worldwide (default), EU Countries & UK, Select Countries.
   - Under US State Laws: Geo-target card offers Worldwide (default), United States, Select Countries.
   - Selecting "EU Countries & UK" (GDPR) or "United States" (US State Laws) and clicking "Publish Changes" restricts the live banner to that region.
   - Selecting "Select Countries" (either law) opens a country-selection dropdown with country names and checkboxes; selected countries show as checked. Publishing restricts the banner to only the checked countries.

4. **Handle validation when Select Countries has no countries chosen**
   1. With "Select Countries" selected under Geo-target and no countries checked, click "Publish Changes".
   2. A validation message "Please select countries" appears below the Select Countries option and the changes are not saved.

5. **Disable the banner for US State Laws visitors**
   1. Under US State Laws, disable the "Show banner" toggle below the Geo-target card.
   2. The US State Laws banner is hidden and the banner preview shows the alert: "The US State Laws has been disabled. You can enable it from 'General', if needed."
   3. Click "Publish Changes" — the US State Laws banner no longer appears on the live website.

6. **Copy the Do Not Sell HTML snippet (US State Laws only)**
   1. In the "Do Not Sell" link card, click the "Copy" button at the top-right of the code text area.
   2. The HTML snippet is copied to the clipboard. No "Copied!" or other success text appears anywhere on the page (confirmed live — this component does not surface a copy-confirmation indicator).

7. **Enable IAB TCF v2.3 and its dependent consent-mode toggles**
   1. Enable the "Support IAB TCF v2.3" toggle. The IAB TCF v2.3 banner appears in the preview, and the "Support Google's Additional Consent Mode" and "Enable Google's Advertiser Consent Mode" toggles become interactable.
   2. Enable "Support Google's Additional Consent Mode" — the partner count shown in the IAB TCF v2.3 preview banner increases and a Google Ad Tech providers list appears.
   3. Enable "Enable Google's Advertiser Consent Mode" — the toggle switches on.
   4. Click "Publish Changes" — the IAB TCF v2.3 banner becomes active on the live website.

8. **Configure advanced settings**
   1. Click "Show advanced settings" at the bottom of the General section — the "Consent expiration (days)" field and "Reload page on consent action" toggle appear.
   2. The Consent expiration field defaults to 365; publishing with this value means the banner reappears to a visitor 365 days after they gave consent.
   3. Enabling "Reload page on consent action" and publishing causes the live page to reload immediately after a visitor gives or declines consent.

9. **Trigger upgrade nudges on locked options (Free/Basic plans)**
   - Clicking the crown/upgrade icon next to a locked Geo-target option ("EU Countries & UK", "Select Countries", or "United States" depending on active law) opens an upgrade nudge headlined "Display your banner only in select countries and regions" with an upgrade CTA.
   - Clicking the upgrade icon next to "Support IAB TCF v2.3" opens an upgrade nudge headlined "Comply with IAB TCF and Google's requirements" (Free-plan tooltip additionally includes the body text "Communicate user consent status to IAB vendors to enable Google ad personalization in EEA and the UK." per the Basic-plan variant case) with an upgrade CTA that navigates to the Plans page.
   - Exact CTA label differs by plan tier (Basic: "Upgrade now"; Free: "Try Pro for free" per Plan Gates cases) — see [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) for the full matrix; not duplicated here per the section-ownership convention.

## Validation & edge cases

- **Select Countries with none selected**: publishing is blocked with the validation message "Please select countries" shown below the Select Countries option.
- **Consent expiration (days) field**: rejects non-numeric input outright (letters/special characters are not accepted as you type). Out-of-range numeric values (e.g. 0 or 10000) trigger the validation message "Please enter a value between 1 and 9999" below the field.
- **Law selector option set is fixed**: exactly three options — GDPR, US State Laws, GDPR & US State Laws — each with a help icon, regardless of plan (the combined option itself is plan-gated, not the list visibility).
- **Geo-target option set depends on both the active law and, in combined mode, the Customize sub-dropdown state** — see Workflow 2 above. Do not assume a merged 4-region list is ever shown at once; that was an earlier incorrect assumption corrected via live verification (see `cases-general.json` audit note on case 36823).
- **IAB TCF v2.3 label**: the source cases and this app consistently use "Support IAB TCF v2.3" as the live product label. `testrail-suite-v2.md`'s section outline still says "IAB TCF v2.2" — that is a stale doc reference to an earlier product version, not a discrepancy in the app itself.
- **Show banner toggle and Do Not Sell link card**: only confirmed to appear under US State Laws in the source cases. No equivalent GDPR-mode behavior is captured here — do not assume parity without live verification.
- **Plan gating boundary**: Free and Basic plans both lock the same three controls (combined Law option, restrictive Geo-target options, IAB TCF v2.3), but their upgrade-tooltip CTA wording differs (Free: "Try Pro for free"; Basic: "Upgrade now"). Pro and Ultimate unlock all three with no gating.

## Related pages
- [display-layout.md](display-layout.md) — the Customization page shell (sidebar, tab navigation, preview panel, Publish Changes) that this General tab lives inside.
- [layout.md](layout.md) — Layout tab; layout options differ per active law (see its own preconditions).
- [colours.md](colours.md) — Colours tab.
- [custom-css.md](custom-css.md) — Custom CSS tab (law-agnostic).
- [content-gdpr.md](content-gdpr.md) — Content tab, GDPR variant (Preference Center, Cookie Notice, Cookie List).
- [content-us-state-laws.md](content-us-state-laws.md) — Content tab, US State Laws variant (Opt-out Center, Cookie Notice, Cookie List).
- [../billing-upgrade/plan-gates.md](../billing-upgrade/plan-gates.md) — full plan-gating CTA/tooltip matrix for the locked controls referenced above.

## Source
Derived from `ai-context/cases-cookie-banner-general.json` (26 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
