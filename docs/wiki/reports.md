# Reports

**Nav path:** Reports
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Page itself is not plan-gated. One element within it — the "Extra pageviews used" counter in the Pageviews summary box — only appears on paid plans (Basic or higher); see docs/wiki/billing-upgrade/plan-gates.md for the broader plan-gate inventory.

## Purpose
The Reports page gives a site owner a single place to see consent-collection and traffic trends over time, so they can confirm the banner is capturing consent as expected and track how many pageviews are being tracked against their plan's limit.

## Page structure
The page is reached via the "Reports" link in the top navigation bar. It displays two cards side by side:

- **Consent Trends** (left card) — title label top-left, a range-selector dropdown top-right.
  - Empty state: an icon plus the text "No visitor consent has been recorded yet. Make sure you've enabled consent logging", where "consent logging" is a clickable link that opens the Advanced Settings page.
  - Populated state: a donut chart with the total consent count and the label "Total Consents" centered inside the donut. A legend to the right of the chart lists three entries with color markers — "Accepted" (green), "Rejected" (red), "Partially Accepted" (blue). Hovering a segment shows a two-line tooltip: percentage on line 1 (e.g. "50%"), consent type and count on line 2 (e.g. "Accepted: 1").
- **Pageviews** (right card) — title label top-left, a range-selector dropdown top-right.
  - Always-visible summary box above the chart area, showing: total pageviews count, current date range, and — on paid plans only — an "Extra pageviews used" counter (reads 0 when there have been no overages). An info icon next to "Total pageviews" shows a tooltip on hover explaining the total includes the monthly plan limit plus any extra pageviews.
  - Empty state (below the summary box): an icon plus the text "No pageviews found!".
  - Populated state: a line chart replacing the empty state. Y axis shows pageview counts; X axis shows the time span for the selected range in "MMM D, YYYY" format (e.g. "Jul 2, 2026"). Hovering a data point shows a two-line tooltip: date in "MMM D, YYYY" format on line 1 (e.g. "Jul 4, 2026"), pageview count followed by the word "pageviews" on line 2 (e.g. "1 pageviews").

Both cards' range-selector dropdowns expand to the same four options: "Last 7 days" (default), "Last 30 days", "Last 1 year", "Custom range". Selecting "Custom range" opens a date picker (calendar) for choosing a custom date range.

## Workflows

1. **View consent trends for the default period**
   1. Navigate to Reports via the top navigation bar.
   2. If no consent data has been recorded, the Consent Trends card shows its empty state with the "consent logging" link.
   3. If consent data exists, the card shows a donut chart defaulted to "Last 7 days", with the Accepted/Rejected/Partially Accepted legend and center total.
   4. Hover any segment to see the percentage + count tooltip.

2. **Jump to consent logging settings from an empty Consent Trends card**
   1. On the Consent Trends card's empty state, click the "consent logging" link.
   2. Result: the Advanced Settings page is displayed.

3. **Filter Consent Trends by time period**
   1. Click the range-selector dropdown on the Consent Trends card.
   2. Choose "Last 7 days" (default), "Last 30 days", "Last 1 year", or "Custom range".
   3. For "Custom range", a calendar appears; select a date range.
   4. Result: the card's chart updates to the selected period's consent data. If the selected custom range has no consent data, the card reverts to the empty state.

4. **View pageview trends for the default period**
   1. Navigate to Reports.
   2. If no pageviews have been tracked, the Pageviews card shows the "No pageviews found!" empty state below the summary box.
   3. If pageview data exists, a line chart replaces the empty state, defaulted to "Last 7 days".
   4. Hover a data point to see the date + pageview count tooltip.

5. **Filter Pageviews by time period**
   1. Click the range-selector dropdown on the Pageviews card.
   2. Choose "Last 7 days" (default), "Last 30 days", "Last 1 year", or "Custom range".
   3. For "Custom range", a calendar appears; select a date range.
   4. Result: the chart updates to the selected period's pageview data, and the X axis reflects the selected range's date boundaries. If the selected custom range has no pageview data, the card reverts to the empty state.

6. **Check extra pageviews usage (paid plans only)**
   1. On a Basic-or-higher plan, navigate to Reports.
   2. Observe the Pageviews card's summary box: total pageviews count, "Extra pageviews used" counter (0 if no overage), and current date range.
   3. Hover the info icon next to "Total pageviews" to see a tooltip explaining the total = monthly plan limit + extra pageviews.

7. **Cross-check Reports data against the Dashboard**
   1. Note the Consent Trends and/or Pageviews values shown on Reports for a given period.
   2. Compare against the equivalent widgets on the Dashboard (Consent Trends Card / Pageviews Card).
   3. Result: values should match — Reports and Dashboard draw from the same underlying data.

## Validation & edge cases
- **No consent data recorded:** Consent Trends card shows its empty state (icon + "No visitor consent has been recorded yet..." message with the "consent logging" link), regardless of range selected.
- **No pageviews tracked:** Pageviews card shows "No pageviews found!" empty state below the summary box; the summary box itself (with the total-pageviews row) still renders even in this state.
- **Custom range selected with no data in range:** both cards independently revert to their respective empty states rather than showing a stale chart.
- **Free plan vs. paid plan:** the "Extra pageviews used" counter row in the Pageviews summary box is present only on paid plans (Basic or higher); free-plan behavior for that row is (not captured in source data — needs live verification).
- **Extra pageviews counter at zero:** displays "0" rather than being hidden, when no overage has occurred on a paid plan.
- Boundary behavior at the edges of each range option (e.g., exact 7-day/30-day/1-year cutoffs) is (not captured in source data — needs live verification).
- Error/failure states (e.g., chart failing to load, API error) are (not captured in source data — needs live verification).

## Related pages
- docs/wiki/consent-log.md — underlying consent event log that Consent Trends aggregates.
- docs/wiki/dashboard (Consent Trends Card / Pageviews Card, once written) — Dashboard equivalents that Reports data is cross-checked against.
- docs/wiki/billing-upgrade/plan-gates.md (once written) — plan-gating reference for the "Extra pageviews used" counter and other paid-plan-only elements.

## Source
Derived from `ai-context/cases-reports.json` (6 TestRail cases — thin, may need a live-crawl follow-up). Drafted 2026-07-14, not yet live-verified against the QA app.
