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

## [2026-07-23] lint | 11. Billing & Upgrade > Plan Gates

- Corrected `docs/wiki/11-billing-upgrade/plan-gates.md`: prior Source section cited
  `ai-context/cases-plan-gates-new.json`, a file that does not exist and is not in
  `ai-context/manifest.json` — no such standalone case file was ever created for this section.
  Replaced with the real location of Section 11's content: three consolidated Layer 2 cases
  (`[Plan Gates] Privacy Policy Generator — Free/Basic/Pro plan`) physically stored in
  `cases-privacy-policy-generator.json`, all `grill_status: confirmed`. Source: published case
  notes (Step 1b).
- Added: full Privacy Policy Generator plan-gate matrix (6 touchpoints x Free/Basic/Pro/Ultimate)
  to Page structure/Workflows/Validation & edge cases — previously undocumented; the page
  described only a single thin Cookie Banner touchpoint case as if it were this section's own
  content. Source: the three cases above, live-verified 2026-07-23 (no additional live check
  needed — source already carries its own 2026-07-23 verification date).
- Clarified: this section owns only consolidated Layer 2 walkthrough cases, not Layer 1
  touchpoint cases (those stay in their feature sections and forward-link here) — the prior page
  text conflated a Layer 1 case with this section's own content.
- Gap surfaced (not resolved, flagged in Known gaps): every other feature section with a
  plan-gated control still has only scattered Layer 1 cases, no consolidated Layer 2 case —
  matches the open suite-wide question already tracked in `coverage-gaps.md` §11.
- Updated `docs/wiki/README.md`: corrected the Plan Gates table row (source, case count,
  freshness), corrected the stale "no case file exists yet" claim for section 10's My Account
  (`cases-my-account.json` exists, 28 cases, just not yet drafted into a page), and added a
  top-of-file coverage note for the Plan Gates correction.

## [2026-07-23] ingest | 14. Permissions

- Added `docs/wiki/14-permissions.md` — first page for this section, which previously had no
  wiki page at all despite real, already-verified source material sitting unused in three other
  sections' case files. Source: 13 permission-divergence cases (`permission_flag: true`) found
  across `cases-organisation-and-sites.json` (10), `cases-team.json` (2), and
  `cases-colours.json` (1) — all `confirmed`/`fixed` except one `skipped:plan-gated` (an
  already-covered plan/role interaction) — plus `testrail-suite-v2.md`'s permission hierarchy
  table. No live check needed: none of Step 3's triggers fired (single, non-conflicting,
  already-live-verified source per fact).
- Surfaced (not a defect, a documented finding): three different UI mechanisms enforce these
  role restrictions inconsistently — disabled+tooltip, disabled+no tooltip, and control not
  rendered at all — captured in the new page's Validation & edge cases as a real product
  inconsistency, not smoothed over.
- Gap flagged (not resolved): whether the one confirmed Account-Owner-only plan-upgrade
  restriction (found on one Cookie Banner nudge) generalizes to every upgrade nudge app-wide is
  unconfirmed — recorded in the page's Known gaps and added to README's spot-check backlog.
- Updated `docs/wiki/README.md`: added the Permissions table row, bumped the top-level coverage
  count from 24 to 25 pages, removed Permissions from the "sections with no case file" live-crawl
  list (moved its one open question to the spot-check list instead).
- Correction to this log's own prior entry: the My Account case count was previously stated as
  "47" in `README.md`'s "Not yet documented" line and this file's entry above — that number was
  the case file's disk size in kilobytes (47.3K), not its case count. Corrected both to the
  actual count, 28, confirmed directly against `cases-my-account.json`.

## [2026-07-23] ingest | 10. Profile & Account > My Account

