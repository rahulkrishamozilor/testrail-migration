# Cookie Manager — Scan & Scan History

**Nav path:** Cookie Manager (top navigation bar) > scan cards (page top) and Scan History tab
**Route:** (not captured in source data for the Cookie Manager page itself — needs live verification). The Detailed Scan History page is confirmed at `/manage-cookies/scan-history/{id}`, implying the parent Cookie Manager page's base path is `/manage-cookies`.
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Partial. **Schedule Scan** is plan-gated (locked on plans without scan scheduling, e.g. Free/Basic) — see Validation & edge cases below and [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) for the full matrix. The **AI Cookie Classifier** is described in `testrail-suite-v2.md` as plan-gated and opt-in, but the source cases here only capture its entry-point card, not its gating rules or plan tiers — (not captured in source data — needs live verification).

## Purpose
This is where a site owner triggers and monitors cookie scans — one-off or scheduled — reviews scan history and per-scan detail, and (on eligible plans) opts into AI-assisted cookie classification.

## Page structure

The Cookie Manager page displays the title **"Cookie Manager"** with subtitle **"Manage your cookie list, scan schedule and more"**, followed by three cards:

- **Last Successful Scan card** — has a **"Scan now"** button on its right, used to trigger an ad-hoc scan.
- **Next Scan card** — has a **"Schedule scan"** button (relabeled **"Reschedule scan"** once a schedule exists), used to configure recurring/one-time scans.
- **AI Cookie Classifier card** — carries a **"New"** badge, an **"Enable AI classifier"** button, and a **"Learn more"** link. Plan-gated and opt-in per `testrail-suite-v2.md`; beyond the card's presence and labels, its enablement flow and plan requirements are (not captured in source data — needs live verification).

Below the cards, two tabs: **"Cookie List"** (active by default, underlined — see [cookie-list-categories.md](cookie-list-categories.md)) and **"Scan History."**

### Scan popup (opened via "Scan now")
- **"Full Scan"** is selected by default; a **"Custom Scan"** radio button is also present.
- Selecting **Custom Scan** expands a text field (placeholder "List standard URL(s), one per line") and shows a replacement alert: *"Your existing cookie list (cookies discovered in the previous scan) will be replaced with the cookies discovered in this scan. Therefore, make sure you include all the pages that sets cookies."*
- With **Full Scan** selected, clicking **"Show advanced options"** reveals **Include URL** and **Exclude URL** text fields (one URL, or wildcard, per line) and shows a differently-worded replacement alert: *"Your existing cookie list (cookies discovered in the previous scan) will be replaced with the cookies discovered in this scan. Therefore, make sure you don't exclude the pages that sets cookies."*
- A **"Scan now"** / **"Scan Now"** button in the popup's bottom right starts the scan, followed by a **"Scanning initiated successfully"** confirmation (green tick) dismissed with **"Ok."**

### Schedule scan popup ("Schedule cookie scan")
Opened via "Schedule scan" (or "Reschedule scan," pre-filled with the current schedule). Contains a **Scan frequency** dropdown with at least four values:

| Frequency | Extra controls shown |
|---|---|
| **Never** | none — disables any existing schedule |
| **Only Once** | date picker + time picker |
| **Weekly** | **"Select Day"** day-of-week dropdown + time picker (the only frequency using a day picker instead of a date picker) |
| **Monthly** | date picker + time picker |

"Show advanced options" within this popup reveals the same Include URL / Exclude URL / Custom Scan fields as the Scan popup, scoping the recurring schedule to specific pages. A **"Save"** button commits the schedule.

### Scan History tab
An always-present advisory alert banner reads: *"We continuously monitor our scanning software to ensure its ongoing effectiveness, security, and accuracy. However, we advise you to run a quick manual check to determine if there are any cookies on your site that our scanner couldn't detect. Instructions on how to check cookies on your website manually."* — the phrase "how to check cookies on your website manually" is a hyperlink to CookieYes documentation.

