# Organisations & Sites — Site Management

**Nav path:** Profile & Account > Organisations & Sites > Site Management
**Route:** `/settings/organizations-and-sites` (site rows). "+ New Site" opens the "Add a new
site" page at `/v1/websites/create`. "Change Plan" / "Choose Plan" open the plan-upgrade page at
`/v1/websites/<id>/upgrade`.
**Roles:** Adding a site — **Account Owner only** (Admin and Editor blocked: "+ New Site" is
disabled with a tooltip). Deleting a site — **Account Owner only** (Admin and Editor both
blocked: "Delete site" is disabled in the More (⋯) menu with a tooltip). Editing a site's URL or
name — **Account Owner and Admin** (Editor blocked: "Edit site URL" / "Edit site name" are
disabled in the More (⋯) menu with a tooltip; Admin and Account Owner are unrestricted).
Cancelling a subscription — **Account Owner only** (Admin and Editor blocked: "Cancel
subscription" is disabled with a tooltip). Adding a staging site — **Account Owner and Admin**
(Editor blocked: "Add staging site" is disabled for an Editor, no tooltip observed, just an
aria-disabled state — Account Owner and Admin are unrestricted). "Copy configuration" carries
**no role restriction** — confirmed enabled for both Admin and Editor. See
`docs/wiki/14-permissions.md` for the app-wide role hierarchy.
**Plan gating:** "Add staging site" is locked with a premium/upgrade badge icon and disabled on
the **Free plan**; it is enabled (no badge) on Basic and above — the gate boundary is Free vs.
Basic-or-higher, not Pro-or-higher. See `docs/wiki/11-billing-upgrade/plan-gates.md` for other
plan gates.

## Purpose
Site Management covers the website rows listed under each organisation on the Organisations &
Sites page: adding new sites, the per-site details columns, subscription-status variants and
their billing entry points, editing a site's URL/name, and the remaining site-level More (⋯)
menu actions (copy configuration, staging site, delete).

## Page structure
Each website row (under an expanded organisation on the Organisations & Sites page) displays the
following columns: **Site URL**, **Site name**, **Created date**, **Plan**, **Next Renewal**,
a **Change Plan** button, a **Manage Site** button, and a **More (⋯)** option.

- **Site URL column** — can carry a status message beneath the URL depending on the site's
  subscription state: "Banner disabled (Pageview limit exceeded)" with an "Upgrade now" link and
  help icon; "Payment failed" with a help icon; "Suspended" with a help icon; "Transfer request
  initiated" with a tooltip (see `site-transfer.md`); or "No payment method available for this
  site." with an "Add payment method" link (see `site-transfer.md`).
- **Plan column** — shows the plan name. A paid plan (Basic / Pro / Ultimate) shows the plan name
  with price and billing cycle, e.g. "Pro $X /Monthly". A Free-plan site shows "Free" with a "Try
  Pro for free" action in place of the Change Plan button. Additional links/labels can appear
  under the plan details: "Switch to Annual - Save 17%" (monthly paid plans), a scheduled-
  downgrade notice with a "Cancel Downgrade" link, or a cancelled-subscription notice with a
  "Reactivate subscription" link.
- **Next Renewal column** — shows the next renewal date, or is blank for Payment failed /
  Suspended sites, or shows a "Subscription will be cancelled and the site will be deleted on
  Month DD, YYYY." notice (with help icon) for a cancelled subscription pending deletion.
- **Change Plan / Manage Site buttons** — "Manage Site" always navigates to that site's Dashboard.
  "Change Plan" opens the plan-upgrade page; it is replaced by "Retry Payment" for a
  Payment-failed site and by "Choose Plan" for a Suspended site or a Banner-disabled
  (pageview-limit-exceeded) site.
- **More (⋯) menu** — contains "Edit Site URL", "Edit site name", "Copy configuration", "Add
  staging site", "Cancel subscription", "Transfer Site" (or "Cancel transfer request" once a
  request is outstanding — see `site-transfer.md`), and "Delete Site".
