# My Account

**Nav path:** Profile & Account > My account (reached via the Profile icon menu, top right of the
Dashboard: Organisations & Sites / Team / Billing & Invoices / MCP access / Notifications /
My account / Logout)
**Route:** `/settings/account`
**Roles:** (not captured in source data — every case exercises the logged-in user's own account
settings; whether Admin/Editor team members see an equivalent page for their own account is not
separately confirmed, though there is no indication it would differ)
**Plan gating:** (not captured in source data — no case asserts a plan-gated control on this page)

## Purpose

My Account is a dedicated settings page (not a modal) where a user manages their own account:
updating their registered email, changing their password, setting up or removing two-factor
authentication (2FA), managing email notification preferences, and deleting their account.

## Page structure

The page has its own left-hand navigation, separate from the Dashboard. Four sections, top to
bottom:

- **Account details** — the registered email address, shown read-only in a disabled field, with a
  "Change email" button.
- **Email notifications** — introductory text ("Choose the type of emails you'd like to receive
  from us.") and a "Manage email preferences" button, leading to a separate preferences page.
- **Security** — a "Change password" button, and either a "Set up 2FA" button (if 2FA is not yet
  enabled) or "Disable 2FA" and "Re-generate recovery codes" buttons (if it is). If the account's
  registered email has not yet been verified, "Set up 2FA" is disabled with a tooltip: "Please
  verify your email address to set up 2FA."
- **Account deletion** — explanatory text ("Once you delete your account, all your data will be
  lost forever") and a "Delete account" button.

## Workflows

### 1. Update the registered email

1. Click the edit icon next to the registered email field. The "Update your email address" modal
   opens with "New email address", "Confirm email address", and "Current password" fields, an
   alert ("A verification code will be sent to the new email address"), and "Cancel"/"Update
   email" buttons.
2. Enter a new email address, repeat it in "Confirm email address", and enter the current
   password, then click "Update email". The modal closes and an "Enter verification code" pop-up
   opens: six digit fields, a "Resend Code" button, and "Cancel"/"Confirm Code" buttons (the
   latter disabled by default).
3. The new address receives an email titled "Verify your new email for CookieYes" containing a
   6-digit code that expires in 10 minutes.
4. Entering the code and clicking "Confirm Code" shows a "Your email has been changed!" pop-up,
   stating the user will be logged out and must log back in with the new address. Clicking
   "Okay" logs the user out to the Log In page; logging in with the new email and the existing
   password reaches the Dashboard, and My Account now shows the new address.
5. Clicking "Resend Code" sends a new code and replaces the button with a "Resend code in [N]
   seconds" countdown; the button reappears once the countdown finishes.
6. Clicking "Cancel" on the verification pop-up closes it without changing the email.

### 2. Change password

1. Click "Change password". The "Change password" modal opens with "Old password", "New
   password", and "Confirm password" fields and "Cancel"/"Change password" buttons.
2. Enter the current password, a new password meeting complexity requirements, and repeat it in
   "Confirm password", then click "Change password". A "Your password has been changed! You'll
   now be logged out automatically. Please log in with your new password to continue using
   CookieYes." dialog is shown; the app then logs the user out and redirects to the Log In page
   (briefly blank in transition — expected during this step, not a defect). Logging back in with
   the new password reaches the Dashboard, confirming the change took effect.
3. Clicking "Cancel" closes the modal and discards entered values.

### 3. Set up two-factor authentication (2FA)

1. Click "Set up 2FA" (only enabled once the registered email is verified). The "Set up
   two-factor authentication (2FA)" modal opens with a QR code, a manual setup key (with a copy
   icon), a verification code field, and "Cancel"/"Verify code" buttons.
2. Add the setup key to an authenticator app, enter the resulting code, and click "Verify code".
   A "2FA has been set up successfully on your account!" pop-up opens with a table of 12
   ten-digit recovery codes, a "Copy" button, an "I've securely saved my 2FA recovery codes."
   checkbox, and an "Okay" button (disabled until the checkbox is checked).
3. After confirming, the Security section shows "Disable 2FA" and "Re-generate recovery codes" in
   place of "Set up 2FA".

### 4. Disable 2FA

1. Click "Disable 2FA". The "Disable two-factor authentication (2FA)?" modal opens with a warning
   that 2FA will need to be set up again in future, a password field, and "Cancel"/"Disable 2FA"
   buttons.
2. Entering the correct password and confirming removes the "Disable 2FA"/"Re-generate recovery
   codes" buttons and restores "Set up 2FA".
3. Clicking "Cancel" closes the modal and leaves 2FA enabled.

### 5. Re-generate 2FA recovery codes

1. Click "Re-generate recovery codes". A modal opens with a warning and a password field,
   requiring the correct password before "Re-generate recovery codes" is enabled.
2. Confirming displays a new table of 12 ten-digit recovery codes with a "Copy" button; the
   "I've securely saved my 2FA recovery codes." checkbox must be checked before "Okay" closes the
   modal.

### 6. Delete account

1. Click "Delete Account" in the Account deletion section. The "Delete account?" modal opens: an
   explanation that deletion is permanent, a warning that the user will need to sign up again to
   use CookieYes in future, a required "I understand and want to delete my account including all
   its data." checkbox, and "Cancel"/"Delete Account" buttons — the latter disabled until the
   checkbox is checked.
2. The modal's "contact us" link opens an external CookieYes support page.
3. Confirming the checkbox enables "Delete Account". Clicking it deletes the account immediately
   — no further confirmation step — and redirects to the Log In page; the deleted account's email
   and password no longer authenticate ("Invalid email/password. Please try again").

### 7. Manage email preferences

1. Click "Manage email preferences" in the Email notifications section. The "Manage your email
   preferences" page opens (route `/settings/manage-preferences`), showing the registered email
   and a note that preference changes do not affect transactional account emails (invoices, scan
   reports).
2. Three independently checkable categories are listed: Product Updates, Marketing, and
   Newsletters, each with its own description. "Save preferences" is disabled until a category is
   toggled.
3. Checking a category and clicking "Save preferences" shows a "Your preferences are saved!"
   toaster; the button becomes disabled again, and the change persists across a reload.
4. "Close preferences" returns to the My Account page.

This page has a second variant reached without the account-settings entry point (its exact
trigger is not yet confirmed — see Known gaps): different intro copy ("Transactional emails, such
as invoices and scan reports, cannot be unsubscribed from." instead of the note above) plus an
additional "Unsubscribe from all emails" button.

## Validation & edge cases

- **Email update — empty fields:** leaving New email/Confirm email/Current password empty shows
  "New email is required", "Confirm Email is required", and "Current Password is required" under
  each field.
- **Email update — invalid format:** an invalid new email address shows "Valid email required"
  under the field (distinct from the empty-field message above).
- **Email update — mismatch:** differing New email/Confirm email values show "New email and
  Confirm email does not match" under Confirm email.
- **Email update — wrong current password:** shows "Invalid password. Please try again" as a
  form-level message (not anchored to the password field).
- **Email update — address already registered:** shows "The new email has already been taken." as
  a form-level message.
- **Verification code — invalid:** shows "Invalid verification code. Please check your email for
  the correct code."
- **Verification code — expired** (more than 10 minutes old): shows "The verification code has
  expired. Please resend code and try again." Confirmed live.
- **Password change — empty fields:** shows "Old password is required", "New password is
  required", and "Confirm password is required".
- **Password change — wrong old password:** shows "Invalid password. Please try again" as a
  form-level message.
- **Password change — complexity:** a new password failing complexity rules shows "Include both
  lowercase and uppercase characters, at least one number, and a special character such as
  ! @ # $ % ^" under New password.
- **Password change — mismatch:** shows "New Password and Confirm Password does not match" under
  New password.
- **2FA setup — invalid code:** shows "Invalid authentication code" under the code field.
- **2FA disable / recovery-code regeneration — wrong password:** both show "Invalid password".

## Known gaps

- **The full email-update happy path** (receiving the verification code in a real inbox,
  confirming it, logging back in with the new address) still has not been exercised end-to-end
  live. The expired-code path was confirmed instead (see Validation & edge cases); every
  individual step around the happy path (modal fields, validation errors, duplicate-email
  detection) was independently confirmed.
- **Disabling 2FA's confirmation toaster text** was not captured in time to confirm its exact
  wording; the resulting button-state change was confirmed.
- **The Manage Email Preferences page's second variant** (different intro copy, plus an
  "Unsubscribe from all emails" button — see Workflow 7) was found by accident; its actual trigger
  (a URL parameter, an unauthenticated/emailed-link context, or something else) is not yet
  identified.

Resolved this pass, previously listed here: account deletion's final action (confirmed — deletes
immediately, deleted credentials correctly stop authenticating), "Save preferences" (confirmed —
"Your preferences are saved!" toaster, persists after reload), the 2FA setup button's "verify
your email first" tooltip (confirmed verbatim against a freshly signed-up, unverified account),
and the Change password flow's post-submit feedback (confirmed — see Workflow 2; the brief blank
transition before the auto-logout redirect is expected, not a defect).

## Related pages

- `docs/wiki/profile-account/team.md` — a separate settings surface for managing other team
  members, as opposed to this page's own-account scope
- `docs/wiki/permissions.md` — app-wide role hierarchy

## Source

Derived from `cases-my-account.json` (28 cases; fetched, grilled, and published 2026-07-07 to
2026-07-09). Two cases (the "Email notifications" section itself, and the duplicate-email
validation error) were newly authored from live findings with no Suite 6 precedent. Drafted
2026-07-23 via `/wiki-sync`; spot-checked live the same day (password change, save preferences,
expired verification code, account deletion, unverified-email 2FA tooltip) — see Known gaps for
the one unresolved finding from that pass.