The table lists scans with columns: **Scan Date** (`[DD Month YYYY HH:MM:SS] (UTC)`), **Scan Status** (badges observed: **Failed** — with an info tooltip icon; **In Progress** — blue; **Aborted** — red), **Urls Scanned**, **Categories**, **Cookies**, **Scripts**, plus a **"More info"** link per row and an **"Abort scan"** icon button while a scan is in progress. For Failed and in-progress/aborted rows, Urls Scanned/Categories/Cookies/Scripts remain empty.

### Detailed Scan History page (`/manage-cookies/scan-history/{id}`)
Reached via a row's "More info" link. Contains:
- A **"Back to Scan History"** button.
- A summary section: **Scan Date** (`[Month DD, YYYY HH:MM:SS] (UTC)`) with a green tick, **Total Cookies**, **Total Categories**, and **Pages Scanned** counts.
- A **"Discovered cookies"** section, grouped by category (category name as a label above each table), each cookie row showing **Id**, **First found URL** (clickable link to the page), **Duration**, and **Description**.
- A **"Pages scanned"** section: a table of **Urls** and **Cookies** (count) columns.

### Scan-result emails
- **"Cookie scanning completed"** email: CookieYes logo; body *"Hi there, We have completed the cookie scan of [website]. Please check your account to get the full report. Best Regards, The CookieYes Team"*; a link on `[website]` opening the scanned site. A second call-to-action link (to the scan results directly) is claimed by one source case but unconfirmed — (not captured in source data — needs live verification).
- **"Cookie scan failed"** email: CookieYes logo; body *"Hi there, We regret to inform you that the recent cookie scan for [website] has failed. Check out the common issues causing scan failure and try applying the suggested solutions to resolve them. After resolving the issues, try re-scanning the site, and if the issue persists, contact us. Best Regards, The CookieYes Team"*; links on `[website]`, "common issues causing scan failure" (troubleshooting docs), and "contact us" (support page).
- The Cookie Manager page itself also shows a failed-scan **alert banner** below the title when the last scan failed: *"The last cookie scan has failed. Check out the common issues causing scan failure and try applying the suggested solutions to resolve them. After resolving the issues, try re-scanning your site, and if the issue persists, contact us."* with "common issues causing scan failure" and "contact us" as hyperlinks.

## Workflows

1. **Run a Full Scan**
   1. Click "Scan now" on the Last Successful Scan card. The Scan popup opens with Full Scan selected by default.
   2. Click "Scan now" in the popup, then dismiss "Scanning initiated successfully" with "Ok."
   3. Open the Scan History tab — the new scan shows an in-progress status.
   4. When the scan completes, its status updates and newly discovered cookies are added to the cookie list under their categories (see [cookie-list-categories.md](cookie-list-categories.md)).

2. **Run a scan restricted to specific pages (Include URL)**
   1. Click "Scan now," then "Show advanced options" — the Include URL / Exclude URL fields appear.
   2. Enter one or more URLs (one per line) in Include URL and click "Scan Now." A "Scan initiated successfully" popup appears.
   3. On completion, a "Cookie scanning completed" email is received and the Scan History tab shows the completed scan.

3. **Run a scan that excludes specific pages (Exclude URL)**
   1. Click "Scan now," then "Show advanced options."
   2. Enter one or more URLs/wildcards in Exclude URL and click "Scan Now."
   3. On completion, a "Cookie scanning completed" email is received; excluded pages should not appear under Urls Scanned for that scan.

4. **Run a Custom Scan of a single page**
   1. Click "Scan now," select the "Custom Scan" radio button — the text field expands.
   2. Enter a single valid URL and click "Scan Now."
   3. On completion, a "Cookie scanning completed" email is received; only that URL appears under Urls Scanned for the scan.

