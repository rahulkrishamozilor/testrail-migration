# /audit-section

You are auditing an **already-published** v2 TestRail section for text-fidelity regressions:
places where an expected result asserts specific text is visible on the page, but the quoted
wording was reworded away somewhere between the Suite 6 source and the published v2 case — plus
any structural mismatch `validate-cases-file` can catch mechanically.

This is a **retrospective audit of published output**, not a pre-publish check — it exists
because that check didn't always happen the first time (see the Site Transfer cases in
`cases-organisation-and-sites.json`, several of which needed exact banner/tooltip/email copy
restored after a manual retrospective pass — this command is that pass, formalized and
repeatable). `/grill-section` verifies a *draft* against the live app before publish; this
command verifies what's *already live in TestRail* against its own Suite 6 source.

---

## Input

`$ARGUMENTS` — a section name (same as you'd pass to `/fetch-section`), or `all` to audit every
published section in one run.

The audited file is `ai-context/cases-<slug>.json`, using the canonical slug rule defined in
`/fetch-section` Step 5 (strip leading numeric prefix, lowercase, spaces → hyphens).

If only `ai-context/draft-<slug>.json` exists (not yet published), stop and tell the user:
> This section hasn't been published yet — there's nothing to audit against TestRail. Run
> `/grill-section` and `/migrate-section` first.

If `$ARGUMENTS` is `all`, resolve every `ai-context/cases-*.json` file (`ls ai-context/cases-*.json`).
For each one, check whether its top-level JSON is a bare list rather than the `{section,
cases:[...]}` envelope (the same check `validate-cases-file` does). A bare list means the file
predates the draft/cases pipeline and has no `source_case_ids` field to audit against — but
**do not assume this means the cases are unpublished**. Check the cases' `id` fields and/or run
`validate-cases-file --verify-routing`: if the ids are real and routing verifies against live
TestRail, these are genuinely published cases sitting in the old schema, not a draft that was
never pushed (a bare list with `id: null` throughout — never actually published — is a different,
narrower case than a bare list with real, live ids). Either way, **skip the fidelity check** for
these files (no `source_case_ids` means nothing to diff against), but report them accurately:
- Bare list, ids null / routing fails → "needs schema normalization first, not yet published."
- Bare list, ids real and routing verifies → "published live content sitting in the legacy
  schema — needs schema normalization before it can go through `/grill-section` or
  `/audit-section` fidelity checks; not the same as an unpublished draft."

---

## Step 1 — Structural check

Run the mechanical check first — it's free, and it catches a different failure class than what
this command exists to find (id/duplicate/routing problems, not text fidelity):

```bash
uv run .claude/scripts/fetch_testrail.py validate-cases-file ai-context/cases-<slug>.json \
  --verify-routing --verify-completeness --project-id 1 --suite-id <v2_suite_id>
```

`--verify-completeness` catches a failure class `--verify-routing` cannot: cases published
directly to TestRail outside `/fetch-section` → `/migrate-section` (or moved/deleted live) and
never reflected in the local file. It diffs this file's own top-level `section_id` against what's
actually live there — `untracked_live_case` means TestRail has a case this file doesn't know
about (real precedent: 22 live cases in Cookie Banner > General sat untracked until a manual
backfill); `stale_local_case` means the reverse (a case this file claims lives here doesn't,
live). If the file has no top-level `section_id` yet, this check can't run
(`completeness_no_section_id`) — note that in the report rather than skipping it silently; it
means the file needs `section_id` backfilled before this class of drift can be caught at all.

Record any errors verbatim for the final report (Step 5). Proceed to Step 2 regardless of
whether it passes — a structural error in one case doesn't block auditing the others. If
`untracked_live_case` fires, treat it like the `unpublished_id`-precedent in the note above: check
whether the live case's content already appears in this file under a different id (a rename/retitle
rather than a true gap) before assuming it needs to be backfilled from scratch.

**Before recommending a fix for any `unpublished_id` finding, check whether the case already
exists elsewhere first.** An `id: null` case sitting in an otherwise-published `cases-*.json`
file is not automatically a case that needs `batch-add-cases` — it may be a stale leftover from
before the case was corrected and re-routed to a different section (its own `rewrite_notes` is
the first place to check for a routing note like "should route to X"), and republishing it as-is
would create a true duplicate of content that's already live elsewhere. Real precedent: three
`unpublished_id` cases in Cookie Banner turned out to already be published, verbatim, under
slightly different titles in Plan Gates — their `rewrite_notes` had said so all along. Before
concluding a case needs to be created, run `dedup-check` against the section named in its
`rewrite_notes` (or any plausible target) and read the result — a near-1.0 match means delete
the stale local copy, not publish it again.

---

## Step 2 — Load state and resume

Read `ai-context/cases-<slug>.json`. Check each case for an existing `"audit_status"` field. If
any are present, this is a resumed run — report how many cases are already audited vs.
remaining, and skip any case that already has an `audit_status` in Step 3 (do not re-check it).

---

## Step 3 — Check each case for text fidelity (one by one)

For every case without an `audit_status`:

