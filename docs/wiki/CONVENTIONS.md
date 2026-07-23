# CookieYes App Wiki — Conventions

> Writing standard for `docs/wiki/*.md`. Read alongside `README.md` (the index) and `log.md` (the
> append-only change record). For TestRail *case* authoring conventions, see the separate
> `migration-conventions.md` at the repo root — that file governs how cases are written; this one
> governs how the app-behavior knowledge base built from them is written.
>
> These pages serve two consumers: a newcomer who has never used CookieYes, and a RAG retrieval
> system that reads each page (or each section of a page) in isolation. Every page must pass the
> completeness standard in `migration-conventions.md` §0 (the newcomer test, the isolation test,
> the RAG accuracy test) before being proposed or applied.

---

## 1. Writing perspective

Third-person, descriptive reference style. The subject of a sentence is the page, feature, or UI
element — never "you" or "I":

- Right: "The Team page lets an Account Owner or Admin invite, view, and manage team members."
- Wrong: "You can use the Team page to invite members."

**Exception — numbered Workflows sections.** Where a page includes a step-by-step Workflows
section (see `consent-log.md` for an example), steps may be written as short imperatives —
"Navigate to Consent Log", "Click the search button" — since they describe a procedure, not a
static feature. The reader is implied, never addressed directly as "you."

**Exception — provenance/verification asides.** Call-outs like "Correction:", "Gap found:", or
"confirmed this run" are allowed to step outside pure feature description to talk about the
documentation's own reliability. That's deliberate — it's how `/wiki-sync` surfaces what's
verified vs. pending — not a style inconsistency.

## 2. No inline TestRail case references

Do not cite specific TestRail case IDs (`#36xxx`) or `ai-context/cases-*.json` filenames inline in
a page's body (Page structure, Workflows, Validation & edge cases, Known gaps sections). Describe
app behavior standalone, as a feature reference — not a case-annotated report.

**Why:** a separate RAG/knowledge base specifically for TestRail case-level lookup is planned for
the future. `docs/wiki/` is meant to stand alone as an app-behavior KB, decoupled from case-level
provenance detail (case IDs, filenames, migration/grill status) that churns far more often than
the app behavior itself does.

**Where citations are still allowed:**
- A page's own **Source** footer section may name the backing `ai-context/cases-*.json` file(s) at
  a coarse, file-level granularity (e.g. "Derived from `cases-team.json` (17 cases)") — this
  matches the convention already used across every page.
- `log.md` is the one file that keeps case-ID citations throughout, since it's an audit trail, not
  a KB page — `/wiki-sync` explicitly records `source (case id / live check / progress file)` for
  every log entry. That requirement stays.

## 3. Freshly-migrated content is source of truth

When a section's underlying TestRail cases were just migrated (the user did the migration
directly, even if the pipeline's own `grill_status`/`audit_status` field isn't set yet), state the
migrated case's steps and titles plainly as documented fact. Do not hedge nearly every paragraph
with "not confirmed this run" / "pending verification."

- Keep genuine **live-check findings** — real discrepancies actually caught via a live browser
  check (a header control that doesn't match its case description, a punctuation mismatch, an
  undocumented feature) — as distinct call-outs. Those are new information the reader needs.
- Fold the general "not yet manually reviewed" caveat into **one** note — in Known gaps and/or the
  Source section — not scattered inline after every claim.
- Expect the page to update incrementally as manual review happens, rather than trying to
  front-load exhaustive verification before drafting anything.

## 4. No test-environment names

Do not mention QA2, QA1, `prod-test`, `kilohub.com`, or other internal test-environment
identifiers inside a page's body. The knowledge base describes the production app as a user
experiences it; test-environment plumbing is an internal detail of how this repo verifies pages,
not a fact about the app.

## 5. Page skeleton

Every page follows the same shape, in this order:

1. **Header block** — `**Nav path:**`, `**Route:**`, `**Roles:**`, `**Plan gating:**`. Use
   "(not captured in source data — needs live verification)" rather than guessing when a fact
   genuinely isn't known.
2. **Purpose** — one paragraph: what the feature is for and why a user would use it.
3. **Page structure** — descriptive breakdown of the UI: cards, fields, buttons, states.
4. **Workflows** (where applicable) — numbered, imperative step sequences for multi-step
   procedures (exports, transfers, generation flows, etc.). Not every page needs this section.
5. **Validation & edge cases** — the failure modes, mismatches, and plan-dependent or
   state-dependent variations worth calling out explicitly.
6. **Known gaps** — what hasn't been checked yet, using the framing in §3 above.
7. **Related pages** — links to other `docs/wiki/*.md` pages this one depends on or is depended on
   by.
8. **Source** — what `ai-context/` file(s) this page was derived from (file-level only, per §2),
   when it was drafted, and its live-verification status.

A section can map to more than one page (e.g. Organisations & Sites splits into Organisation
Management / Site Management / Site Transfer). Resolve section → page(s) via `README.md`'s table,
not by guessing a filename transform.

**No numbered path prefixes.** Folder and file names use plain feature names
(`cookie-banner/general.md`, `billing-upgrade/plan-gates.md`) — never a `testrail-suite-v2.md`
section number (no `04-cookie-banner/`, `11-billing-upgrade/`). The same reasoning as §2 applies
one level up: `docs/wiki/` is meant to stand alone as an app-behavior KB, and a migration-specific
section number baked into every path is exactly the kind of provenance coupling that decouples
badly — those numbers already drift (see `testrail-suite-v2.md`'s own note on sections renumbered
out of sequence to avoid a ripple effect). The section-tree ordering this would otherwise convey
lives in `README.md`'s numbered `##` headings instead, which is the right place for it — that
file is this project's own maintenance index, not a page an external reader or RAG system
consumes standalone.

## 6. README.md and log.md

- `README.md` is the index: one table per top-level section, columns Page / Source / Cases /
  Freshness. Update a page's Freshness column whenever its live-verification status changes.
  Update the top-level page count and the "Known gaps / next pass" list whenever a page is added.
- `log.md` is append-only. Every applied wiki change gets an entry, in the form documented at the
  top of that file. Never edit or remove a past entry — only append.
