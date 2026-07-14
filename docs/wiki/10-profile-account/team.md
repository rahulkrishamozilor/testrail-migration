# Team

**Nav path:** Profile & Account > Team
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin can manage team (add/remove members, invite, modify roles); Editor is blocked from these actions — see docs/wiki/14-permissions.md
**Plan gating:** (not captured in source data — needs live verification; no case in this set asserts a seat-count limit or plan-gated cap on team size)

## Purpose
The Team page lets an Account Owner or Admin invite, view, and manage the people who have access to an organisation — assigning each member an Admin or Editor role, tracking invitation status, and removing access when needed.

## Page structure
Reached via the "Profile" icon at the top right corner of the app, then "Team" in the dropdown menu (menu order: Organisations & Sites / Team / Billing & Invoices / MCP access / Notifications / My account / Logout).

The Team page has a "Team Members" title at the top left and a "+ Invite new user" button at the top right.

Below the title sits an **Account Owner card**, containing:
- The card title with an Account ID badge ("Acc ID: [Account ID]") at the top right
- The Account Owner's email address
- An organisation dropdown showing the default organisation ("[Username]'s organisation" with "Org ID: [Organization ID]" beneath it)

Below the organisation dropdown is the **team member table** with three columns: Email address, Role, and Status.
- The Account Owner's own row shows their email and an "Account Owner" role badge, and never has a "More" (...) option — the Owner's own row can never be managed.
- Every invited Admin or Editor member appears as an additional row with email, role badge (Admin/Editor), and status (Pending or Active). Each such row has a "More" (...) option, except when it is the viewer's own row (self-management is likewise blocked).

If the Account Owner's own email address has not yet been verified, the "+ Invite new user" button is disabled, with a tooltip on hover: "Please verify your email to invite users."

## Workflows

### 1. Invite a new team member
1. Click "+ Invite new user" (top right of the Team page). The "Invite new user" pop-up opens, showing:
   - Text under the title: "The invited user will have access to all sites in the selected organisation"
   - An info banner: "The user will receive an email with instructions to join your team."
   - An "Organisation*" dropdown (placeholder "Select organisation")
   - An "Email address*" field (placeholder "email@address.com")
   - A "Role*" label with a "Learn more" link to its right, opening the roles/permissions documentation (not captured in source data — needs live verification of the exact destination page title)
   - "Admin" role radio button — "Can manage sites, users, and has all Editor permissions"
   - "Editor" role radio button — "Can manage cookie banner, cookie scan, consent settings, and legal policies"
   - "Cancel" and "Invite user" buttons ("Invite user" stays disabled until organisation, email, and role are all set)
2. Select the organisation, enter the invitee's email address, and select a role (Admin or Editor).
3. Click "Invite user".
   - If the email already has access to the selected organisation: a validation error appears under the "Email address*" field — "This user already has access to the selected organisation." No invite is sent.
   - If the email format is invalid (e.g. "not-an-email"): the "Invite user" button stays enabled while typing (no client-side format check), but clicking it shows "Valid email required" under the field, the button becomes disabled again, and no invite is sent.
   - Otherwise, the invited user is added to the team member table with the invited email, the selected role badge, a "Pending" status, and a "More" (...) option.
4. The invitee receives an email titled "You've been invited to join an organization in CookieYes" containing a "Join Organization" button (and a plain-text fallback invitation link).
5. Clicking "Join Organization":
   - **Existing CookieYes user:** lands on the "Join your team now!" login page, with a banner "You've been invited to join [Destination organization name] (Organisation ID: [Destination organization ID])." The invitee's email is pre-filled and disabled. The invitee enters their password (an "Enter password" field with an eye icon) and clicks "Join now", or uses the "Forgot your password?" link.
   - **New (non-existing) user:** lands on the "Join your team now!" sign-up page with the same organisation banner and pre-filled/disabled email. The invitee enters a password in "Create password" and checks "I agree to the Terms and acknowledge the Privacy Policy" (Terms and Privacy Policy are separate links). Checking that box reveals a second, optional, unchecked checkbox: "I agree to receive important product updates, news and insights from CookieYes." Clicking "Join now" does not require the second checkbox.