5. **Schedule a recurring or one-time scan**
   1. Click "Schedule scan" on the Next Scan card — the "Schedule cookie scan" popup opens.
   2. Select a frequency: "Only Once" (pick a future date/time), "Weekly" (pick a day via "Select Day" plus a time), or "Monthly" (pick a future date/time). Optionally expand "Show advanced options" to scope the schedule to Include/Exclude/Custom Scan URLs.
   3. Click "Save." The popup closes and the Next Scan card shows the scheduled date/time; for Weekly/Monthly the button changes to "Reschedule scan."
   4. For a one-time ("Only Once") schedule, once the scheduled time arrives the scan runs, a "Cookie scanning completed" email is received, and the Next Scan card reverts to "Not scheduled."

6. **Disable an existing scan schedule**
   1. Click "Reschedule scan" on the Next Scan card — the popup opens pre-filled with the current schedule.
   2. Select "Never" from the Scan frequency dropdown and click "Save."
   3. The Next Scan card shows "Not scheduled" and its button reverts to "Schedule scan."

7. **Abort an in-progress scan**
   1. With a scan in progress, click the "Abort scan" icon button on its Scan History row.
   2. A confirmation popup appears: *"Are you sure you want to abort the scan?"* with "Cancel" and "Abort" buttons.
   3. Clicking "Abort" closes the popup; the row updates to an "Aborted" status (red), with Urls Scanned/Categories/Cookies/Scripts remaining empty.

8. **View a scan's full detail**
   1. On a completed scan's Scan History row, click "More info."
   2. The Detailed Scan History page opens at `/manage-cookies/scan-history/{id}`, showing the summary counts, the "Discovered cookies" breakdown by category, and the "Pages scanned" table.

## Validation & edge cases

- **Unverified email blocks scanning**: if the account email is not verified, clicking "Scan now" shows no popup and instead a tooltip: *"Please verify your email address to rescan your website for cookies."* The same tooltip and blocked behavior apply to "Schedule scan."
- **Custom Scan field validation**: entering a second URL on the same line (without pressing Enter) in the Custom Scan text field shows *"Invalid URL(s)"* below the field.
- **Schedule Scan plan gate**: on plans without scan scheduling (below Pro), clicking "Schedule scan" (with a verified email) opens a promotion modal headlined *"Run automated scans and get an up-to-date cookie list every time,"* with text *"Available in: Pro and Ultimate plans"* and a **"Try Pro for free"** CTA button (not "Upgrade now" — a stale label from an earlier product version). See [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md).
- **Weekly frequency is the odd one out**: it shows a day-of-week picker ("Select Day") rather than a date picker, unlike Only Once/Monthly.
- **Failed scan state**: shows the on-page alert banner (verbatim above), a "Failed" badge with tooltip in Scan History, and empty stat columns.
- **In-progress scan state**: "In Progress" badge (blue), empty stat columns, and an "Abort scan" icon button.
- **AI Cookie Classifier**: confirmed present as a card with "New" badge, "Enable AI classifier" button, and "Learn more" link; its actual classification behavior, opt-in flow, and plan requirements are (not captured in source data — needs live verification).

## Related pages
- [cookie-list-categories.md](cookie-list-categories.md) — Cookie List tab, category sidebar, and where newly-discovered cookies from a scan land.
- [edit-add-cookies.md](edit-add-cookies.md) — Edit/Add Cookie popups for cookies surfaced by a scan.
- [../06-consent-log.md](../06-consent-log.md) — consent proof recorded against cookies/categories a scan discovers.
- [../11-billing-upgrade/plan-gates.md](../11-billing-upgrade/plan-gates.md) — Schedule Scan (and other Cookie Manager) plan-gating detail.

## Source
Derived from `ai-context/cases-cookie-manager.json` (34 TestRail cases total, split by sub-topic — 23 cases feed this file: 37261, 37262, 37263, 37264, 37265, 37266, 37267, 37268, 37269, 37270, 37271, 37272, 37273, 37274, 37283, 37284, 37285, 37286, 37287, 37288, 37290, 37291, 37293). Drafted 2026-07-14, not yet live-verified against the QA app.
