# Organisations & Sites — Organisation Management

**Nav path:** Profile & Account > Organisations & Sites > Organisation Management
**Route:** `/settings/organizations-and-sites`
**Roles:** Organisation creation and deletion — **Account Owner only** (Admin and Editor both
blocked: the "+ New organisation" button is disabled with a tooltip for them, and the More (⋯)
menu that exposes "Delete organization" is a per-organisation control gated the same way as
rename). Renaming an organisation ("Edit organization name") — **Account Owner and Admin**
(Editor blocked: the organisation's More (⋯) control is not rendered at all for an Editor).
Account ownership transfer — **Account Owner only** (Admin and Editor blocked: the "Transfer
Ownership" button is not rendered on the Account Owner card for them). See
`docs/wiki/permissions.md` for the app-wide role hierarchy (Editor ⊂ Admin ⊂ Account Owner).
**Plan gating:** None captured in source data for this sub-topic — organisation create/rename/
delete and account ownership transfer are not plan-gated in the source cases.

## Purpose
Organisation Management covers the top section of the Organisations & Sites page: the Account
Owner card (including account ownership transfer) and the organisation dropdown(s) beneath it —
creating, renaming, and deleting organisations, and paging through an organisation's sites when
there are many.

## Page structure
The Organisations & Sites page (Profile menu > Organisation & Sites) is laid out top to bottom:

- **Header** — a "+ New site" button (disabled until the account email is verified) and, to its
  right, a "+ New organisation" button. A website search bar ("Search by website URL") also sits
  in the header (see `site-management.md` for how it filters the list).
- **Account Owner card** — displays the "Account Owner" title with an "Acc ID: [Account ID]"
  badge in the top right, a "Transfer Ownership" button, and the account owner's email address.
- **Organisation dropdown(s)** — below the email address. The default organisation is labelled
  "[Username]'s organization" with an "Org ID: [Organization ID]" badge, expanded by default, and
  each organisation row carries a More (⋯) control.
  - The More (⋯) menu on an organisation with **no sites** (e.g. a fresh default organisation)
    shows **only** "Edit organization name".
  - The More (⋯) menu on an organisation that **contains sites** shows both "Edit organization
    name" and "Delete organization".
- **Website-details rows** — under each expanded organisation, one row per site (columns: Site
  URL, Site name, Created date, Plan, Next Renewal, Change Plan, Manage Site, More (⋯)) — see
  `site-management.md` for the full column breakdown.
- **Pagination control** — appears at the bottom right of an organisation's card once that
  organisation has more than 50 sites, with page numbers and four navigation arrows: «
  (first page), ‹ (previous page), › (next page), » (last page).

## Workflows

**1. Creating a new organisation**
1. On the Organisations & Sites page, click "+ New organisation" in the header.
2. Result: the "Add new organisation" pop-up opens, showing an info banner reading "The new
   organisation will be added to your own account (Acc ID: [Account ID])", a mandatory
   "Organisation name*" field (placeholder "My organisation"), and Cancel / "Add organisation"
   buttons. "Add organisation" is disabled by default.
3. Enter a valid name in the "Organisation name" field.
4. Result: the "Add organisation" button becomes enabled.
5. Click "Add organisation".
6. Result: the pop-up closes and the new organisation appears as a dropdown in the Account Owner
   card with its own Org ID badge.

**2. Cancelling organisation creation**
1. Open the "Add new organisation" pop-up (as above).
2. Click "Cancel".
3. Result: the pop-up closes and no organisation is created.

**3. Renaming an organisation**
1. Click the More (⋯) control on an organisation and select "Edit organization name".
2. Result: the "Edit Organization name" pop-up opens with a field labelled "Organization name*
   (Org ID: [Organization ID])", pre-filled with the current name, and Cancel / "Save changes"
   buttons.
3. Change the name to a valid new organisation name.
4. Click "Save changes".
5. Result: the pop-up closes and the organisation dropdown updates to show the new name.

**4. Cancelling a rename**
1. Open "Edit Organization name" for an organisation (as above) and change the name in the field.
2. Click "Cancel".
3. Result: the pop-up closes and the organisation name remains unchanged.

**5. Deleting an organisation**
1. Click the More (⋯) control on an organisation **that contains sites** and select "Delete
   organization" (this option is not shown for an organisation with no sites).
2. Result: the "Delete organization?" pop-up opens with a permanent-deletion warning (the
   organisation and all associated user access will be removed and cannot be undone), an "I
   understand and want to delete this organization including all its data." checkbox, and
   Cancel / "Delete organization" buttons — "Delete organization" is disabled by default.
3. Tick the "I understand and want to delete this organization including all its data." checkbox.
4. Result: "Delete organization" becomes enabled.
5. Click "Delete organization".
6. Result: the pop-up closes and the organisation is removed from the Account Owner card.

**6. Paging through an organisation with more than 50 sites**
1. Expand an organisation that has more than 50 sites.
2. Result: the website list shows with a pagination control at the bottom right — page numbers
   plus «, ‹, ›, » arrows. On page 1, « and ‹ are disabled.
3. Click › (next page).
4. Result: the next page of sites is displayed.
5. Click » (last page).
6. Result: the last page is displayed and › and » become disabled.
7. Click « (first page).
8. Result: the original first page of sites is displayed again.

**7. Transferring account ownership**
1. Click "Transfer Ownership" in the top right of the Account Owner card.
2. Result: the "Transfer account ownership" pop-up opens with an info banner stating ownership
   can only be transferred if the new owner does not already own another account (and that the
   current owner retains Admin access), an alert banner stating the current payment method
   remains in use until the new owner replaces it, a "New owner*" dropdown, a "Your password*"
   field, and Cancel / "Transfer ownership" buttons.
3. Select a new owner from the "New owner*" dropdown.
4. Enter the current account owner's valid password in "Your password*".
5. Result: "Transfer ownership" becomes enabled.
6. Click "Transfer ownership".
7. Result: ownership transfers to the selected user, and the previous account owner's role
   changes to Admin. Note: the UI does not reactively update after a successful transfer — a
   page reload is needed to see the new state (owner-only controls such as "+ New site",
   "+ New organisation", Change Plan, and Switch to Annual become disabled for the former owner
   after reload).

## Validation & edge cases
- **Over-length organisation name (create or rename):** entering a name longer than 190
  characters shows "Organisation name is too long" under the field, and the Add/Save button
  stays disabled.
- **Invalid password on ownership transfer:** submitting an incorrect password shows an inline
  "Invalid password" error under "Your password*" plus a toast "Failed to transfer ownership:
  Invalid password"; ownership is not transferred.
- **Delete option visibility:** "Delete organization" only appears in the More (⋯) menu for
  organisations that already contain at least one site — a fresh, empty default organisation
  only exposes "Edit organization name".
- **Pagination boundaries:** « and ‹ are disabled on the first page; › and » are disabled on the
  last page. (Minor accessibility note, not a functional defect: the first/last-page arrow
  buttons' accessible name renders as the raw untranslated i18n key rather than a real label —
  the icons themselves render correctly.)
- **Role-restricted — Admin and Editor cannot create an organisation:** the "+ New organisation"
  button is disabled with tooltip "Only the Account Owner can create a new organisation."; no
  pop-up opens.
- **Role-restricted — Editor cannot rename an organisation:** the organisation's More (⋯) control
  is not rendered at all for an Editor (so "Edit organization name" is unreachable). Admin and
  Account Owner both see the control.
- **Role-restricted — Admin and Editor cannot transfer account ownership:** the "Transfer
  Ownership" button is not rendered on the Account Owner card for either role.

## Related pages
- [Site Management](site-management.md)
- [Site Transfer](site-transfer.md)
- [Team](../team.md)
- [Paid Plan](../../billing-upgrade/paid-plan.md)
- [Permissions](../../permissions.md)

## Source
Derived from `ai-context/cases-organisation-and-sites.json` (66 TestRail cases total, split by
sub-topic — 17 of those cases feed this file). Drafted 2026-07-14, not yet live-verified against
the QA app beyond what is already noted from the source cases' own grill passes.