- **Website search bar** ("Search by website URL") — sits in the page header; filters the visible
  site list to URLs matching the search term, and clearing it restores the full list.

## Workflows

**1. Adding a new site**
1. On the Organisations & Sites page, with a verified account email, click "+ New Site" in the
   header.
2. Result: the "Add a new site" page is displayed.

**2. Filtering the site list**
1. Type part of a website URL into "Search by website URL" and submit.
2. Result: the site list filters to only websites whose URL matches the search term.
3. Clear the search box.
4. Result: the full site list is restored.

**3. Viewing a site's dashboard**
1. Click "Manage Site" on a website row.
2. Result: that site's Dashboard page is displayed.

**4. Changing a site's plan**
1. Click "Change Plan" on a website row.
2. Result: the plan-upgrade page for that site is displayed.

**5. Switching to annual billing**
1. On a site with a monthly paid plan (Basic, Pro, or Ultimate), locate "Switch to Annual - Save
   17%" under the plan details in the Plan column.
2. Click "Switch to Annual - Save 17%".
3. Result: the "Save 17% with Annual Plan" pop-up opens, showing the Site URL, current monthly
   plan and price, new yearly plan and price, and Cancel / "Upgrade to Annual" buttons.

**6. Reactivating a cancelled subscription**
1. On a site with a cancelled subscription, observe the Next Renewal column: "Subscription will
   be cancelled and the site will be deleted on Month DD, YYYY." plus a "Reactivate subscription"
   link and help icon.
2. Click "Reactivate subscription".
3. Result: the "Reactivate your subscription?" pop-up opens, stating the subscription will be
   reactivated immediately, with Cancel / "Reactivate subscription" buttons.
4. Click "Reactivate subscription" in the pop-up.
5. Result: the subscription is reactivated and a next renewal date is displayed under Next
   Renewal.

**7. Cancelling a subscription**
1. Open a paid-plan site's More (⋯) menu and select "Cancel subscription".
2. Result: the "Cancel your [Plan_name] subscription?" confirmation pop-up is displayed.

**8. Scheduling and cancelling a downgrade**
1. Schedule a downgrade via Change Plan > Plans list page > Downgrade > Confirm Downgrade (the
   downgrade takes effect at the end of the current billing cycle).
2. Result: the website row shows "Your current plan will be downgraded to [downgraded_plan] on
   [Month DD, YYYY]" alongside a "Cancel Downgrade" link.
3. Click "Cancel Downgrade".
4. Result: the "Cancel downgrade?" pop-up opens with the text "[website] will continue with the
   current plan." and "Go back" / "Cancel downgrade" buttons.
5. Click "Cancel downgrade" in the pop-up.
6. Result: the scheduled downgrade is cancelled, the downgrade label disappears from the row, and
   the site remains on its current plan.

**9. Editing a site URL**
1. Open a website's More (⋯) menu and select "Edit Site URL".
2. Result: the "Edit Site URL" pop-up opens with a "Site URL*" field pre-filled with the current
   URL, an alert banner about URL-change legal-compliance steps, and Cancel / "Save Changes"
   buttons.
3. Enter a valid new URL and click "Save Changes".
4. Result: the Site URL column updates to the new URL. A URL entered with an "http://" or
   "https://" prefix is accepted and saved exactly as entered (no stripping or normalisation to a
   bare domain).

**10. Editing a site name**
1. Open a website's More (⋯) menu and select "Edit site name".
2. Result: the "Edit site name" pop-up opens with a "Site name*" field pre-filled with the
   current name and Cancel / "Save Changes" buttons.
3. Enter a valid new name and click "Save Changes".
4. Result: the Site name column updates to the new name.

**11. Copying a site's configuration**
1. Open a website's More (⋯) menu and select "Copy configuration".
2. Result: a copy-configuration flow opens (destination/target selection). Exact flow contents
   not captured in source data — needs live verification.

