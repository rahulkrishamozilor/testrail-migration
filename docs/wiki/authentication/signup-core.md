# Sign Up — Core (shared form validation & email verification)

**Nav path:** 01. Authentication > Sign Up > Core
**Route:** (not captured in source data — needs live verification)
**Roles:** N/A — pre-account (signup happens before any Editor/Admin/Account Owner role exists)
**Plan gating:** N/A — the signup form and its field validation are identical regardless of which
plan the user ends up on after signup. Plan-specific post-signup behavior (Standard/Free, Trial
without card, Trial with card/Checkout, Agency) is documented in the sibling pages linked below,
not here.

## Purpose
This page documents the Sign Up form's field validation rules and the email verification flow
that follow it. These behaviors are shared across every Sign Up page variant (Standard/Free,
Trial without card, Trial with card/Checkout, Agency) — rather than repeating them on each
variant's page, they are documented once here and referenced from those pages.

## Page structure
The Sign Up page presents a form with the following elements:

- **Email field** — text input for the user's email address.
- **Website field** — text input for the user's website URL, expected in `example.com` format
  (i.e. without a scheme/protocol prefix).
- **Password field** — text input for the account password.
- **Terms and Conditions checkbox** — an acceptance checkbox whose label contains two inline
  links: a **"Terms and Conditions"** link and a **"Privacy Policy"** link, each opening the
  corresponding CookieYes legal page.
- **"Get Started" button** — submits the form.

Exact field order, placeholder text, and layout are not captured in the source data — needs live
verification.

After a successful signup, the user is sent an email titled **"Verify your email for CookieYes"**
containing a **"Verify Email"** button. Depending on when/whether that link is clicked, the user
lands on one of:

- The **email verification success page**, which has a **"Go to Dashboard"** button.
- The **"Your email verification failed!"** page, which has a **"Resend Verification Email"**
  button. This page appears both when the link has expired (not clicked within 1 hour of signup)
  and when the associated account was deleted before verification.

## Workflows

1. **Submit the signup form**
   1. Enter a value in the Email field, the Website field, and the Password field.
   2. Check the Terms and Conditions checkbox.
   3. Click **"Get Started"**.
   - What happens next (which page the user lands on, what plan they start on) is plan-variant
     specific and is documented on the relevant variant page (see Related pages below), not here.
     This Core page only covers the field-level validation shown when submission is invalid (see
     Validation & edge cases) and the email verification flow that follows a valid submission.

2. **Verify email after signup**
   1. Open the **"Verify your email for CookieYes"** email in the inbox.
   2. Click the **"Verify Email"** button in the email.
   3. Result: the **email verification success page** is displayed.
   4. Click **"Go to Dashboard"**.
   5. Result: the **Dashboard** page is displayed.

3. **Resend verification email after link expiry**
   1. Precondition: signup was completed but the email was not verified within 1 hour; the
      original **"Verify your email for CookieYes"** email is still in the inbox.
   2. Open that email (more than 1 hour after signup) and click **"Verify Email"**.
   3. Result: the **"Your email verification failed!"** page is displayed.
   4. Click **"Resend Verification Email"**.
   5. Result: a new verification email is received, and a **"Verification email has been resent
      successfully."** notification appears.

4. **Resend verification email after the account was deleted**
   1. Precondition: signup was completed, but the account was deleted before the email was
      verified; the original **"Verify your email for CookieYes"** email is still in the inbox.
   2. Open that email and click **"Verify Email"**.
   3. Result: the **"Your email verification failed!"** page is displayed, with a **"Resend
      Verification Email"** button.
   4. Click **"Resend Verification Email"**.
   5. Result: a new verification email is received and a success notification appears. Source
      cases disagree on the exact wording/behavior here (flagged as C70 vs. C1148 in the source
      data) — treat this specific sub-case as needing manual/live verification before relying on
      it, even though the general expired-link resend flow (workflow 3) is not in question.

5. **Open legal links from the signup form**
   1. Click the **"Terms and Conditions"** link in the acceptance checkbox label.
   2. Result: the CookieYes Terms and Conditions page is displayed.
   3. Click the **"Privacy Policy"** link in the acceptance checkbox label (separately from step 1).
   4. Result: the CookieYes Privacy Policy page is displayed.

## Validation & edge cases

All of the following are triggered by filling the form as described, leaving the noted field(s)
in the invalid state, and clicking **"Get Started"**:

| Field | Invalid condition | Exact error message |
|---|---|---|
| Email | Left empty | "Email is required" |
| Email | Already registered to an existing account | "The email has already been taken." |
| Email | Invalid format (e.g. "notanemail") | "Valid email required" |
| Email | Exceeds 190 characters | "Your email address exceeds the maximum value of 190 characters" |
| Website | Left empty | "Website is required" |
| Website | Not in `example.com` format | "Please enter URL in the format example.com" |
| Website | Exceeds 75 characters | "URL should be less than 75 characters" |
| Password | Left empty | "Password is required" |
| Password | Fewer than 8 characters | "Minimum 8 characters required" (displayed directly below the password field) |
| Password | Exceeds 64 characters | "The password is too long" |
| Terms and Conditions | Checkbox left unchecked | "Please agree to terms and conditions to proceed" |

Boundary values called out by the source cases: password length boundaries are 8 (minimum,
inclusive — below this is invalid) and 64 (maximum, inclusive — above this is invalid); email
length boundary is 190 characters (above this is invalid); website URL length boundary is 75
characters (above this is invalid).

Email verification edge cases:
- **Expired link** (>1 hour after signup, not yet verified): lands on "Your email verification
  failed!" with a working "Resend Verification Email" button that successfully sends a new email.
- **Deleted account**: clicking the original verification link after the account was deleted
  before verification also lands on "Your email verification failed!" with a "Resend Verification
  Email" button — but see workflow 4 above regarding a source-data disagreement on the resend
  outcome in this specific scenario.

## Related pages
- [Sign Up — Standard (Free)](./signup-standard-free.md)
- [Log In](./login.md)
- [Password Reset](./password-reset.md)

This page underlies all Sign Up variants (Standard/Free, Trial without card, Trial with card /
Checkout, Agency) — their pages cover what happens after a valid submission and should be read
together with this one rather than repeating its validation rules.

## Source
Derived from `ai-context/cases-signup-core.json` (17 TestRail cases). Drafted 2026-07-14, not yet
live-verified against the QA app.