### 3a. Does this case need a fidelity check at all?

One test, no category filter (per `migration-conventions.md` §4, "Quoted on-page text — always
verbatim"): **does any step, precondition, or expected result in this case quote specific text
as appearing on the page?** A banner, a status badge, a button label, a dialog message, a
tooltip, an email body, a page title — anything asserting "the app shows/displays X" in quotes.
It does not matter whether the quote looks legally significant, decorative, or trivial (a plain
status badge is just as in-scope as a legal disclosure) — if the case commits to a specific
quoted string, that commitment needs checking.

- If the case quotes specific on-page text anywhere → it needs a check (3b).
- If every step/expected result only describes an outcome or state change without quoting
  specific text ("the popup should close", "the toggle should be off by default", "the button
  should be disabled") → `"audit_status": "not-applicable"`. There is nothing to compare against
  because the case never committed to specific wording.
- A vague/generic phrasing pattern from `migration-conventions.md` §3's "vague to avoid" table
  (e.g. "should be reflected", "corresponding changes should occur") sitting where a quote would
  normally go is itself a smell — it may mean a quote was paraphrased down into vagueness. Treat
  it as needing a check: fetch the source and see whether it had a specific string this case
  should have kept.

Do not narrow this further by guessing at "importance" — that judgment call is exactly what
caused an inconsistency in an earlier run of this command (a plain scan-status badge was
initially treated as out of scope while a nearly identical one was fixed). If it's quoted as
on-page text, check it.

### 3b. Fetch the source and compare

If the case has `source_case_ids`, fetch each one:

```
mcp__testrail-search__get_test_case(case_id=<id>)
```

Compare the source's actual wording for the quoted content against what's currently in the v2
case.

**Rule: `grill_status` outranks the Suite 6 source when the two disagree.** If the case's
`grill_status` is `"confirmed"` or `"fixed"`, a source/draft mismatch is not by itself evidence
of a fidelity regression — per `/grill-section` Step 3c, both verdicts mean the quoted text was
already checked word-for-word against the live QA app (`"confirmed"`: the draft already matched
live and nothing changed; `"fixed"`: the draft was actively corrected to match live). Either can
legitimately supersede a stale Suite 6 default — the legacy suite predates the current product
and is not guaranteed to reflect it. **Do not "restore" the Suite 6 wording over a
`"confirmed"`/`"fixed"` case just because they disagree.**

This priority does not extend to `grill_status: "needs-manual-check"` or `"skipped:<reason-code>"`
— neither carries a completed live-text check (the former is grill's own unresolved flag, the
latter was never driven at all). For those, and for cases with no `grill_status` at all, fall
back to the normal source-diff logic below with no special deference either way.

Even under the priority rule, don't stop at "grill said so" if something about the *current* v2
wording itself looks off — reads like a paraphrase rather than a verbatim on-page string, looks
truncated or cut short, or is internally inconsistent with a pattern the rest of the section
otherwise follows consistently. That's a signal grill's check may not have caught this specific
string (or was checking a different part of the same case). In that situation, validate against
the live app (Step 4) if at all possible before touching anything — do not silently prefer the
source either. If a live check isn't feasible right now, leave the case `"reworded-flagged"` and
say in `audit_note` which side (source vs. current draft) you suspect and why, rather than
picking one blind.

With that priority applied, there are three outcomes:

- **Matches verbatim, or the v2 wording is a legitimate structural rewrite with no quoted
  content lost** → `"audit_status": "verbatim-confirmed"`.
- **Reworded, `grill_status` doesn't already cover it (see rule above), and you can confidently
  restore the exact source wording** → correct the field in place — use the Edit tool with exact
  string matching directly on the target file, the same discipline as `/grill-section` Step 3c
  (no tmp scripts, no batch rewrites) — and set `"audit_status": "reworded-fixed"`. Record what
  changed and which source case it was restored from in `audit_note`.
- **Reworded, but the source itself is ambiguous/truncated, `grill_status` says the current
  wording was already live-verified, or you can't be confident of the exact correct wording
  without checking the live app** → leave the text as-is, set `"audit_status": "reworded-flagged"`,
  and record why in `audit_note` — including, when relevant, that the disagreement is with a
  `"confirmed"`/`"fixed"` grill verdict and a live re-check (not a source restore) is the
  recommended next step.

If the case has no `source_case_ids` (a gap case found during grilling, or newly authored) and
3a still flagged it as needing a check, there's no source to diff against — set
`"audit_status": "no-source-case"` and note in `audit_note` what a live spot-check should
confirm.

### 3c. Write back immediately

Same discipline as `/grill-section`: write `audit_status` / `audit_note` / any corrected field
back into `ai-context/cases-<slug>.json` **after each case**, not batched at the end. This makes
the run resumable if interrupted (Step 2 picks up where it left off).

---

## Step 4 — Optional live spot-check (recommended, not mandatory)

For every case left as `"reworded-flagged"` or `"no-source-case"` after Step 3 — the ones the
source diff alone couldn't resolve — offer to spot-check against the live app, reusing
`/grill-section`'s login and session-switching logic (its Step 2) rather than re-deriving it.
Only these flagged cases need a live check; do not re-verify cases already
`"verbatim-confirmed"` or `"reworded-fixed"`.

Prioritize, within that flagged set, any case flagged specifically because it conflicts with a
`"confirmed"`/`"fixed"` `grill_status` (per the priority rule in 3b) — those are exactly the
cases where a live check is the only way to settle whether the current wording (already
live-verified once, per grill) or the Suite 6 source is actually right, since neither a blind
source-restore nor a blind "grill wins" assumption is safe to apply on paper alone.

Also prioritize any case whose `grill_status` is still `"needs-manual-check"` — that status means
`/grill-section` itself never resolved it, so nothing has verified this case at all yet. Left
alone, these sit unresolved indefinitely (a real case: two cases stuck at `needs-manual-check`
were only found and resolved by accident, well after the section had already gone through both
grilling and a prior audit pass). Don't let a case's absence from the "flagged" set above (it may
already read `"verbatim-confirmed"` from a source-only check) excuse it from this priority — a
source diff can still pass while the underlying `needs-manual-check` question goes unanswered.

**Ask the user before starting a browser session** — this step has real cost (login,
navigation, possibly account switching) proportional to the number of flagged cases, not the
size of the section.

For each flagged case: navigate to the precondition's starting state, drive to where the quoted
text should appear, and compare word-for-word against what's live (or, for email content, an
actual received email — same constraint `/grill-section` operates under for `email-required`
cases). Update `audit_status` to `"verbatim-confirmed"` or `"reworded-fixed"` accordingly, with
the same write-back discipline as Step 3c. If it still can't be resolved live (e.g. the exact
scenario can't be reproduced), leave it `"reworded-flagged"` and say why.

---

## Step 5 — Report

Tally `audit_status` values by reading the file (not from context) and produce:

```
## Audit report — <section name>

**Structural:** clean | N validate-cases-file error(s) — see below
**Untracked live cases:** N (live in TestRail, missing from this file)
**Stale local entries:** N (file claims a case lives here; it doesn't, live)
**Verbatim-confirmed:** X
**Reworded — fixed:** N
**Reworded — flagged for review:** N
**No source case (unresolved):** N
**Not applicable:** X

### Structural errors
[validate-cases-file output, verbatim]

### Reworded — fixed
- [title] — was: "..." → now: "..." (source: C#####)

### Reworded — flagged for review
- [title] — v2 says: "..." | source (C#####) suggests: "..." | why unresolved: ...

### No source case (unresolved)
- [title] — audit_note
```

Write the top-level `"audited_at"` timestamp (`date -u +"%Y-%m-%dT%H:%M:%SZ"`) into the file
once every case has an `audit_status`.

If `$ARGUMENTS` was `all`, run Steps 1–5 per file, then prepend a cross-section summary table
(files audited, files skipped for schema normalization, total fixed, total flagged) before the
per-file reports.

---

## Rules

- This command never touches TestRail directly — every fix in Step 3/4 is local, to
  `ai-context/cases-<slug>.json`. If a `reworded-fixed` correction should also be pushed to
  TestRail, that's a separate, explicit step: tell the user to run `batch-update-cases
  --from-draft` and wait for approval, the same as any other case content change. Do not fold
  that into this command.
- Never invent a "corrected" quote that isn't actually sourced from the Suite 6 case or the live
  app — an unconfirmed guess is a `reworded-flagged`, not a `reworded-fixed`.
- `grill_status` outranks the Suite 6 source on disagreement (see 3b): a `"confirmed"`/`"fixed"`
  verdict means the quoted text already passed a live word-for-word check, so don't restore
  source wording over it. Only depart from that if the current wording itself looks truncated,
  rephrased, or inconsistent with the section's own pattern — and then validate live (Step 4)
  before changing anything, rather than trusting either side on paper. `"needs-manual-check"` and
  `"skipped:<reason-code>"` carry no such guarantee; fall back to the normal source diff for those.
- Follow the same draft-file convention as `/grill-section`: fixes go directly into
  `ai-context/cases-<slug>.json`. Never create a new file (no `cases-<slug>-audit.json`,
  no `draft-<slug>-fixes.json`).
- Report every case, even the ones needing no action (`not-applicable`, `verbatim-confirmed`) —
  a silently-skipped case is indistinguishable from an unaudited one.
- No category filtering on whether a quote "matters" — a plain status badge gets the same
  verbatim scrutiny as a legal disclosure. The only filter is 3a's test: was specific on-page
  text quoted at all.
- For reference, the full set of `audit_status` values used across the file:
  - `"verbatim-confirmed"` — checked against source (and/or live app); quoted text matches, or
    the case quotes nothing
  - `"reworded-fixed"` — a quote was paraphrased; corrected back to the exact wording, source noted
  - `"reworded-flagged"` — paraphrase found but the exact correct wording couldn't be confirmed
  - `"no-source-case"` — no `source_case_ids` to diff against; needs a live check or human review
  - `"not-applicable"` — this case quotes no specific on-page text; no verbatim requirement applies
