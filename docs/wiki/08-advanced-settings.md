# Advanced Settings

**Nav path:** Advanced Settings
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Mixed, control-by-control (this page is not gated as a whole). Three controls
are gated: "Disable banner on specific pages" (Pro+), "Subdomain consent sharing" and its
dependent "Link to your list of sites" (Pro+), and "Static IP Scan" (Ultimate+). All other
controls on this page are available on every plan. See "Validation & edge cases" below for the
exact locked-state behavior of each, and docs/wiki/11-billing-upgrade/plan-gates.md for the
general upgrade-nudge/CTA pattern shared across gated features.

## Purpose
Advanced Settings is a single flat page that groups low-level, cross-cutting configuration for
the cookie banner and consent pipeline: banner activation/installation status, consent-sharing
and consent-renewal behavior, Google Consent Mode (GCM) diagnostics, Microsoft UET/Clarity
consent integrations, and cookie-scan behavior. It is the page a user visits to troubleshoot why
the banner isn't showing, to verify GCM/UET wiring, or to change scan/consent behavior that
doesn't belong on the Cookie Banner customization page itself.

## Page structure
The Advanced Settings page displays five sections, top to bottom (per case 37192):

1. **Banner settings**
2. **Consent settings**
3. **Google consent mode (GCM)**
4. **Microsoft consent mode & Clarity API integration**
5. **Scan settings**

