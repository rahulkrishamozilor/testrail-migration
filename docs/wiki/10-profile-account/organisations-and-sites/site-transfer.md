# Organisations & Sites — Site Transfer

**Nav path:** Profile & Account > Organisations & Sites > Site Transfer
**Route:** Initiated from `/settings/organizations-and-sites` (a website's More (⋯) menu). The
recipient-side routes (logout confirmation page, site-transfer Log In page, "Website transfer
request" page) are not captured in source data — needs live verification.
**Roles:** **Account Owner only** — Admin and Editor are both blocked: the "Transfer Site" option
is disabled in a website's More (⋯) menu with tooltip "Only the Account Owner can transfer a
site." for either role. See `docs/wiki/14-permissions.md` for the app-wide role hierarchy.
**Plan gating:** None captured in source data for this sub-topic.

## Purpose
Site Transfer covers moving ownership of a website from one organisation to another — either
instantly within the same account, or via an email-based request/accept/reject flow when the
destination organisation belongs to a different account, subject to a 7-day expiry.

## Page structure
- **Transfer Site entry point** — a "Transfer Site" option in a website's More (⋯) menu on the
  Organisations & Sites page. Once a cross-account transfer request is outstanding for that site,
  this option is replaced by **"Cancel transfer request"**.
- **"Transfer site to another organisation" modal** — opened via "Transfer Site". Contains:
  - A disabled "Site URL" field showing the site being transferred.
  - A disabled "Current organisation" field showing the source organisation name + Org ID.
  - A "Destination organisation*" dropdown.
  - Cancel and "Transfer site" buttons — "Transfer site" is disabled until a destination is
    selected.
- **Destination organisation dropdown states:**
  - No other organisations available: shows a "No organizations found" (observed live as "No
    organisations found!") option that cannot be selected.
  - An organisation owned by the **same account** is selected: an info banner reads "The site
    will be immediately transferred to the destination organization as it is owned by you. Once
    the site is successfully transferred, users in the current organization will lose access, and
    users in the destination organization will gain access to the site."
  - An organisation owned by **another account** is selected: an info banner reads "The owner of
    the destination organization will receive an email with instructions to accept the transfer
    request. Once the site is successfully transferred, users in the current organization will
    lose access, and users in the destination organization will gain access to the site."
  - Important: an organisation owned by a different ("recipient") account only becomes selectable
    as a cross-account destination after the sender has been added as a team member of that
    organisation — it is not simply any organisation that exists on the platform (see Workflow 5).
- **"Transfer request initiated" indicator** — once a cross-account request is sent, this text
  with a tooltip appears under the site's URL on its row.
- **"Cancel site transfer request?" modal** — opened via "Cancel transfer request" in the More
  (⋯) menu once a request is outstanding.
- **Recipient-side pages/emails:**
  - Email "You've received a site transfer request in CookieYes" with a "Review Transfer Request"
    button/link.
  - Logout confirmation page (shown if the recipient's browser is logged in as a different user).
  - Site-transfer Log In page, with the invitee's email pre-filled and disabled.
  - "Website transfer request" page, with Accept and Reject buttons.
  - Post-transfer, if the transferred site has no payment method: "No payment method available
    for this site." text with an "Add payment method" link and help icon on the site's row.

## Workflows

**1. Opening the Transfer Site modal and reading the destination dropdown states**
1. Open a website's More (⋯) menu and select "Transfer Site".
2. Result: the "Transfer site to another organisation" modal opens (Site URL and Current
   organisation fields disabled, Destination organisation* dropdown, Transfer site disabled).
3. Open the Destination organisation dropdown with no other organisations available.
4. Result: shows "No organizations found" (unselectable).
5. With another organisation on the same account available, select it.
6. Result: the immediate-transfer info banner is shown (quoted above).
7. Select a destination organisation belonging to another account instead.
8. Result: the email-request info banner is shown (quoted above).

**2. Cancelling out of the Transfer Site modal**
1. Open "Transfer Site" and click "Cancel".
2. Result: the modal closes with no transfer initiated.

**3. Blocked transfer with no destination selected**
1. Open "Transfer Site" and open the Destination organisation dropdown without selecting anything.
2. Result: "Transfer site" remains disabled/non-actionable, so the transfer cannot proceed.

**4. Transferring a site within the same account (instant)**
1. Open "Transfer Site" and select a destination organisation owned by the same account.
2. Result: the immediate-transfer info banner is shown.
3. Click "Transfer site".
4. Result: the site transfers immediately, and a toast confirms: "[Site URL] has been
   successfully transferred to [organization name] (Org ID: [organization id])."

**5. Setting up and initiating a cross-account transfer request**
An organisation owned by a different account only appears in the Destination organisation
dropdown after the sender has been made a team member of that organisation. To reach that state:
1. As the recipient account owner, upgrade to Basic or higher if not already on a paid plan (team
   invites appear to require a paid plan).
2. As the recipient, go to Profile menu > Teams > "Invite new user".
3. Select the recipient's organisation from the "Organization" dropdown.
4. Enter the sender account owner's email in "Email address*".
5. Select the "Admin" (or "Editor") radio button under "Role".
6. Click "Invite user" — an invite email is sent to the sender.
7. As the sender, open the "You've been invited to join an organization in CookieYes" email,
   click "Join Organization", enter a password, and click "Join now" to accept.

Only after this does the recipient's organisation appear in the sender's Destination organisation
dropdown, labelled as belonging to another account.

8. As the sender, open the website's More (⋯) menu, select "Transfer Site", and select the
   recipient's organisation as the destination.
9. Click "Transfer site".
10. Result: the destination owner receives the transfer-request email, and a toast confirms "The
    site transfer request has been successfully sent to [email]." The website row now shows
    "Transfer request initiated" under the Site URL (tooltip: "A request has been initiated to
    transfer this site to [organization name] (Org ID: [organization id]). The site will remain
    in the current organization until the request is accepted by the owner of the destination
    organization, before it expires on [Month mm, yyyy]."), and the site's More (⋯) menu now shows
    "Cancel transfer request" in place of "Transfer Site".

**6. Cancelling an outstanding transfer request**
1. With a transfer request outstanding (per Workflow 5), open the website's More (⋯) menu and
   select "Cancel transfer request".
2. Result: the "Cancel site transfer request?" modal opens with the message "The transfer request
   initiated for [URL] will be cancelled immediately and the site will remain in the current
   organization." and Cancel / "Cancel transfer request" buttons.
3. Click "Cancel" in the modal.
4. Result: the modal closes and the transfer request remains active.
5. Reopen the modal and click "Cancel transfer request".
6. Result: the request is cancelled, the "Transfer request initiated" indicator disappears from
   the Site URL, and the More (⋯) menu shows "Transfer site" again.

**7. Destination owner receiving the transfer-request email**
1. Initiate a cross-account transfer request (Workflow 5).
2. Result: a toast confirms the request was sent to the destination owner's email.
3. Open the destination owner's inbox and load the "You've received a site transfer request in
   CookieYes" email.
4. Result: the email shows the CookieYes logo, body text "Hi there, [user email] has requested to
   transfer the site [Site URL] from their organization to your organization in CookieYes. Please
   review the request and take action before it expires on [Month dd, yyyy].", a "Review Transfer
   Request" button/link (with a note that the link can be copied and pasted into the browser),
   and sign-off "Best Regards, The CookieYes Team".

**8. Recipient clicks Review Transfer Request while logged in as someone else**
1. With a cross-account request outstanding and the recipient's browser currently logged in as
   some other user (not yet the recipient), open the request email and click "Review Transfer
   Request".
2. Result: a logout confirmation page is shown: "Logged in as [logged in user email address]"
   (avatar = first letter of that email), an info banner "Log out now to accept the site transfer
   request received at [invitee email].", and a "Log out to continue" button.
3. Click "Log out to continue".
4. Result: the site-transfer Log In page is displayed, with an "Email address" field pre-filled
   with the invitee's email and disabled, a Password field, a "Log In" button, and a "Forgot your
   password?" link.

**9. Recipient logs in and reaches the Website transfer request page**
1. On the site-transfer Log In page (per Workflow 8), enter a valid password and click "Log In".
2. Result: the "Website transfer request" page is displayed.

**10. Accepting a transfer request**
1. On the "Website transfer request" page, click "Accept".
2. Result: the website transfer success page is displayed and the site moves to the recipient's
   organisation.
3. Check the sender's email inbox.
4. Result: an email with subject "Your site has been transferred to another organization in
   CookieYes" is received, body: "[email] has accepted your request to transfer the site
   [site_url] from [current_org_name] to [destination_org_name]."

**11. Rejecting a transfer request**
1. On the "Website transfer request" page, click "Reject".
2. Result: a transfer-request-rejected page is displayed and the site remains in the sender's
   organisation.
3. Check the sender's email inbox.
4. Result: an email with subject "Your site transfer request to another organisation in CookieYes
   has been rejected" is received, body: "[email] has rejected your request to transfer the site
   [site_url] from [current_org_name] to [destination_org_name]."

**12. Missing payment method after an accepted transfer**
1. Accept a transfer request (Workflow 10) which routes to a Stripe payment page for the newly
   transferred site.
2. Click "Back" on the Stripe payment page instead of completing payment.
3. Result: the Organisations & Sites page is displayed with the newly transferred site listed.
4. Observe the transferred site's row.
5. Result: shows "No payment method available for this site." with an "Add payment method" link
   and a help icon; hovering the help icon shows the tooltip "If you do not add a payment method
   before the next renewal date, Month DD, YYYY, the site will be suspended and permanently
   deleted within 30 days of suspension."
6. Click "Add payment method".
7. Result: the Stripe payment page is displayed.

## Validation & edge cases
- **7-day expiry:** a cross-account transfer request expires 7 days after it is initiated. The
  "Transfer request initiated" tooltip states the exact expiry date. Attempting to reach the
  "Website transfer request" page and Accept **after** the 7-day expiry: the page reflects that
  the request has expired, so the transfer can no longer be completed via Accept.
- **Suspension after transfer with no payment method:** if a transferred site still has no
  payment method by its next renewal date, the site is put into **Suspended** status. (Requires
  setting `subscription_renew_at` to a past date and running the
  `payment-method-not-added-transfer-site` scheduled task to reproduce; a page refresh is needed
  to see the Suspended status after the task runs.)
- **Shopify-connected site block:** a site created via the CookieYes Shopify app installation
  cannot be transferred to another account's organisation. Attempting it shows the error "This
  site can only be transferred to an organization you own, as it is connected to your account via
  CookieYes' Shopify app.", and the site is not transferred. (Same-account transfers for a
  Shopify-connected site are not addressed by this case.)
- **Cross-account destination visibility:** an organisation belonging to another account will
  never appear in the Destination organisation dropdown unless the sender has first been invited
  into and joined that organisation as a team member (Admin or Editor role) — see Workflow 5.
  There is no other path to make a cross-account organisation selectable.
- **Role-restricted — Admin and Editor cannot transfer a site:** "Transfer site" is disabled in
  the More (⋯) menu with tooltip "Only the Account Owner can transfer a site." for both roles.

## Related pages
- [Organisation Management](organisation-management.md)
- [Site Management](site-management.md)
- [Team](../team.md)
- [Paid Plan](../../11-billing-upgrade/paid-plan.md)
- [Permissions](../../14-permissions.md)

## Source
Derived from `ai-context/cases-organisation-and-sites.json` (66 TestRail cases total, split by
sub-topic — 16 of those cases feed this file). Drafted 2026-07-14, not yet live-verified against
the QA app beyond what is already noted from the source cases' own grill passes (several
cross-account transfer cases were manually approved by the user on review rather than executed
live in-session).
