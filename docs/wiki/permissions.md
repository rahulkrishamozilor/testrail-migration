# Permissions

**Nav path:** (cross-cutting — not a single page; the role hierarchy governs controls across
Profile & Account, Team, Organisations & Sites, and any plan-upgrade nudge app-wide)
**Route:** N/A — no dedicated route; see each affected feature page for the actual control
**Roles:** This page IS the role reference for the whole app.
**Plan gating:** Not plan-gated itself; interacts with plan gating in one confirmed case (an
Account-Owner-only restriction on initiating a plan upgrade — see Validation & edge cases).

## Purpose

CookieYes has three account roles, forming a strict hierarchy: **Editor ⊂ Admin ⊂ Account
Owner**. Every organisation has exactly one Account Owner; Admin and Editor are roles assigned
to invited team members (see `docs/wiki/profile-account/team.md` for the invite flow).

For most of the app — Cookie Banner, Cookie Manager, Consent Log, Languages, Advanced Settings,
Reports, Dashboard, Onboarding — all three roles have identical access; there is no restriction
to document. This page exists for the places where access genuinely diverges, split into two
tiers:

- **Account-Owner-only actions** — blocked for both Admin and Editor. Covers organisation
  creation, site creation/deletion/transfer, account ownership transfer, subscription
  cancellation, and initiating a plan upgrade.
- **Editor-only restrictions** — blocked for Editor alone; Admin has the same access as the
  Account Owner. Covers team management (inviting, changing roles, removing members),
  organisation/site name editing, site URL editing, and adding a staging site.

## Page structure

Not applicable — this is a cross-cutting reference, not a page with its own UI. The controls
described below render inline on their respective feature pages (Team, Organisations & Sites,
Cookie Banner), each disabled or hidden according to the viewer's role.

## Validation & edge cases

### Account-Owner-only (Admin and Editor both blocked)

- **Create an organisation** — the "+ New organisation" button is disabled, with a tooltip:
  "Only the Account Owner can create a new organisation."
- **Add a site** — the "+ New site" button is disabled, with a tooltip: "Only the Account Owner
  can add a new site."
- **Delete a site** — the "Delete site" option in a site's More (⋯) menu is disabled, with a
  tooltip: "Only the Account Owner can delete a site."
- **Transfer a site** — the "Transfer site" option in a site's More (⋯) menu is disabled, with a
  tooltip: "Only the Account Owner can transfer a site."
- **Transfer account ownership** — the "Transfer ownership" button is not rendered at all on the
  Account Owner card for Admin or Editor (not merely disabled).
- **Cancel a subscription** — the "Cancel subscription" option is disabled, with a tooltip:
  "Only the Account Owner can cancel subscription."
- **Initiate a plan upgrade** — confirmed on one touchpoint (Cookie Banner's Custom CSS upgrade
  nudge): the nudge's "Try it now" button is disabled, with a tooltip: "Only account owner can
  change plan." Not yet confirmed whether this restriction generalizes to every upgrade nudge
  app-wide, or is specific to this one nudge — see Known gaps.

### Editor-only (Admin has Account-Owner-equivalent access; only Editor is blocked)

- **Invite a new team member** — the "+ Invite new user" button is disabled by default (not
  clickable-then-blocked), with a tooltip: "Only the Account Owner or an Admin can manage a
  user."
- **Change a member's role / remove a member** — the "More" (...) option on another member's row
  is disabled by default, with the same tooltip as above. This is a shared, generic
  "manage a user" tooltip, not action-specific wording — the same tooltip text appears for both
  the invite button and the per-row More menu.
- **Edit a site URL** — the "Edit site URL" option is disabled, with a tooltip: "Only the Account
  Owner or an Admin can edit the site URL."
- **Edit a site name** — the "Edit site name" option is disabled, with a tooltip: "Only the
  Account Owner or an Admin can edit the site name."
- **Edit an organisation name** — the organisation's More (⋯) menu is not rendered at all for an
  Editor (not merely disabled), so "Edit Organisation Name" is unreachable rather than blocked.
- **Add a staging site** — the "Add staging site" option is disabled for an Editor with no
  tooltip observed (aria-disabled state only) — distinct from the other Editor-only
  restrictions above, which do show a tooltip. This is a separate restriction from the Free-plan
  gate on the same control (see `docs/wiki/billing-upgrade/plan-gates.md`'s Known gaps): an
  Editor on a paid plan is still blocked by role, independent of plan tier.

### UI pattern inconsistency

Three different mechanisms enforce these restrictions, inconsistently: (1) a disabled control
with an explanatory tooltip on hover (most cases), (2) a control disabled with no tooltip at all
(Editor + Add staging site), (3) the control not rendered at all rather than shown-disabled
(Transfer ownership button for Admin/Editor; the organisation More menu for Editor). This is a
real, confirmed inconsistency in how the app communicates role restrictions to the user, not a
documentation gap.

## Known gaps

- Whether the Account-Owner-only plan-upgrade restriction (confirmed on the Cookie Banner Custom
  CSS nudge) applies to every upgrade nudge app-wide, or just that one touchpoint, is unconfirmed.
- Billing & subscription management more broadly (beyond "cancel a subscription") is asserted as
  Account-Owner-only by the permission model but has no dedicated case set of its own yet — no
  Billing & Upgrade wiki page exists beyond `plan-gates.md`.
- No case set exists yet for role divergence (if any) in Agency, Platforms, or Internal Tools
  sections.

## Related pages

- `docs/wiki/profile-account/team.md` — team invite/role-management flows this page's
  Editor-only restrictions apply to
- `docs/wiki/profile-account/organisations-and-sites/organisation-management.md` — organisation
  creation, naming, and ownership transfer
- `docs/wiki/profile-account/organisations-and-sites/site-management.md` — site creation,
  editing, deletion, and subscription cancellation
- `docs/wiki/profile-account/organisations-and-sites/site-transfer.md` — site transfer
- `docs/wiki/billing-upgrade/plan-gates.md` — plan-tier gating, a separate axis from the
  role-based restrictions on this page

## Source

Derived from 13 permission-divergence cases across `cases-organisation-and-sites.json` (10
cases), `cases-team.json` (2 cases), and `cases-colours.json` (1 case) — all live-verified
(`confirmed`/`fixed`, one `skipped:plan-gated` for an already-covered plan interaction), plus the
role hierarchy table in `testrail-suite-v2.md`. Drafted 2026-07-23 via `/wiki-sync`, first version
of this page.
