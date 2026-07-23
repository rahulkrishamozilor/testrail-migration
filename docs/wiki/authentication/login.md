# Log In

**Nav path:** Authentication > Log In
**Route:** (not captured in source data — needs live verification)
**Roles:** N/A
**Plan gating:** N/A

## Purpose
The Log In page authenticates a user with an email address and password and, on success, redirects
them to the Dashboard. It also serves as the entry point to two other authentication flows: creating
a new account (Sign Up) and recovering access to an existing one (Forgot Password).

## Page structure
The Login page presents a simple credentials form with the following elements:

- **Email address field** — a required text input for the account email.
- **Password field** — a required input for the account password. Characters are masked (displayed
  as dots) by default.
- **Show/hide toggle (eye icon)** — sits on the Password field. Clicking it reveals the entered
  password in plain text; clicking it again re-masks it.
- **"Log In" button** — submits the form with the entered email and password.
- **"Forgot your password?" link** — navigates away from the Login page to the Forgot Password page.
- **"Sign Up" link** — navigates away from the Login page to the Sign Up page.

## Workflows

**1. Successful login**
1. Start on the Login page with a registered account already existing.
2. Enter valid credentials into the Email address and Password fields.
3. Click "Log In".
4. Result: the Dashboard page is displayed.

**2. Viewing the entered password**
1. On the Login page, enter a password into the Password field (it appears masked, as dots).
2. Click the eye icon on the Password field.
3. Result: the entered password is displayed in plain text. Clicking the eye icon again re-masks it.

**3. Navigating to Sign Up**
1. On the Login page, click the "Sign Up" link.
2. Result: the Sign Up page is displayed.

**4. Navigating to Forgot Password**
1. On the Login page, click the "Forgot your password?" link.
2. Result: the Forgot Password page is displayed.

## Validation & edge cases

- **Empty email field:** Leave the Email address field empty (Password filled), click "Log In" →
  error message: **"Email is required"**.
- **Invalid email format:** Enter a malformed email address, fill in Password, click "Log In" →
  error message: **"Valid email required"**.
- **Empty password field:** Leave the Password field empty (Email filled), click "Log In" →
  error message: **"Password is required"**.
- **Non-existing email:** Enter an email with no registered account, plus any password, click
  "Log In" → error message: **"Invalid email/password. Please try again"**.
- **Incorrect password:** Enter a registered email address with an incorrect password, click
  "Log In" → error message: **"Invalid email/password. Please try again"** (same message as the
  non-existing-email case — the app does not distinguish between "unknown email" and "wrong
  password" in its error text).
- **Field/control presence:** Email address and Password fields are both marked as mandatory in
  the UI; the eye icon toggle, "Log In" button, "Forgot your password?" link, and "Sign Up" link
  are all expected to be visible and interactive on page load.

## Related pages
- [Forgot Password / Reset Password](password-reset.md)
- [Sign Up](signup-core.md)

## Source
Derived from `ai-context/cases-login.json` (10 TestRail cases). Drafted 2026-07-14, not yet live-verified against the QA app.
