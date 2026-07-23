# Wiki change log

Append-only record of changes applied to `docs/wiki/` by `/wiki-sync`. Each entry lists what
changed, why, and its source (case id / live check / progress file) — a clean feed for the
separate project that consumes `docs/wiki/`, so it never has to diff the whole tree to find what
moved.

## [2026-07-23] ingest | 03. Dashboard

- Added `docs/wiki/03-dashboard.md` — first page for this section, which previously had no wiki
  page at all. Source: 9 backfilled `ai-context/cases-dashboard-*.json` files (88 TestRail cases,
  IDs 36612–36830), all `grill_status: "not-tracked-by-repo"` since they were published outside
  this repo's normal pipeline. About 20 of the 88 cases were live-verified this run (login as
  `free` and `ultimate` QA accounts, empty/default-state facts only — no account-data mutation);
  the rest remain pipeline debt and are called out inline in the page's Known gaps section.
- Correction flagged (not applied to TestRail): `cases-dashboard-header.json` #36622 and
  `cases-dashboard-states.json` #36612/#36613 describe "Notifications" and "Profile" as two
  separate header controls; live-verified this run to actually be one combined account/profile
  menu button with "Notifications" as a nested menu item. Source: live check.
- Correction flagged (not applied to TestRail): `cases-dashboard-cookie-banner-status-card.json`
  #36620's installation-modal title quote uses a straight apostrophe; the live app renders a curly
  apostrophe. Cosmetic. Source: live check.
- Gap found: a "New: Classify cookies with AI" upsell button on the Cookie Summary card, present
  on both accounts checked, has no corresponding case in any Dashboard case file. Source: live
  check.
- Updated `docs/wiki/README.md`: corrected the stale "no case file exists yet" claim for section
  03 (9 case files actually exist, backfilled 2026-07-23), added the Dashboard page's table row,
  bumped the top-level coverage count from 23 to 24 pages, and removed Dashboard from the
  "sections with no case file" live-crawl list in Known gaps / next pass (moved it to the
  spot-check list instead, since it now has partial coverage).
