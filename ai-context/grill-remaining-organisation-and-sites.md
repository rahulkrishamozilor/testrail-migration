# Grill handoff — Organisation and Sites

**PUBLISHED 2026-07-10 — all 66 cases created in TestRail v2 (suite 16), IDs 37294-37359.**
Source file renamed to `ai-context/cases-organisation-and-sites.json` (the `--write-back` step
does this automatically once every case has an id). Section breakdown: Organisation Management
(1824) 11, Site Management (1825) 26, Site Transfer (1826) 18, Permissions > Admin (1775) 6,
Permissions > Editor (1776) 4, Billing & Upgrade > Plan Gates (1793) 1. Nothing left to migrate
for this section — this handoff doc is now historical context only.

---

- Draft (source of truth): `ai-context/draft-organisation-and-sites.json` (66 cases) — superseded, see note above
- Last grilled: 2026-07-10T11:34:17Z
- Tally: 44 confirmed, 12 fixed, 0 needs-manual-check, 6 skipped, 4 suggested
- Nothing published to TestRail. Resume with `/grill-section organisation and sites` — it auto-skips cases that already have a `grill_status`.

## Environment / accounts
- Env `qa2.kilohub.com`; route **/settings/organizations-and-sites** (Profile menu > Organisations & Sites).
- Login: the form autofills the shared test password — set the email field to the target account and click Log In (never type/print the password). Accounts in `qa-accounts.json`.
- `disposableuser` — verified; sites jd.com (Basic, cancelled sub), i.lj (Basic, suspended), jih.ko (Pro). Best for functional/mutating + billing states.
- `adminuser` (mcp3) / `editoruser` — Admin / Editor members of hud's org (Acc 1716); for permission cases.
- `multiplewebsitesuser` (rahulkrishna+hud@mozilor.com) — same "hud" account, stocked with >50 sites (org "Rahulkrishna+mcp3's organisation", ID 1736) across 2 pages, including several Suspended/Free sites. Used 2026-07-10 to confirm the pagination case. Also Acc ID 1716 (the account owning that org) is the same account `adminuser`/`editoruser` are Admin/Editor members of — used 2026-07-10 to live-verify both ownership-transfer cases (transfer hud -> editoruser, confirm, transfer back editoruser -> hud to restore state). Still a candidate 2nd recipient account for the cross-account site-transfer cases in blocker B below — not yet attempted there.
- CAVEAT: stale Playwright profile lock across MCP reconnects — if you see 'Browser is already in use', kill the orphaned `ms-playwright-mcp` chrome + remove its Singleton* files, then retry.

## NOT verified — grouped by blocker

### D. Skipped — backend state / email inbox / time
- [destructive-precondition] Verify that the Banner disabled (pageview limit exceeded) status displays in the website details
- [destructive-precondition] Verify that the Payment failed status displays with the Retry Payment action
- [email-required] Verify that the destination owner receives the site transfer request email
- [email-required] Verify that rejecting a site transfer request cancels the transfer
- [time-dependent] Verify accepting a site transfer request after the 7-day expiry
- [time-dependent] Verify that a transferred site is suspended when no payment method is added before the next renewal date

## Suggested (gap-hunt) — approve/reject at /migrate-section
- Verify that the website search bar filters the site list by URL
- Verify that the Copy configuration option copies a site's configuration
- Verify that the Add staging site option creates a staging site
- Verify that a site URL entered with an http/https protocol prefix is accepted and saved as-is (NEW 2026-07-10)

