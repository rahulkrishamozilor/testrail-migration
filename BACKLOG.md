# Backlog

Cross-cutting follow-up tasks that don't belong to a single section's test-case coverage gaps —
see `coverage-gaps.md` for those. This file tracks process-level or suite-wide items: doc/wiki
accuracy audits, structural decisions that block casing more than one section, etc.

Mark closed items with ~~strikethrough~~ and the date/resolution, rather than deleting the line —
same convention as `coverage-gaps.md`.

---

## Character limit — internal-docs vs. live vs. wiki audit

**What:** `internal-docs/Character limit - Privacy Policy Fields (1).pdf`'s "current limit" column
has been found stale in multiple places across the Privacy Policy Generator wizard — Data
Retention's custom-period and "not yet decided" fields, Disclosure of Data's four field-level
limits, and now Miscellaneous Disclosures' DPO contact, data controller/representative, custom
safeguard, and CCPA metrics-link fields. In every case, live already enforces the doc's own
**recommended** value (pages 19–21), not its stated **current** one — the doc's own Assessment
column already self-flags most of these as "Increase," so this isn't unnoticed drift, just a
"current" column nobody went back to update after the recommendation shipped.

**Why it matters:** the doc still reads as authoritative for anyone who hasn't cross-checked it
against a specific gap-closing pass's reconciliation notes, and `docs/wiki/legal-policies/
privacy-policy-generator.md` records confirmed character limits for some fields (e.g. Contact
Information, ~line 131–135; another field ~line 184–186) but not others — Miscellaneous
Disclosures currently has none recorded despite this pass confirming four.

**Task:**
- ~~Sweep the remaining PPG steps (Company Details, Collection of Data, Use of Data) for the same
  stale-current-limit pattern~~ — **done 2026-07-17.** Company Details and Use of Data turned out
  already fully covered (some already carrying the same doc-mismatch finding, e.g. cases 39455,
  39460, 39477, 39613 — none needed new cases). Collection of Data had three genuine gaps with no
  boundary-value case at all: cookie policy URL (doc 500 → live 2000), "Do Not Track" response
  (doc 2000 → live 2500), and the review/change-process description field (doc 2000 → live 2500).
  All three now have a draft case in `ai-context/draft-privacy-policy-generator.json` (unpublished
  — awaiting `/grill-section` and `/migrate-section`). No further steps in this feature remain
  unswept for this pattern.
- ~~Update the wiki page to record every confirmed character limit per field~~ — **done 2026-07-17**
  for the three fields above (`docs/wiki/legal-policies/privacy-policy-generator.md`, section
  3b Additional Information). Miscellaneous Disclosures' four fields from the same 2026-07-16 pass
  (DPO, controller, custom safeguard, CCPA metrics) are still not recorded in the wiki — that part
  of this task is still open.
- Decide whether to flag the stale `internal-docs` PDF back to whoever owns it, since it's an
  authored spec doc that already contains its own correct recommendation — this is a "someone
  forgot to update one column" fix, not new analysis. Still open.

---

## Plan Gates — Layer 2 suite-wide check

**What:** Already logged in `coverage-gaps.md` (09. Legal Policies > Privacy Policy Generator,
identified 2026-07-16) — PPG's clause/field-level plan gates (for-profit question, CCPA-gated
chips, the entirely-gated Disclosure of data step, the retention "Not yet decided" option) exist
only as Layer 1 touchpoint cases in the feature section; no Layer 2 case in `11. Billing &
Upgrade > Plan Gates` consolidates them per plan tier, per `testrail-suite-v2.md`'s "Plan-gated
features" Layer 2 feature-scoped exception.

**Why it's here and not just in coverage-gaps.md:** it was explicitly held as a suite-wide
question, not a PPG-only one — every section in the suite has plan gates, so authoring PPG's
Layer 2 cases first would mean doing this section-by-section piecemeal instead of once, properly.

**Task:** Audit which sections already have their Layer 2 Plan Gates case and which only have
scattered Layer 1 touchpoint cases (like PPG). Not yet started. Needs user approval before casing
either way, for PPG or any other section.

---

*(Add new items below as they're identified.)*
