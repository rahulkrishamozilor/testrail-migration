# Languages

**Nav path:** Languages
**Route:** (not captured in source data — needs live verification)
**Roles:** Account Owner, Admin, Editor — all equal access
**Plan gating:** Adding any language beyond the pre-set default requires a paid plan (Basic or
higher) — the Add Language popup itself is plan-gated. On the Free plan, the "Add Language"
button is enabled but opens an upgrade nudge instead of the popup. See
`docs/wiki/11-billing-upgrade/plan-gates.md` for the full gate-by-plan verification (this
specific nudge case is tracked there, not under Languages, per the two-layer plan-gating
convention).

## Purpose
Languages lets an account configure which languages the cookie consent banner is translated
into, designate a default fallback language, and jump into per-language content editing — so
that site visitors see banner text in their own language (or a sensible fallback when they
don't).

## Page structure
Reached via the app header's **Languages** tab.

- **Info alert banner** at the top of the page, containing a **"Learn more"** link. Clicking it
  opens the **"How to Add a Multilingual Cookie Consent Banner?"** documentation page (external).
- **"Your required languages" card**, directly below the alert banner:
  - A **"+ Add Language"** button in the top right of the card.
    - Free plan: button is enabled but shown with a premium icon.
    - Paid plan (Basic or higher): button is enabled and reads "+ Add Language" with no premium
      icon.
  - The **language list** below the button, with two columns: **"Language list"** and
    **"Language code"** (e.g. English is listed with code `en`).
    - The default language's row shows a **"Default"** badge to the right of its language code.
      Hovering the badge shows a tooltip: *"The default language serves as a fallback option
      when your site is loaded in a language that you haven't added here."*
    - Each row has two controls on the right: an **"Edit Content"** button and a **3-dot menu**
      button. The menu's contents depend on whether the row is the default language and whether
      more than one language exists (see Workflows below).
    - Non-default languages can carry an **"Inactive"** badge instead of/alongside their normal
      state — this appears only after a downgrade from a paid plan to Free (see Validation &
      edge cases).
- **Add Language popup** (opens from "+ Add Language" on a paid plan):
  - Title: **"Add Language"**.
  - Label: **"Select language(s) *"**.
  - A language dropdown containing:
    - A search text field with placeholder **"Search..."**.
    - A scrollable, alphabetically-ordered list of languages with checkboxes (e.g. Abkhazian,
      Afar, Afrikaans, ...). Checking a language does not move it to the top of the list —
      alphabetical order is preserved regardless of selection.
    - The account's existing default language is pre-checked and disabled (cannot be
      unchecked).
    - A dropdown-selector button in the top-right corner of the dropdown collapses/expands the
      list.
    - Selected language names are echoed in a selection field above the search box.
  - **Cancel** and **Add** buttons.
- **Change language popup** and **Delete language popup** — separate, single-purpose popups
  opened from a row's 3-dot menu (see Workflows below).

## Workflows

**1. View the Languages page**
1. Navigate to the Languages page via the app header's Languages tab.
2. Observe the info alert banner (with "Learn more" link) and the "Your required languages"
   card with the language list below it.
   Result: the "+ Add Language" button is visible in the card's top right — enabled with a
   premium icon on Free plan, enabled and unlabeled-icon on paid plans.

**2. Open the multilingual banner documentation**
1. Click the **"Learn more"** link in the info alert banner.
   Result: the "How to Add a Multilingual Cookie Consent Banner?" documentation page opens.

**3. Add a language that has an available translation (canonical happy path)**
Precondition: account on a paid plan (Basic or higher).
1. Click **"+ Add Language"**.
2. In the dropdown, select a language with an available translation (e.g. French) via its
   checkbox.
   Result: the language name is selected and displayed in the selection field above the search
   box.
3. Click **Add**.
   Result: popup closes; the selected language appears in the language list on the Languages
   page.

**4. Add a language that has no available translation**
Precondition: Add Language popup is open.
1. Select a language with no available translation (e.g. Abkhazian) via its checkbox.
   Result: an inline **"Translations not available"** label appears next to the language, and a
   note reads: *"Note: Translations are not available for some of the languages you have added,
   so the banner content that has not been translated will be displayed in English."*
2. Click **Add**.
   Result: popup closes; the language is added to the language list.

**5. Add multiple languages in one action**
Precondition: account on a paid plan (Basic or higher).
1. Click "+ Add Language".
2. Tick the checkboxes for two or more languages (e.g. German and Spanish).
   Result: all selected languages are checked and listed in the selection field above the
   search box.
3. Click **Add**.
   Result: popup closes; all selected languages are added to the language list in a single
   action.

**6. Add Language on the Free plan (plan-gated)**
Precondition: account is on the Free plan.
1. Observe the "Add Language" button in the "Your required languages" card.
   Result: button is enabled and shows a premium icon.
2. Click the button.
   Result: an upgrade nudge popup appears with heading **"Show banner in multiple languages as
   per your visitor's preference!"**, text **"Available in: All premium plans"**, and a
   **"Try Pro for free"** CTA button.

**7. Trigger and dismiss the geo-target cross-sell nudge**
Precondition: account on a paid plan (Basic or higher); language list currently has exactly one
language.
1. Click "+ Add Language", select a language, and click Add.
   Result: popup closes; new language appears in the list; a geo-target in-app nudge popup also
   appears.