- Added `docs/wiki/10-profile-account/my-account.md` — first page for this section, which
  previously had no wiki page despite a fully fetched/grilled/published 28-case file. Source:
  `cases-my-account.json` (grilled 2026-07-08, published 2026-07-09) — 21 routine-confirmation
  cases skipped per Step 2, 7 change-signaling cases carried forward (wording/label corrections,
  two new gap-found cases with no Suite 6 precedent, one previously-undocumented "Email
  notifications" section). No live check triggered per Step 3: no conflicting sources, nothing
  `not-tracked-by-repo` (all cases are a properly grilled/published export, just with a few
  deliberately unexecuted steps — see below), and the facts already carry their own
  2026-07-08 verification date.
- **Gap found, surfaced as a defect, not smoothed over:** the Change password flow has a
  confirmed, reproducible bug — after a successful password change, the account settings page
  goes completely blank before auto-logout, instead of showing the expected in-place
  confirmation. The password change itself does take effect. Flagged in the new page's Known
  gaps for engineering review. Source: live check performed during the original grill pass.
- Flagged as known gaps (deliberately unexecuted, not silently dropped): account deletion's
  final confirm click (irreversible, no disposable test account available) and the Manage Email
  Preferences page's "Save preferences" action (skipped to avoid mutating the shared test
  account's real subscription state). Both need a disposable account to finish safely — not
  re-attempted in this pass.
- Updated `docs/wiki/README.md`: added the My Account table row, bumped the top-level coverage
  count from 25 to 26 pages, removed My Account from the "sections with no case file" live-crawl
  list, and added its three follow-up items to the spot-check list.

## [2026-07-23] lint | 10. Profile & Account > My Account (live spot-check)

- Live-verified via Playwright against the QA app, per the user's request and explicit approval
  for account deletion specifically. Used `disposableuser` (per `qa-accounts.json`) for
  reversible checks, and a freshly created signup account (deleted afterward as part of the test
  itself) for account deletion and the unverified-email 2FA tooltip, to avoid touching any shared
  fixture irreversibly.
- **Confirmed, resolving three prior known gaps:** account deletion's final action (deletes
  immediately; deleted credentials then correctly fail login with "Invalid email/password.
  Please try again"), "Save preferences" on Manage Email Preferences (toaster "Your preferences
  are saved!", persists after reload), and the 2FA setup button's unverified-email tooltip
  ("Please verify your email address to set up 2FA.", confirmed verbatim against a fresh
  unverified signup).
- **Confirmed exact text, previously untested:** the expired-verification-code error ("The
  verification code has expired. Please resend code and try again.") — sent a real code to a
  mozilor.com inbox, waited past its 10-minute window, submitted it, got the exact documented
  message.
- **New facts added:** the page's route (`/settings/account`), the Manage Email Preferences
  route (`/settings/manage-preferences`), and a previously-unknown second variant of that page
  (different intro copy, plus an "Unsubscribe from all emails" button) found by accident —
  its trigger not yet identified, flagged as a new known gap rather than chased down.
- **Unresolved contradiction escalated, not auto-resolved (per Step 4):** the previously
  documented Change-password "blank page, no toaster" defect did not reproduce as originally
  described — a proper "Your password has been changed!" dialog appeared — but the page still
  went blank for a few seconds before redirecting to Log In, on both attempts. Two readings
  (dialog was added/fixed with the blank transition left over, vs. the dialog's appearance being
  itself intermittent) are both live in the page's Known gaps; deliberately not resolved to one
  or the other.
- Updated `docs/wiki/README.md`: My Account's table row and the spot-check backlog entry both
  updated to reflect what's now confirmed vs. still open.

## [2026-07-23] lint | 10. Profile & Account > My Account (contradiction resolved by user)

- The Change-password post-submit contradiction from the entry above was escalated per Step 4
  and has now been resolved by explicit user judgment: the brief blank transition before the
  auto-logout redirect is expected during that step (attributed to environment performance, not
  a functional defect) and the "Your password has been changed!" dialog is the correct, expected
  confirmation. Updated Workflow 2 in `docs/wiki/10-profile-account/my-account.md` to state this
  plainly as documented fact, and moved the item from Known gaps to the page's "resolved this
  pass" note. Source: user decision, 2026-07-23.
- Updated `docs/wiki/README.md`'s My Account row and spot-check backlog entry to drop the
  contradiction, leaving only the real-inbox email round-trip and 2FA-disable toaster text as
  open follow-ups for this page.

## [2026-07-23] lint | repo-wide (path rename, no content change)

- Dropped every `testrail-suite-v2.md` section-number prefix from `docs/wiki/` folder and file
  names — the wiki is meant to stand alone from the migration's own provenance (per
  `CONVENTIONS.md` §2), and a TestRail section number baked into every path is exactly that kind
  of coupling. The ordering it gave is unaffected: `README.md`'s numbered `##` headings still
  carry it. Renamed: `01-authentication/` → `authentication/`, `03-dashboard.md` → `dashboard.md`,
  `04-cookie-banner/` → `cookie-banner/`, `05-cookie-manager/` → `cookie-manager/`,
  `06-consent-log.md` → `consent-log.md`, `07-languages.md` → `languages.md`,
  `08-advanced-settings.md` → `advanced-settings.md`, `09-legal-policies/` → `legal-policies/`,
  `10-profile-account/` → `profile-account/`, `11-billing-upgrade/` → `billing-upgrade/`,
  `14-permissions.md` → `permissions.md`, `17-reports.md` → `reports.md`.
- Fixed every internal link across `docs/wiki/*.md` (including `README.md`) to the new paths, plus
  two references in the repo root's `coverage-gaps.md` and `BACKLOG.md`. `log.md`'s own past
  entries above are intentionally left referencing the old paths (they were correct at the time
  they were written; append-only means history isn't rewritten) — read any old path in this file
  as the section's current page under its new, unnumbered name.
- Added the no-numbered-prefix rule to `CONVENTIONS.md` §5 so future pages don't reintroduce this.
  Source: user request, 2026-07-23.