### 1. Banner settings
- **Cookie banner status** — a read-only status line with one of three states:
  - **Inactive (code not installed):** status reads "Inactive"; a reload button (tooltip:
    "Verify installation") and a "Get Installation code" button are shown; helper text reads
    "Looks like the installation code isn't added to your site yet! Click Get installation code
    to copy the code."
  - **Active:** status reads "Active" with a help icon (tooltip: "If you remove the code from
    your site, it may take up to 24 hours for the change to reflect here"); text below reads
    "You have successfully set up your cookie banner!"; a "Get Installation code" button remains
    visible.
  - **Inactive (pageview limit exceeded):** status reads "Inactive"; no reload button is shown;
    text reads "Pageview limit exceeded: Upgrade to activate banner." with an "Upgrade" link.
  - **Inactive (user-disabled):** when "Banner display status" is set to Disabled while status
    was Inactive, the reload button is removed and text reads "Looks like you have disabled the
    banner on your site. Enable it from Banner display status."
- **Banner display status** — a dropdown with options "Enabled" / "Disabled", defaulting to
  "Enabled". Helper text reads "By disabling this, the CookieYes script/banner on your site will
  be disabled, allowing you to test and debug any issues." Selecting a new value shows Confirm
  and Discard icons next to the dropdown until confirmed or discarded.
- **Disable banner on specific pages** — Pro+ only (locked with a premium icon on lower plans,
  label reads "Not set", edit icon disabled). On Pro+, an edit (pencil) icon opens a popup with a
  URL text area and "Save Changes"/"Cancel" buttons for entering URL patterns on which the
  banner should not display.

### 2. Consent settings
- **Consent log toggle** — enabled by default; controls whether consents given on the user's
  website are recorded to the Consent Log page.
- **Subdomain consent sharing** — Pro+ only (locked with a premium icon and a disabled/unchecked
  toggle on lower plans). On Pro+, enabled by default; helper text includes a "re-scan" link to
  the Cookie Manager page. When enabled, consent given on the main domain is recognised on
  subdomains without re-prompting.
- **Link to your list of sites** — Pro+ only, appears under Consent settings once Subdomain
  consent sharing is enabled. Defaults to label "Not set" with an edit icon and an info-tooltip
  icon (tooltip: "This will be linked in the first layer of your banner if you share consent
  across subdomains. Required for TCF 2.2 compliance."). The edit icon opens an "Add a URL
  listing covered sites" modal with a URL text field (placeholder "https://www.example.com"),
  disabled "Save changes" button until valid input is entered, and an active "Cancel" button.
- **Renew user consents** — a "Renew Now" button that opens a "Renew user consents?" confirmation
  popup with "Cancel" and "Renew Consent" buttons.

### 3. Google consent mode (GCM)
- **Support GCM** toggle — enabled by default; helper text links to "integrate Consent Mode with
  CookieYes" (GCM integration docs) and "displaying Google's Privacy Policy on your banner".
  Disabling this toggle also disables the dependent "Allow Google tags to fire before consent"
  toggle.
- **Allow Google tags to fire before consent** toggle — disabled by default; only meaningful
  while Support GCM is enabled. When enabled, Google tags fire on the site before the user
  provides consent.
- **Check GCM status** — a "Check Now" button. Clicking it briefly shows "Checking" with a
  loader, then displays "Last checked: [timestamp]" plus one of several result states (see
  Validation & edge cases below), each with a "resolve this issue" or "troubleshooting guide"
  link to the relevant documentation page.
- **GCM Debug Mode** toggle — when enabled, opens the browser console (DevTools) on the user
  website to a set of consent-category diagnostic lines (see Validation & edge cases below).

### 4. Microsoft consent mode & Clarity API integration
- **Support Microsoft UET Consent Mode** toggle — enabled by default, with a "Learn more" link
  to UET Consent Mode documentation. While enabled, user consent is passed to Microsoft UET tag
  events; disabling it stops consent being passed to UET.
- **Microsoft Clarity Consent API integration** toggle — enabled by default, with a "Clarity
  Consent API" documentation link. While enabled, user interaction data is sent to the Clarity
  Dashboard only after consent; disabling it sends data to Clarity regardless of consent.

### 5. Scan settings
- **Static IP scan** — Ultimate plan only. On lower plans, a premium icon is shown and the
  status dropdown is disabled (tooltip: "Upgrade to the Ultimate plan to unlock this feature.").
  On Ultimate, a status dropdown offers "Enabled"/"Disabled" (defaults to "Disabled"); enabling
  it means subsequent cookie scans are initiated from a static IP address.

## Workflows

**Banner settings**

1. **Installing the banner from an Inactive (no-code) state**
   1. Start on Advanced Settings with the installation code not yet added to the site.
   2. Observe the Cookie banner status option: shows "Inactive", a reload button (tooltip
      "Verify installation"), and a "Get Installation code" button.
   3. Click "Get Installation code". Result: the banner installation popup opens.

2. **Verifying installation via the reload button**
   1. Start on Advanced Settings with the installation code added to the site but status still
      showing "Inactive".
   2. Click the reload button next to the Inactive status. Result: a mini tab opens loading the
      user website with the banner; status line reads "Connecting to your site to verify
      installation" with a loading icon.
   3. Wait for verification. Result: status updates to "Active"; a help icon appears; text below
      reads "You have successfully set up your cookie banner!"

3. **Banner display status confirm/discard**
   1. Start on Advanced Settings (Banner display status defaults to "Enabled").
   2. Open the dropdown and select "Disabled". Result: "Disabled" is selected; Confirm and
      Discard icons appear.
   3. Click Discard. Result: dropdown reverts to "Enabled"; Confirm/Discard icons disappear.
   4. Select "Disabled" again and click Confirm. Result: "Disabled" is confirmed and takes
      effect on the site (banner is no longer displayed on the user website; Cookie banner
      status changes from "Active" to "Inactive" with text "Looks like you have disabled the
      banner on your site. Enable it from Banner display status.").
   5. Re-select "Enabled" and click Confirm. Result: the banner is re-enabled on the site.

4. **Disable banner on specific pages (Pro+)**
   1. Start on Advanced Settings on Pro plan or higher, with "Disable banner on specific pages"
      showing "Not set".
   2. Click the edit icon. Result: the "Disable banner on specific pages" popup opens with a URL
      text area and "Save Changes"/"Cancel" buttons.
   3. Enter an invalid URL and click "Save Changes". Result: an "Invalid URL(s)" error appears
      below the text area; the popup stays open.
   4. Clear the field, enter one or more valid URLs, and click "Save Changes". Result: popup
      closes; the option now reads "[N] URL pattern(s) added".
   5. Navigate to one of the saved URLs on the user website. Result: the cookie banner is not
      displayed on that page.

**Consent settings**

5. **Consent log toggle**
   1. Start on Advanced Settings (Consent log toggle enabled by default).
   2. Give consent on the user website. Result: consent is recorded on the Consent Log page.
   3. Disable the Consent log toggle, then give consent again on the user website. Result: the
      new consent is not recorded on the Consent Log page.

6. **Subdomain consent sharing (Pro+)**
   1. Start on Advanced Settings on Pro plan or higher (Subdomain consent sharing enabled by
      default).
   2. Click the "re-scan" link in the helper text. Result: the Cookie Manager page opens.
   3. (Precondition: CookieYes is installed on both main domain and a subdomain, and the
      subdomain has been scanned.) Accept the cookie banner on the main domain, then navigate to
      the subdomain. Result: the banner does not reappear on the subdomain — consent from the
      main domain is recognised there.

7. **Link to your list of sites (Pro+, requires Subdomain consent sharing enabled)**
   1. Start on Advanced Settings on Pro plan or higher with Subdomain consent sharing enabled;
      "Link to your list of sites" shows "Not set".
   2. Click the edit icon. Result: the "Add a URL listing covered sites" modal opens with a URL
      text field (placeholder "https://www.example.com"); "Save changes" is disabled; "Cancel"
      is active.
   3. Click "Cancel". Result: modal closes; option still shows "Not set".
   4. Click the edit icon again, enter an invalid URL, and click "Save changes". Result: "Please
      enter a valid URL" error is shown; modal stays open.
   5. Clear the field, enter a valid URL (e.g. `https://www.example.com/privacy`), and click
      "Save changes". Result: modal closes; the URL appears as a clickable link next to the
      option label; the descriptive subtext disappears.
   6. On a GDPR (IAB TCF v2.3) banner regulation, open the Cookie Banner first-layer preview.
      Result: the sentence "Please note that your choices apply across all our subdomains" is
      shown with "subdomains" as a hyperlink whose href matches the saved URL.

8. **Renew user consents**
   1. Start on Advanced Settings.
   2. Click "Renew Now" under Renew user consents. Result: a "Renew user consents?" confirmation
      popup appears with "Cancel" and "Renew Consent" buttons.
   3. Click "Cancel". Result: popup closes; no renewal occurs.
   4. Click "Renew Now" again, then click "Renew Consent". Result: old consents are invalidated,
      the cookie banner reappears on the user website, and the "Last renewal" date/time updates
      to the current date and time.

**Google consent mode (GCM)**

9. **Support GCM and dependent toggle**
   1. Start on Advanced Settings (Support GCM enabled by default).
   2. Click the "integrate Consent Mode with CookieYes" link. Result: the CookieYes GCM
      integration documentation page opens in a new tab.
   3. Disable the Support GCM toggle. Result: GCM is disabled and the "Allow Google tags to fire
      before consent" toggle also becomes disabled.
   4. With Support GCM re-enabled, enable "Allow Google tags to fire before consent". Result:
      Google tags fire before the user provides consent on the site.

10. **Check GCM status**
    1. Start on Advanced Settings with Support GCM enabled and a website in a specific GCM
       configuration state (see Validation & edge cases for each state).
    2. Click "Check Now". Result: status shows "Checking" with a loader, then "Last checked:
       [timestamp]" plus the result message for that configuration state.
    3. Click the "resolve this issue" / "troubleshooting guide" link in the result message.
       Result: the corresponding GCM Troubleshooting (or scan-failure) documentation page opens.

11. **GCM Debug Mode**
    1. Start on Advanced Settings with GCM Debug Mode toggle enabled for a website in a specific
       GCM configuration state (see Validation & edge cases).
    2. Open the user website with browser DevTools open. Result: the console shows per-category
       consent diagnostic output matching that configuration state.

**Microsoft consent mode & Clarity API integration**

12. **Support Microsoft UET Consent Mode**
    1. Start on Advanced Settings (toggle enabled by default).
    2. Click "Learn more". Result: the UET Consent Mode documentation page opens in a new tab.
    3. With the toggle enabled, confirm consent is passed to Microsoft UET tag events.
    4. Disable the toggle. Result: user consent is no longer passed to UET tag events.

13. **Microsoft Clarity Consent API integration**
    1. Start on Advanced Settings (toggle enabled by default).
    2. Click the "Clarity Consent API" link. Result: the Clarity Consent API documentation page
       opens.
    3. With the toggle enabled, confirm user interaction data is sent to the Clarity Dashboard
       only after consent.
    4. Disable the toggle. Result: user data is sent to the Clarity Dashboard regardless of
       cookie consent.

**Scan settings**

14. **Static IP scan (Ultimate)**
    1. Start on Advanced Settings on the Ultimate plan; Static IP scan status dropdown defaults
       to "Disabled".
    2. Open the dropdown. Result: "Enabled"/"Disabled" options are shown.
    3. Select "Enabled" and click Confirm. Result: Static IP scan is enabled; subsequent cookie
       scans are initiated from a static IP address.
    4. Select "Disabled" and click Confirm. Result: Static IP scan is disabled.

## Validation & edge cases

- **Cookie banner status — pageview limit exceeded:** reproduced via the pageview-limit
  scheduled-task chain (`GET /api/migrate/set-pageviews?...`, `GET
  /api/test/execute-scheduled-task?name=pageview-limit-reached-actions`, then
  `pageview-banner-disable`). Result: status is "Inactive", the reload button is hidden, and
  text reads "Pageview limit exceeded: Upgrade to activate banner." with an "Upgrade" link to
  the plan upgrade page.
- **URL validation — "Disable banner on specific pages":** an invalid URL entered in the popup's
  text area produces an "Invalid URL(s)" error and keeps the popup open.
- **URL validation — "Link to your list of sites":** an invalid URL produces "Please enter a
  valid URL" and keeps the modal open; "Save changes" stays disabled until the field holds valid
  input.
- **Plan-gated: Disable banner on specific pages (below Pro).** Premium icon shown next to the
  label; edit (pencil) icon disabled; label reads "Not set"; tooltip on the premium icon reads
  "Upgrade to Pro or a higher plan to unlock this feature." See
  docs/wiki/11-billing-upgrade/plan-gates.md.
- **Plan-gated: Subdomain consent sharing (below Pro).** Premium icon shown; toggle is disabled
  and unchecked; tooltip reads "Upgrade to Pro or a higher plan to unlock this feature." See
  docs/wiki/11-billing-upgrade/plan-gates.md.
- **Plan-gated: Static IP Scan (below Ultimate).** Premium icon shown; status dropdown disabled;
  tooltip reads "Upgrade to the Ultimate plan to unlock this feature." See
  docs/wiki/11-billing-upgrade/plan-gates.md.
- **Check GCM status — result states (each with a distinct message and troubleshooting link):**
  - No GCM implementation: "Error: Consent tab empty" — "This error occurs when (i) GCM is not
    implemented on your website or (ii) when no consent data is collected."
  - Correct implementation: "No error detected" — "Good job! Google Consent Mode is configured
    correctly on your website."
  - Custom script missing/incomplete (Method 2): "Error: Default consent not set" — "This error
    occurs when (i) the default consent state is not defined or properly configured in the
    CookieYes CMP Tag in GTM, or (ii) when using the Custom Script method, the custom script for
    GCM is missing or incomplete."
  - Consent preference updates not firing: "Error: Consent doesn't update" — "This error occurs
    when the consent preferences of users are not properly updated or recorded."
  - Analytics tag loads before the CookieYes custom script: "Error: Default consent set too
    late" — "This error occurs when (i) other tags fire before the default consent is set, or
    (ii) Google Tag Gateway (GTG) is active on your site, causing tags to load before the
    consent banner initializes."
  - Invalid/inaccessible website URL: "Scan failed" — "The scan couldn't be completed due to an
    unexpected error. Please try again or check out this troubleshooting guide."
- **GCM Debug Mode — console output states:**
  - No GCM implementation: console shows "No Consent Mode data found".
  - Correct implementation: each consent category (`ad_storage`, `analytics_storage`, etc.)
    shows `Default: denied` and `Update: denied`, followed by "Consent mode states were set
    correctly."
  - Default consent not configured: categories show `Default: missing` (not denied), with
    warning "Some categories are missing a default value."
  - Default consent set too late: categories show `Default: denied`/`Update: denied` plus
    warning "A tag read consent before a default was set."
  - Consent updates not firing: categories show `Default: denied` but `Update: missing`; note
    the source data reproduces "Consent mode states were set correctly." even in this error
    case — treat this as-is, not as a documentation error, until live-verified.
- **Destructive/environment-dependent preconditions not fully exercised in source data:**
  several cases (Active-status reload, pageview-limit exceeded, Renew user consents,
  subdomain-consent-sharing propagation, all Check GCM status and GCM Debug Mode error states)
  require specific external site/GTM configurations or scheduled-task API calls and were
  marked `skipped:destructive-precondition` or `needs-manual-check` during grilling — behavior
  above reflects the drafted expectation, not a live-confirmed one in every case.
- **Consent Template / Banner settings section internals beyond the controls listed above:**
  not captured in source data — needs live verification.
- **Route/URL pattern for the Advanced Settings page itself:** not captured in source data —
  needs live verification.

## Related pages
- [Cookie Banner — General](04-cookie-banner/general.md)
- [Languages](07-languages.md)
- [Plan Gates](11-billing-upgrade/plan-gates.md)

## Source
Derived from `ai-context/cases-advanced-settings.json` (35 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
