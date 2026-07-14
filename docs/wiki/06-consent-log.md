# Consent Log

**Nav path:** Consent Log
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** No plan-gated *access* to the page itself (Free and paid plans both reach it).
Plan state changes what the page shows and enforces — see the plan-dependent behavior called
out under Page structure and Workflows below, and see docs/wiki/11-billing-upgrade/plan-gates.md
for the general plan-gate model.

## Purpose

The Consent Log page is the record of how visitors to a connected website have responded to the
cookie banner — accepted, rejected, or partially accepted. It lets the account holder search,
inspect, and export that consent history as evidence of compliance (e.g. for audits or legal
requests), and download a per-visitor Proof of Consent PDF.

## Page structure

Reached via the "Consent Log" tab in the top navigation bar. The page's main content area shows
a single card titled "Your visitor consents":

- **Heading row** — the "Your visitor consents" title, with an "Export as CSV" link button to
  its right.
- **Search field** — top right of the card, with a magnifying-glass search button. Accepts a
  consent ID. After a search is submitted, the magnifying-glass icon is replaced by a × (clear)
  button.
- **Consent table** — column set depends on plan:
  - **Free plan:** four columns — Consent ID, Consent Status, Date/Time (UTC ± 00:00), Proof of
    Consent.
  - **Paid plans (Basic, Pro, Ultimate):** five columns — Consent ID, Country, Consent Status,
    Date/Time (UTC ± 00:00), Proof of Consent. The Country column is the only structural
    difference from the Free plan table.
  - The Consent ID and Proof of Consent column headers each carry a tooltip icon.
  - Consent ID cells show a truncated ID; hovering reveals the full ID as tooltip text.
  - Consent Status cells show one of: "Accepted", "Rejected", "Partially accepted" (grill note
    flags a possible capitalization mismatch — the Dashboard shows "Partially Accepted" with a
    capital A; the Consent Log table's exact capitalization needs live verification).
  - Date/Time cells are formatted `[Month] [Date], [Year] [hh:mm:ss]`.
  - Proof of Consent cells show a download button that opens the Proof of Consent modal.
  - On paid plans, a note below the table reads: "You can view up to 100 visitor consents logged
    here. Use the export option if you want to download the historical log data."
- **Empty state** — when no consent has ever been recorded, the card shows an empty-state icon
  and the message "No consent log found! Visitor consents may not have been recorded yet. Make
  sure you've enabled consent logging" (no trailing period), with "consent logging" as a link to
  Advanced Settings.
- **No-results state** — when a search matches nothing (including a query outside the plan's
  retention/search window), the table area shows: "No data available! While older logs may not
  be available here, you can export the data to access them."

## Workflows

### 1. Viewing recorded consent entries
1. Navigate to Consent Log (top navigation bar).
2. If at least one visitor has interacted with the banner, the consent table lists entries with
   Consent ID, (Country, on paid plans), Consent Status, Date/Time, and a Proof of Consent
   download button per row.
3. If no visitor has interacted with the banner yet, the card shows the empty state described
   above instead of a table.

### 2. Inspecting a truncated Consent ID
1. Locate an entry's Consent ID cell (shown truncated).
2. Hover over it.
3. The complete, untruncated consent ID appears as tooltip text.

### 3. Viewing Proof of Consent for an entry
1. In the consent table, locate the download button under the Proof of Consent column for the
   entry.
2. Click the download button.
3. The "Proof of consent" modal opens, showing the entry's Consent ID, its Consent date, and
   Cancel / Generate PDF buttons.
4. Click **Cancel** — the modal closes and no file is generated or downloaded.
5. Click **Generate PDF** instead — a "Generating PDF..." confirmation dialog appears with the
   message "We will send the proof of consent report to [email] when it is ready for download."
   and an Okay button. Clicking Okay closes the dialog. The PDF itself is delivered by email, not
   downloaded directly in-browser.

### 4. Searching by Consent ID
1. On the Consent Log page, enter a Consent ID into the search field (top right of the card).
2. Click the search button (magnifying-glass icon) or press Enter.
3. If the ID matches an existing entry within the account's search window, only the matching
   entry (or entries) is shown.
4. If the ID does not match any entry, or matches an entry outside the plan's search window
   (see below), the table shows: "No data available! While older logs may not be available
   here, you can export the data to access them."
5. After a search is active, click the **×** button that has replaced the magnifying-glass icon
   to clear the search — the field empties, the × reverts to the magnifying-glass icon, and the
   full consent log list is restored.

### 5. Plan-dependent search window
The in-app search (workflow 4) only reaches back a limited window depending on plan; entries
older than the window return the "No data available!" message even though they still exist and
can be retrieved via CSV export:
- **Free plan:** past 1 month.
- **Basic plan:** past 3 months.
- **Pro plan:** past 6 months.
- **Ultimate plan:** a plan-specific window that is not captured in source data — needs live
  verification (the source TestRail case for this was truncated before the retention figure was
  recorded).

### 6. Exporting the consent log as CSV
1. Click the "Export as CSV" link button next to the "Your visitor consents" heading.
2. If the account's email is verified, the "Export consent logs" modal opens.
   - **Free plan:** the modal shows "With the Free plan, you can export consent logs from the
     past 1 year. To retain logs for up to 5 years, upgrade to a paid plan." with "upgrade to a
     paid plan" as a link to the Plans page.
   - **Paid plans (Basic, Pro, Ultimate):** the modal shows "You can export consent logs from the
     past 5 years. Logs beyond this period are not retained." with no upgrade link.
   - A "Select a date range to export data" label and date picker are shown, defaulting to
     "Last 30 days" (displayed in DD/MM/YYYY format). Cancel and "Export as CSV" buttons sit at
     the bottom of the modal.
3. Click the date range control to open a dropdown with: Last 30 days (default), Last 3 months,
   Last 6 months, Last 12 months, All time, Custom. Choosing any preset updates the date picker
   to the corresponding start/end dates. Choosing **Custom** opens a two-month calendar picker
   (future dates disabled) for selecting a custom start and end date; the chosen range is then
   reflected back in the date picker field.
4. Click "Export as CSV" inside the modal. A confirmation pop-up appears: title "Creating a CSV
   file...", message "We will send your export to [email] when it is ready for download.", and
   an Okay button. Clicking Okay closes the pop-up.
5. A "Download consent log" email is sent to the registered address; opening it and clicking its
   "Download Consent Log" button downloads the CSV file. (Not automatable — verified only by
   manual email inspection.)
6. If the account's email is **not** verified, the "Export as CSV" button is disabled: clicking
   it triggers no action, and hovering over it shows a tooltip reading "Please verify your email
   address to export your visitor consent log."

## Validation & edge cases

- **Empty state:** no consent ever recorded shows the empty-state icon/message with a working
  link to Advanced Settings (workflow 1); this is distinct from the "No data available!"
  no-results state, which only appears after a search.
- **Unverified email blocks export:** Export as CSV is inert and shows a blocking tooltip rather
  than opening the export modal (workflow 6, step 6).
- **Search outside retention/search window:** returns "No data available!" even though the
  underlying entries still exist and remain retrievable via CSV export — the message text
  explicitly points the user at the export option.
- **Cancel is a no-op:** in the Proof of Consent modal, Cancel closes the modal with no file
  generated (confirmed behavior, not just an assumption from UI convention).
- **Consent status values:** exactly three — Accepted, Rejected, Partially accepted. The
  "Partially accepted" label's exact capitalization in the table (vs. "Partially Accepted" on
  the Dashboard) is unconfirmed — needs live verification.
- **Ultimate plan retention/search window:** not captured in source data — needs live
  verification before relying on any specific figure.
- **PDF generation is email-delivered, not a direct download:** clicking Generate PDF triggers an
  email-notification flow identical in shape to CSV export, not an immediate browser download.

## Related pages

- docs/wiki/05-cookie-manager/cookie-list-categories.md
- docs/wiki/17-reports.md

## Source

Derived from `ai-context/cases-consent-log.json` (23 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