## Findings to carry forward
- Permission blocks = disabled control + role tooltip (exact text lives in each permission case's `expected`).
- Live labels are British/sentence-case: '+ New site', '+ New organisation', 'Next renewal', 'Add new organisation'/'Add organisation', 'Delete site?'.
- Live validation strings: 'Website already exists', 'Valid website required', 'This field is required', 'Please enter a valid site name', 'Organisation name is too long'.
- Editor-only divergence: Editor cannot edit site URL/name or org name (Admin can) -> 14 > Editor.
- Added AO-only permission cases: cannot transfer a site, cannot cancel a subscription.
- Ownership transfer (both cases) confirmed live via hud <-> editoruser (Acc 1716). Note: the page does NOT reactively update after a successful transfer — needs a reload to reflect the new owner/role. Not a bug per se, just something to know if re-testing manually.
- 2026-07-10 v1 audit of the 13 Site Transfer cases: restored verbatim banner/tooltip/email copy on 7 cases (previously paraphrased during v2 collapsing) — see each case's `rewrite_notes` for what changed and which C-id it was restored from.
- Found + added a genuine gap during that audit: a Shopify-connected site (created via the Shopify app install, which just makes a normal website record in the webapp) is blocked from cross-account transfer with the error "This site can only be transferred to an organization you own, as it is connected to your account via CookieYes' Shopify app." — sourced from C9717/C17212. C11237 (filed under the Shopify section but showing the generic banner instead) is a faulty/mislabeled duplicate from a Suite-6 section mix-up — excluded as a source. New case needs a Shopify-connected test site (none currently in `qa-accounts.json`) to live-verify.
- Same-account site transfer confirmed live on disposableuser: created a 2nd org, transferred jd.com into it (banner + toast text matched v2 draft verbatim), then transferred jd.com back and deleted the temp org to restore state. Incidental note: the "Delete organisation" More-menu option appeared even on the temp org right after it was emptied back to 0 sites — worth re-checking whether the earlier-confirmed rule ("no-sites org shows Edit only, org-with-sites shows Edit+Delete") is actually about site count or about default-vs-non-default org; didn't chase this further.
- IMPORTANT — cross-account transfer destination precondition corrected (2026-07-10): a destination org from "another account" is NOT just any org that exists on the platform. Traced the chained precondition (C9718) behind C9719/C9737/C11238/C11240 — an org only becomes selectable in a site's "Destination organization" dropdown after the sender account owner has been invited as a team member (Admin/Editor) into that org via Profile menu > Teams > "Invite new user" (on the recipient's side) and has accepted the invite. C9718 also has the recipient upgrade to a paid (Basic) plan before inviting — untested whether Team invites actually require this, but assume so until disproven. All 7 blocker-B cases (transfer initiates request, Shopify-blocked, cancel request, review-transfer-request login flow, website-transfer-request page render, accept, add-payment-method) have this full setup recipe spelled out inline in their `preconditions` field, formatted per migration-conventions.md §2e (numbered list with real line breaks, intro sentence, blank line, then navigation state). `qa-accounts.json` has no pair already in this "invited as team member into a DIFFERENT account's org" configuration — `adminuser`/`editoruser` are members of hud's own org, which is the reverse relationship and doesn't satisfy this precondition.
- 2026-07-10: all 7 of those blocker-B cases manually reviewed and approved by the user (content/preconditions confirmed accurate as written) — NOT executed live against qa2.kilohub.com. `grill_status` set to `confirmed` based on manual review, not a live run. If a live run is ever desired: pick two accounts (e.g. disposableuser as sender, hud as recipient, or vice versa), run the Teams invite + accept steps once, then the whole chain (initiate -> cancel/review/login/accept/payment-method) can be walked through in sequence on that same pair. The Shopify-blocked case additionally needs a Shopify-connected test site, which doesn't exist in `qa-accounts.json` yet.
- 2026-07-10 RESOLVED — over-length URL/site-name cases were false negatives, not missing validation. Root cause: my first grill pass used raw JS `dispatchEvent`/direct `.value` assignment instead of Playwright's real `.fill()`/typing, and never actually clicked "Save Changes" — the error text only renders on submit, not on type/blur. Re-tested properly on disposableuser (jd.com): entering >75 chars and clicking Save Changes surfaced "URL should be less than 75 characters" (site URL, matches draft verbatim) and "Site name must be 75 characters or less" (site name, draft had 'Maximum allowed characters is 75' from v1 C6789 — wrong, now fixed to live text). Both now `confirmed`/`fixed`. Lesson: always actually click the submit button when grilling submit-triggered validation, don't infer from disabled-state alone.
- 2026-07-10 gap-hunt finding (site URL protocol prefix): entering a site URL with an "https://" prefix (e.g. "https://valid-test-domain.com") saved successfully with no error, and the Site URL column displayed it verbatim including the prefix -- no stripping/normalisation to a bare domain. No existing case tests a protocol-prefixed URL. Added as a new `suggested` case. Reverted jd.com back to its original bare-domain URL afterward.
- Also ruled out during this pass: no separate "excessive repeated-label" rejection exists for site URLs -- that earlier appearance was itself an artifact of the same raw-DOM-event testing bug, not real product behavior. Unchanged-value Save Changes is disabled by default (expected, no gap).
- 2026-07-10, caught during /migrate-section review: "Add staging site" is plan-gated. Verified live -- disabled with a premium/upgrade badge icon on Free plan (freeplansite/hd.com), enabled on Basic (disposableuser/jd.com). Per migration-conventions.md §6, added as its own `plan_gate_flag: true` case (routes to 11. Billing & Upgrade > Plan Gates, not the feature section) rather than as a step in the functional "Add staging site" case. No existing Plan Gates case covers this touchpoint yet (checked cases-plan-gates-new.json) -- may need merging into a consolidated per-plan walkthrough case later.
- 2026-07-10, IMPORTANT test-hygiene finding: while checking role-based permission blocks for "Add staging site", discovered `editoruser`'s role in hud's org (1736) had silently become **Admin**, not Editor -- confirmed via Team page and `GET /api/v2/user` (`organization_users[].role_slug`). Root cause: the earlier hud <-> editoruser ownership-transfer test round-trip triggered the app's documented "previous owner retains Admin access" behavior a second time, upgrading editoruser from Editor to Admin as a side effect. Fixed by logging in as hud and using Team > (⋯) > "Change role" to set editoruser back to Editor. **Any account used as an ownership-transfer recipient should be treated as role-tainted afterward** -- verify its role_slug before reusing it for permission tests. Noted directly in `qa-accounts.json`'s editoruser entry.
- With the role corrected, re-verified all Editor-blocked site items on jf.com (Org 1736): Edit site URL/name, Transfer site, Delete site, Cancel subscription all still show disabled for Editor -- the earlier confirmations for those (made before this session's ownership-transfer mishap) hold up. Org-actions (⋯) menu absence for Editor (org rename) also re-confirmed.
- NEW permission case added: "Add staging site" is Editor-blocked (disabled, no icon/tooltip on hover) but Admin-enabled -- a genuine hierarchy divergence, same pattern as site/org name editing. Added `permission_flag: true` case routing to 14 > Editor. "Copy configuration" was also checked in the same pass and is enabled for both Admin and Editor -- no permission case needed for it.