**12. Adding a staging site**
1. Open a website's More (⋯) menu and select "Add staging site" (Free plan: the option is shown
   with a premium/upgrade badge icon and is disabled instead — see Validation & edge cases).
2. Result: an add-staging-site flow opens. Exact flow contents not captured in source data —
   needs live verification.

**13. Deleting a site**
1. Open a website's More (⋯) menu and select "Delete Site".
2. Result: the "Delete site?" confirmation pop-up is displayed with the warning "The site <url>
   will be permanently deleted from this account, including your subscription and all associated
   data. This action is irreversible." and Cancel / "Delete site" buttons.
3. Click "Delete site" in the confirmation pop-up.
4. Result: the site is deleted from the organisation.

## Validation & edge cases
- **Site URL — duplicate:** entering a URL that already exists on the account shows "Website
  already exists" and the site is not saved.
- **Site URL — invalid:** shows "Valid website required".
- **Site URL — empty:** shows "This field is required".
- **Site URL — over-length:** a URL longer than 75 characters shows "URL should be less than 75
  characters" (this error only renders after clicking "Save Changes", not from typing/blur
  alone).
- **Site URL — Cancel:** clicking Cancel on the Edit Site URL pop-up closes it with the URL
  unchanged.
- **Site name — empty:** shows "Please enter a valid site name".
- **Site name — over-length:** a name longer than 75 characters shows "Site name must be 75
  characters or less" (also only renders after clicking "Save Changes").
- **Subscription status — Banner disabled (pageview limit exceeded):** "Banner disabled
  (Pageview limit exceeded)" with "Upgrade now" link and help icon under the Site URL; "Choose
  Plan" button shown in place of Change Plan. Requires backend fixture state to reproduce
  (pageview count forced to the plan limit) — not reachable via UI alone.
- **Subscription status — Payment failed:** "Payment failed" status with help icon; blank Next
  Renewal; no "Switch to Annual" link; "Change Plan" replaced by "Retry Payment", which opens the
  Stripe invoice page.
- **Subscription status — Suspended:** "Suspended" status with help icon; blank Next Renewal; no
  "Switch to Annual" link; "Choose Plan" button shown (opens the plan-upgrade page) in place of
  Manage Site's usual companion action.
- **Plan label — Free plan:** shows "Free" with a "Try Pro for free" action instead of Change
  Plan.
- **Role-restricted — Admin and Editor cannot add a site:** "+ New Site" disabled with tooltip
  "Only the Account Owner can add a new site."
- **Role-restricted — Admin and Editor cannot delete a site:** "Delete site" disabled in the More
  (⋯) menu with tooltip "Only the Account Owner can delete a site."
- **Role-restricted — Admin and Editor cannot cancel a subscription:** "Cancel subscription"
  disabled with tooltip "Only the Account Owner can cancel subscription."
- **Role-restricted — Editor cannot edit a site URL:** "Edit site URL" disabled with tooltip "Only
  the Account Owner or an Admin can edit the site URL." (Admin and Account Owner unrestricted.)
- **Role-restricted — Editor cannot edit a site name:** "Edit site name" disabled with tooltip
  "Only the Account Owner or an Admin can edit the site name." (Admin and Account Owner
  unrestricted.)
- **Role-restricted — Editor cannot add a staging site:** "Add staging site" disabled for an
  Editor (aria-disabled, no tooltip observed); enabled for Admin and Account Owner.
- **Plan-gated — Add staging site on Free plan:** shown with a premium/upgrade badge icon and
  disabled; enabled with no badge on Basic and above.

## Related pages
- [Organisation Management](organisation-management.md)
- [Site Transfer](site-transfer.md)
- [Team](../team.md)
- [Paid Plan](../../11-billing-upgrade/paid-plan.md)
- [Permissions](../../14-permissions.md)

## Source
Derived from `ai-context/cases-organisation-and-sites.json` (66 TestRail cases total, split by
sub-topic — 33 of those cases feed this file). Drafted 2026-07-14, not yet live-verified against
the QA app beyond what is already noted from the source cases' own grill passes.
