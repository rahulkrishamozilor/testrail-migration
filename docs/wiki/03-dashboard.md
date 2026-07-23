# Dashboard

**Nav path:** Dashboard (default landing page immediately after login)
**Route:** `/dashboard`
**Roles:** Account Owner (confirmed this run, Free and Ultimate plans). Admin/Editor rendering
pending manual review.
**Plan gating:** No plan-gated *access* — every plan tier lands on this page. Individual cards and
header elements change content/format by plan tier (called out inline below). See
docs/wiki/11-billing-upgrade/plan-gates.md for the general plan-gate model.

## Purpose

The Dashboard is the account's home page: a header with account/site controls plus a stack of
alert banners and status cards that summarize the connected website's cookie-banner installation
state, cookie inventory, consent activity, and pageview traffic at a glance.

## Page structure

### Header (global — appears on every page, not just Dashboard)

- **Logo** (left) — clicking it navigates to `/dashboard`.
- **Website selector** — a combobox showing the current site's domain, next to the logo. Opening
  it lists every site in the account's organisation(s), grouped by organisation name (e.g.
  "Rahulkrishna+freeplansite's organisation — Org ID: 1752"), plus a **"New Site"** button at the
  bottom of the list. The "New Site" button is disabled while the account's email is unverified
  (confirmed live).
- **"Become a partner"** and **"CookieYes Documentation"** buttons, right side of the header.
- **Account/profile menu** — a single icon-only button at the far right of the header. Opening it
  reveals one dropdown menu containing: account email (display only), **Organisations & Sites**,
  **Team**, **Billing & Invoices**, **MCP access**, **Notifications**, **My account**, **Logout**.
  - **Correction:** earlier documentation described "Notifications" and "Profile" as two separate,
    independently-visible header controls (a bell icon plus a profile dropdown). Live-verified this
    run on two accounts (Free and Ultimate): there is only **one** combined account/profile menu
    button, and "Notifications" is a menu item inside it, not a standalone bell icon anywhere in
    the header.
- **"Refer & Earn"** button — appears once the account's email is verified (confirmed absent on
  unverified accounts this run).
- **Top navigation tabs:** Dashboard, Cookie Banner, Cookie Manager, Consent Log, Languages,
  Advanced Settings, a **Legal Policies** dropdown (containing "Cookie Policy Generator" and
  "Privacy Policy Generator" — the latter currently carries a "New" badge), and Reports.
- **Plan indicator** — "Current plan: {tier}" plus a pageviews-used counter. The counter's format
  is plan-dependent (live-verified): on the Free plan it reads "Pageviews used: 0/5,000 (0%)"; on
  the Ultimate plan it reads only a bare count ("0") with no visible "/limit (%)" fraction. Both
  have an info icon next to the count.
- **Plan action button** — "Try Pro for free" (Free plan, confirmed) or "Upgrade" with a crown
  icon (Ultimate plan, confirmed).

### Alert banners

Zero or more dismissible alerts render above the status cards, most tied to a specific account or
site condition:

- **Email verification banner** — shows whenever the account's email is unverified: "Check the
  {email} mailbox to verify your email address." with a "Resend Verification Email" link and a
  dismiss (×) control. Confirmed present, word-for-word, on two different unverified accounts.
- **"Compliance alert: Cookie banner missing"** — shows when at least one cookie has been detected
  on the site but no consent banner is active. Confirmed present on two accounts, each with a
  different body sentence reflecting that account's actual cookie count (e.g. "We detected 1
  cookie on your website..." vs. "Your site is currently setting 15 non-essential cookies without
  user consent...") — the body text is data-driven, not a fixed string. Clicking its **"Enable
  consent banner"** button opens the same "Get installation code" modal described under Cookie
  Banner Status Card below.
- **Other alert variants** — onboarding-installation-pending, 80%/100%/exceeded pageview-limit
  warnings, and the uncategorised-cookies compliance alert.

### Cookie banner status card

(TestRail refers to this section as "Banner Status Card"; the live UI's own card heading reads
"Cookie banner status", lower-case.)

- Shows the connected site's domain at the top.
- **Status line** reads "Inactive" (confirmed) or "Active", with a refresh/re-check icon button
  beside it.
- When Inactive because the installation code isn't on the site yet, the card shows "Looks like
  the installation code isn't added to your site yet!" (confirmed, exact) with a **"Get
  installation code"** button.
  - Clicking it opens a modal titled "CookieYes installation code isn't added to your site." with
    two tabs ("Install manually on website" / "Install with Google Tag Manager"), a copyable
    `<script>` snippet, platform-specific guide links (WordPress, Wix, Kajabi, Shopify, Magento,
    Blogger, Drupal, Squarespace, MODX, Kartra, HTML, Others), and a "Verify" button.
  - **Minor text mismatch found:** the modal's live title uses a curly apostrophe ("isn**’**t"),
    while existing documentation quotes it with a straight apostrophe ("isn**'**t"). Punctuation-
    only.
- **Regulation** field — confirmed showing "GDPR"; US State Laws / combined-regulation values not
  yet checked.
- **Targeted location** field — confirmed showing "Worldwide" with a "Geo-target" link/button on
  an Ultimate-plan account (Geo-targeting not configured); it navigates to the Cookie Banner
  customization page.
- **"Customise banner"** button at the bottom of the card, navigating to the Cookie Banner page
  (confirmed present).
- Other sub-states (Active-with-verify-flow, upgrade nudges for Free/Basic plans on Geo-target,
  regulation-change detection) pending manual review.

### Cookie summary card

- Shows **Total cookies** and **Categories** counts, **Last successful scan** timestamp, **Pages
  scanned** count, a **Next scan** value with a **Schedule** link, and a **Manage cookies** button
  at the card's bottom (confirmed layout, populated state).