2. Inspect the nudge: it shows a feature image, title **"Geo-target your banner for specific
   countries"**, body copy mentioning **"Available in: Pro and Ultimate plans"**, a "help guide"
   link, and two buttons: **"Get geo-targeting now"** and **"Dismiss"**.
3. Click "Get geo-targeting now" → the in-app nudge upgrade page is displayed. Or click
   "Dismiss" → popup closes and does not reappear in the current session.
   (This nudge advertises the separate geo-targeting feature, not the language feature itself —
   it fires only the first time a second language is added.)

**8. Cancel the Add Language popup**
1. With the Add Language popup open, click **Cancel**.
   Result: popup closes; no language is added to the language list.

**9. Click Add with no new language selected**
1. Open the Add Language popup without selecting any new language and click **Add**.
   Result: the Add button is enabled (the existing default language is pre-selected and locked),
   but clicking it with no new selection just closes the popup without adding anything.

**10. Search and filter the language dropdown**
1. Click the dropdown-selector button in the top-right corner of the language dropdown.
   Result: the language list collapses.
2. Type a partial language name into the "Search..." field.
   Result: the list filters to matching languages only, still in alphabetical order.
3. Scroll through the filtered list.
   Result: the list is scrollable.

**11. Edit a language's content**
1. Click the **"Edit Content"** button on a language's row in the list.
   Result: the Edit Content page for that language opens (see
   `docs/wiki/04-cookie-banner/content-gdpr.md` / `content-us-state-laws.md` for the content
   types edited there).

**12. Change the default language when only one language exists**
1. Click the 3-dot menu on the only (default) language row.
   Result: the menu shows a single option, **"Change default language"**.
2. Click it.
   Result: a "Change language" popup opens with a language dropdown (current default marked),
   label **"Select a default language *"**, and **Cancel**/**Change** buttons.
3. Select a different language and click **Change**.
   Result: popup closes; the selected language becomes the new default in the list; a toast
   confirms **"Your default language was updated to [language name]"**.

**13. Set a non-default language as the default**
Precondition: at least two languages exist.
1. Click the 3-dot menu on a non-default language row.
   Result: the menu shows **"Set as Default"** and **"Delete"**.
2. Click "Set as Default".
   Result: a confirmation popup appears: **"Set [language] as the default?"** with warning text
   and **Cancel** / **"Set as default"** buttons.
3. Click "Set as default".
   Result: popup closes; the selected language is now the default in the list.

**14. Delete a non-default language**
Precondition: at least two languages exist, one non-default.
1. Click the 3-dot menu on a non-default language and click **"Delete"**.
   Result: a **"Delete language?"** popup appears with warning text: *"The [language_name]
   language and any translations you've added in this language will be permanently deleted."*
   and **Cancel** / **"Delete language"** buttons.
2. Click "Delete language".
   Result: popup closes; the language is removed from the language list.

## Validation & edge cases
- **Default language's own menu is locked down.** When two or more languages exist, the default
  language's own 3-dot menu still shows "Set as Default" and "Delete", but **both options are
  disabled** — a default language cannot be deleted or re-asserted as default from its own menu.
  It can only be replaced as default via another language's "Set as Default"/"Change default
  language" flow.
- **No-match search.** Typing a string that matches no language (e.g. "zzzz") in the Add
  Language dropdown's search field filters the list down to zero items. There is no explicit
  "no results" message shown — the list is simply empty.
- **Add with nothing new selected.** The Add button stays enabled even with no new selection
  (the default language is pre-checked and locked), but clicking it is a no-op for the list —
  only the popup closes.
- **Plan downgrade (paid → Free) with existing multiple languages.** Preconditions: account was
  on a paid plan with multiple languages added, then downgraded to Free.
  1. Navigating to the Languages page shows an alert banner: **"Multi-lingual banners are not
     available on our free plan"**. Non-default languages now show an **"Inactive"** badge, and
     their "Edit Content" button is disabled.
  2. The 3-dot menu for an Inactive language shows only **"Set as default"**. Selecting it and
     confirming in the resulting popup makes that language the new default and removes its
     Inactive badge — reactivation is possible even while on the Free plan.
  (Source note: this scenario's live-QA verification was skipped in the migration grill step
  because it requires an actual plan downgrade to set up — treat it as documented but not
  independently re-confirmed against the live app.)
- **Two distinct plan-gated nudges, don't confuse them:** the Free-plan "Add Language" nudge
  ("Show banner in multiple languages...", "Available in: All premium plans", "Try Pro for
  free") gates the *language feature itself*; the geo-target nudge ("Geo-target your banner for
  specific countries", "Available in: Pro and Ultimate plans", "Get geo-targeting now") is a
  cross-sell for a *different* feature (geo-targeting) that happens to fire after a paid-plan
  user adds their second language.

## Related pages
- `docs/wiki/04-cookie-banner/general.md`
- `docs/wiki/04-cookie-banner/content-gdpr.md`
- `docs/wiki/04-cookie-banner/content-us-state-laws.md`
- `docs/wiki/11-billing-upgrade/plan-gates.md`

## Source
Derived from `ai-context/cases-languages.json` (23 TestRail cases). Drafted 2026-07-14, not yet
live-verified against the QA app.