6. On success, the "You've successfully joined your team!" page is shown, with a success icon, that heading, the text "You can now start collaborating with your teammates", and a "Go to Dashboard" button.
7. Clicking "Go to Dashboard" takes the new member to their own Dashboard page.
8. Back on the inviter's Team page, the member's row status updates from "Pending" to "Active".

This flow is identical for Admin and Editor invitees except for the role badge assigned.

### 2. Change a member's role
1. On the team member table, click the "More" (...) option on the target member's row (the row must be Active; Admin or Editor). A menu opens with "Change role" and "Remove user".
2. Click "Change role". The "Change user role" pop-up opens, showing:
   - A disabled "Organisation*" dropdown, pre-selected to the organisation the member has access to
   - A disabled "Email address*" field, pre-filled with the member's email
   - A "Role*" label with a "Learn more" link
   - "Admin" and "Editor" role radio buttons (same descriptions as the invite pop-up), with the member's current role pre-selected
   - "Cancel" and "Change role" buttons
3. Select the other role radio button (Admin or Editor).
4. Click "Change role". The member's row updates to show the new role badge; the "Active" status and "More" (...) option are unchanged.

### 3. Remove a team member
1. Click the "More" (...) option on an Active member's row, then click "Remove user". The "Remove user?" pop-up opens with the text: "Once removed, [member's email] will no longer be able to access [Organisation_name] (Org ID: [Organisation_id]). This action cannot be undone." and "Cancel"/"Remove" buttons.
2. Click "Remove". The member's row is removed from the team member table immediately.

### 4. Accept an invitation while a different account is already logged in
1. In the invited user's mailbox, obtain the invitation link, and load it in a browser where a different CookieYes account is already logged in.
2. A logout confirmation page is displayed: the "CookieYes" logo, a "Welcome back" title, and "Logged in as [logged in user email address]" (plain text, with the first letter of that email shown as an avatar icon).
3. An info banner reads: "Log out now to accept the invite received at [invitee email address] to join [destination organization name] (Organisation ID: [organization id]) ." (the live app has a stray space before the final period — a known template quirk, not a wording choice). A "Log out to continue" button is shown below.
4. Clicking "Log out to continue" logs out the current session and lands on the "Join your team now!" page for the invited account, continuing workflow 1 from the join step.

## Validation & edge cases
- **Duplicate invite:** inviting an email that already has access to the selected organisation is blocked with "This user already has access to the selected organisation." shown under the Email address field.
- **Invalid email format:** e.g. "not-an-email" is accepted as typed (no client-side check) but rejected on submit with "Valid email required"; "Invite user" is re-disabled and no invite is sent.
- **Unverified Account Owner email:** "+ Invite new user" is disabled account-wide with tooltip "Please verify your email to invite users." until the Owner verifies their own email.
- **Account Owner row is never manageable:** no "More" (...) option ever appears on the Owner's own row.
- **Self-management is blocked:** the viewer's own row (Admin or Editor viewing themselves) never shows a "More" (...) option either.
- **Editor role-restricted variant — cannot invite:** logged in as Editor, "+ Invite new user" is disabled by default (not clickable-then-blocked). Hovering shows the tooltip "Only the Account Owner or an Admin can manage a user." — this is a generic "manage a user" message, not invite-specific wording, and is shared with the More-button tooltip below.
- **Editor role-restricted variant — cannot change role or remove:** logged in as Editor, the "More" (...) option on any other member's row is disabled by default; clicking it shows the same tooltip, "Only the Account Owner or an Admin can manage a user.", and the Change role / Remove user menu does not open.
- **Plan-gated seat limits:** (not captured in source data — needs live verification). None of the 17 cases assert a maximum team size or plan-based seat cap; treat any such limit as unconfirmed until checked live.
- Destructive action ("Remove user?") always requires confirmation via the pop-up before the row disappears — no undo after confirming.

## Related pages
- docs/wiki/10-profile-account/organisations-and-sites/site-transfer.md — ownership/role interactions when transferring site or organisation ownership
- docs/wiki/14-permissions.md — app-wide role/permission hierarchy (Account Owner / Admin / Editor)

## Source
Derived from `ai-context/cases-team.json` (17 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