- Before a site's first scan, the card shows 0 for Total cookies and Categories, "Not available"
  for Last successful scan, and 0 for Pages scanned — taken as source of truth pending manual
  review (this section was just migrated).
- **Gap found:** the card header also shows an **"Upgrade to AI Cookie Classifier"** button
  labeled **"New: Classify cookies with AI"**, on both the Free and Ultimate accounts checked —
  a newer feature not yet reflected anywhere else in this knowledge base. Its behavior (what
  clicking it does) hasn't been explored yet.
- Schedule-link behavior differs by plan — a free-plan account gets a schedule-scan upgrade nudge
  ("Try Pro for Free"/"Upgrade now" CTA), a paid-plan account goes straight to Cookie Manager's
  scan scheduling.

### Consent trends card

- Empty state (no visitor consent recorded yet): "No visitor consent has been recorded yet" with
  "Make sure you've enabled consent logging" (consent logging as a clickable link), a "Last 7
  days" range indicator in the card header, and a "View all data" link at the bottom. Confirmed
  exact, word-for-word, on both accounts checked.
- Donut-chart states with actual recorded consent (Accepted/Rejected/Partially Accepted mixes)
  pending manual review.

### Pageviews card

- Empty state (no pageviews recorded yet): "No pageviews found!" with "Pageviews may not have
  been recorded yet. Make sure you've added the installation code to your site", and a "View all
  data" link at the bottom. Confirmed exact, word-for-word, on both accounts checked.
- Populated line-chart states, date-range selection, and over-limit-usage highlighting pending
  manual review.

### Recent consent logs card

- Empty state (no consents recorded yet): "No consent log found!" with "Visitor consents may not
  have been recorded yet. Make sure you've enabled consent logging" (consent logging as a
  clickable link), and a "View all logs" control at the bottom. Confirmed exact, word-for-word,
  on both accounts checked.
- Populated states for Accepted/Rejected/Partially-Accepted consent entries and the Consent ID
  tooltip's "Learn more" link pending manual review.

### Dashboard states

Two documented render states — unverified email vs. verified email — largely correspond to what's
already described above rather than being a distinct UI area:

- **Unverified email (confirmed this run):** website selector present; email-verification banner
  shown; header shows Become a partner / Documentation / the single account-profile menu (see the
  Header correction above) and **no** "Refer & Earn" button; all eight nav tabs present; Legal
  Policies dropdown contains Cookie Policy Generator + Privacy Policy Generator; plan indicator
  and all five dashboard cards (Banner Status, Cookie Summary, Consent Trends, Pageviews, Recent
  Consent Logs) render.
- **Verified email:** same as above but the email-verification banner is absent and "Refer & Earn"
  appears — pending manual review.
- This state pairing doesn't appear in `testrail-suite-v2.md`'s canonical section tree at all, and
  may be redundant with the Header section's and each card's own render-state coverage — flagged
  for a human keep/retire decision, not something this page resolves.

## Add a New Site

Reached via the header's website-selector "New Site" button (disabled while email is unverified —
confirmed above). The page renders required fields and controls for organization selection, site
URL, and plan; submitting with no organization selected, an invalid site URL, or an empty site URL
each shows a validation error; toggling Monthly/Annual billing and changing Currency update the
displayed plan prices; selecting a plan with "Get Started" subscribes the new site to that plan;
Cancel discards site creation and returns to the Dashboard; and a "reach out to support" link
opens the CookieYes troubleshoot page. Taken as source of truth pending manual review (including
the actual payment/subscription step, not yet live-checked).

Note: "Add a New Site" is actually a **top-level TestRail section**, not nested under Dashboard —
same for "Header" above. Both are documented on this page for now (matching how
`docs/wiki/README.md` currently groups them under "03. Dashboard"), but this grouping may be worth
revisiting — Header in particular is global chrome, not Dashboard-specific.

## Validation & edge cases

- **Header account-menu is a single combined control**, not separate bell + profile icons — see
  the Header correction above.
- **Pageviews-used counter format is plan-dependent**: fraction-with-percentage on Free, bare count
  on Ultimate (Basic and Pro tiers not yet checked).
- **Installation-modal title has a punctuation-only mismatch** against existing documentation
  (curly vs. straight apostrophe) — cosmetic, not a behavior bug.
- **"Upgrade to AI Cookie Classifier" / "New: Classify cookies with AI"** on the Cookie Summary
  card is a real, live-observed UI element not yet documented anywhere else — a genuine coverage
  gap.
- **Compliance alert body text is data-driven** (varies with actual cookie count on the site), so
  don't treat any single wording of it as the fixed string — only the alert's heading and the
  "Enable consent banner" button/destination were confirmed stable.

## Known gaps

- No Admin/Editor role verification this run — Account Owner only, confirmed.
- This section was just migrated into TestRail; the content above is taken as source of truth for
  now. A manual live-review pass is pending and expected to update this page incrementally as it
  happens, rather than all at once.
- A representative sample of cases was live-verified this run against the QA2 app — see the
  "confirmed" call-outs above. The rest are documented straight from the migrated content.

## Related pages

- docs/wiki/11-billing-upgrade/plan-gates.md
- docs/wiki/04-cookie-banner/display-layout.md
- docs/wiki/05-cookie-manager/cookie-list-categories.md
- docs/wiki/06-consent-log.md

## Source

This section was just migrated into TestRail; its content is treated as source of truth for this
page. Drafted 2026-07-23 via `/wiki-sync`, with a sample live-verified against the QA2 app — see
inline confirmations above. Manual review of the remainder is still pending and will update this
page incrementally.
