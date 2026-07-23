# Sign Up — Standard (Free)

**Nav path:** Sign Up > Standard (Free)
**Route:** (not captured in source data — needs live verification)
**Roles:** N/A — pre-account / first Account Owner created here
**Plan gating:** N/A — this IS the free-plan entry point

## Purpose
The Standard (Free) signup flow is the entry point for creating a new CookieYes account on the
free plan. Completing it creates the account (with the submitting user as the first Account
Owner) and sends the user into onboarding — with no payment/card-collection step anywhere in the
flow. This is what distinguishes it from its sibling flows in the same section (`Trial without
card`, `Trial with card (Checkout)`, `Agency`), per the section outline in
`testrail-suite-v2.md`; the source cases for this page contain no billing or card fields at all.

## Page structure
The Sign Up page (Standard/Free variant) presents:

- **Email address** field — required.
- **Website** field — required.
- **Password** field — required; includes a show/hide toggle (eye icon).
- **"I accept the Terms and Conditions & Privacy Policy"** checkbox — unchecked by default.
- **"Get Started"** button.
- **"Log In"** link.

(Not captured in source data — needs live verification: field placeholder text, inline help
text, logo/branding elements, or any marketing copy on the page.)

## Workflows

### 1. Complete signup with valid credentials
1. User is on the Sign Up page.
2. Enter a valid email address, website URL, and password into the corresponding fields.
3. Check the "I accept the Terms and Conditions & Privacy Policy" checkbox.
4. Click **Get Started**.
5. Result: the onboarding / banner setup page is displayed (see
   `docs/wiki/02-onboarding/banner-setup.md` — not yet written).
6. Result: a verification email with the exact subject **"Verify your email for CookieYes"** is
   sent to the registered email address.

(Not captured in source data — needs live verification: the exact destination route/URL for step
5; whether the account or the associated site record is created before or after email
verification; what happens if the user closes the tab before verifying.)

### 2. Navigate to Log In from the signup page
1. User is on the Sign Up page.
2. Click the **Log In** link.
3. Result: the Login page is displayed.

## Validation & edge cases
Field-level validation (invalid email format, weak/short password, required-field errors,
duplicate-email handling) and the general email-verification mechanics are shared across all
signup variants and are documented in `signup-core.md`, not here.

Specific to this flow:
- No payment or card-entry step appears anywhere in the 3 source cases — consistent with this
  being the free-plan path (contrast with `Trial with card (Checkout)`).
- The checkbox is unchecked by default and must apparently be checked as part of the happy path,
  but the source cases do not test submitting with it unchecked. (Not captured in source data —
  needs live verification: whether "Get Started" is disabled until the checkbox is checked, or
  clickable but produces a validation error.)
- (Not captured in source data — needs live verification: whether the Website field enforces a
  URL format, and whether that site becomes the account's first tracked site immediately.)

## Related pages
- `docs/wiki/authentication/signup-core.md` — shared signup form validation, email
  verification mechanics (not yet written)
- `docs/wiki/authentication/login.md` — destination of the "Log In" link (not yet written)

## Source
Derived from `ai-context/cases-signup-standard-free.json` (3 TestRail cases — thin, may need a
live-crawl follow-up pass). Drafted 2026-07-14, not yet live-verified against the QA app.
