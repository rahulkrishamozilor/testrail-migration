# Password Reset

**Nav path:** Authentication > Password Reset (entered via "Forgot your password?" link on Log In)
**Route:** (not captured in source data — needs live verification)
**Roles:** N/A
**Plan gating:** N/A

## Purpose
The Password Reset flow lets a user with a registered email address regain access to their
account by requesting a reset link via email and using it to set a new password. It spans five
screens: the Forgot Password request form, a check-inbox confirmation page, the emailed reset
link, the Reset Password form, and a final reset-confirmation success page.

## Page structure

**1. Forgot Password page** (reached via "Forgot your password?" on Log In)
- **Email address field** — required text input for the account email.
- **"Submit" button** — submits the email address to request a reset link.
- **"Back to Login" link** — navigates back to the Log In page.

**2. Check-inbox confirmation page** (shown after submitting a valid email)
- A confirmation message indicating the reset email has been sent (exact copy not captured in
  source data — needs live verification).
- **"Back to Login" link** — navigates back to the Log In page.

**3. Reset-link email** ("Password Reset Request" email, sent to the submitted address)
- Contains a **"Reset Password" button** which, when clicked, opens the Reset Password page.

**4. Reset Password page** (reached by clicking "Reset Password" in the email)
- **Email address field** — required text input; must match the email the reset was requested
  for.
- **New password field** — required text input for the new password.
- **Confirm password field** — required text input; must match the New password field.
- **"Reset Password" button** — submits the form to complete the reset.

**5. Reset confirmation page** (shown after a successful reset)
- A success indicator — a green tick icon confirming the password was reset.
- **"Log In" button** — navigates to the Log In page.
- A "Your password has been changed" notification email is sent to the registered address at
  this point.

## Workflows

**1. Requesting a reset link (successful request)**
1. Start on the Forgot Password page.
2. Enter a valid, registered email address into the Email address field.
3. Click "Submit".
4. Result: the check-inbox confirmation page is displayed.
5. Result: a "Password Reset Request" email is received at the registered email address.

**2. Opening the reset link from email**
1. With a "Password Reset Request" email received (per Workflow 1), open the email in the inbox.
2. Click the "Reset Password" button in the email.
3. Result: the Reset Password page is displayed.

**3. Successful password reset**
1. On the Reset Password page, enter the registered email address.
2. Enter a valid password (8–64 characters) in both the New password and Confirm password
   fields, ensuring they match.
3. Click "Reset Password".
4. Result: the reset confirmation page is displayed with a success indicator (green tick) and a
   "Log In" button.
5. Result: a "Your password has been changed" notification email is received at the registered
   address.

**4. Returning to Log In from the Forgot Password page**
1. On the Forgot Password page, click "Back to Login".
2. Result: the Log In page is displayed.

**5. Returning to Log In from the check-inbox confirmation page**
1. On the check-inbox confirmation page, click "Back to Login".
2. Result: the Log In page is displayed.

**6. Returning to Log In from the reset confirmation page**
1. On the reset confirmation page, click "Log In".
2. Result: the Log In page is displayed.

## Validation & edge cases

**Forgot Password page**
- **Empty email field:** Click "Submit" without entering an email address → error message:
  **"Email is required"**.
- **Invalid email format:** Enter a malformed email address, click "Submit" → error message:
  **"Valid email required"**.
- **Field/control presence:** Email address field is marked mandatory; "Submit" and "Back to
  Login" are both visible and interactive on page load.

**Reset Password page**
- **Empty email field:** Fill New password and Confirm password, leave Email empty, click "Reset
  Password" → error message: **"Email is required"**.
- **Invalid email format:** Enter a malformed email, matching new/confirm passwords, click "Reset
  Password" → error message: **"Valid email required"**.
- **Mismatched email (does not match the reset request):** Enter an email address different from
  the one the reset was requested for, matching new/confirm passwords, click "Reset Password" →
  error message: **"This password reset token is invalid."**
- **Empty new password field:** Fill Email and Confirm password, leave New password empty, click
  "Reset Password" → error message: **"New Password is required"**.
- **Empty confirm password field:** Fill Email and New password, leave Confirm password empty,
  click "Reset Password" → error message: **"Confirm Password is required"**.
- **Password too short (< 8 characters):** Enter registered email, matching new/confirm
  passwords under 8 characters, click "Reset Password" → error message: **"Minimum 8 characters
  required"** (inferred — verify before automation).
- **Password too long (> 64 characters):** Enter registered email, matching new/confirm passwords
  over 64 characters, click "Reset Password" → error message: **"The password is too long"**.
- **Mismatched new/confirm passwords:** Enter registered email, different values in New password
  and Confirm password, click "Reset Password" → error message: **"New Password and Confirm
  Password does not match"**.
- **Expired reset token (> 1 hour old):** Using a "Password Reset Request" email sent more than 1
  hour earlier, open the reset link, enter the registered email and matching new/confirm
  passwords, click "Reset Password" → error message: **"This password reset token is invalid."**
  (displayed below the Confirm password field). Note this is the same message shown for a
  mismatched email — the app does not appear to distinguish an expired token from a
  wrong-email token in its error text.
- **Field/control presence:** Email address, New password, and Confirm password fields are all
  marked mandatory; the "Reset Password" button is visible and interactive on page load.
- **Valid password bounds:** 8–64 characters is the accepted range for New password / Confirm
  password.

## Related pages
- [Log In](login.md)

## Source
Derived from `ai-context/cases-forgot-password.json` (21 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
