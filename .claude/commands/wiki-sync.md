# /wiki-sync

You are keeping `docs/wiki/` — the LLM-readable knowledge base of the CookieYes web app — correct,
complete, and current for one section. This is the **lint + ingest** pass in the sense of
Karpathy's LLM-wiki pattern (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
`docs/wiki/README.md` already functions as that pattern's `index.md` (a per-page catalog with
source/freshness metadata); this command is the periodic health check that keeps the pages it
indexes from silently drifting, plus the mechanism that turns newly-verified facts into wiki
updates.

This command is **not scoped to the migration** — the migration is what's seeding the wiki's first
pass right now, but this command is meant to keep running long after Suite 6 → v2 migration work
is done, as the product keeps changing. Don't treat "migration complete" as a reason this command
stops being useful.

**How this differs from its siblings:** `/audit-section` checks whether a *TestRail case's* quoted
text still matches its Suite 6 source. This command checks whether the *wiki page* still matches
what the case notes and the live app actually say — a different document, a different source of
truth, and (per this project's decision) a different, harder rule on what happens when the two
disagree: see Step 4's contradiction handling.

A separate consumer project builds and serves the actual embedded/queryable wiki from
`docs/wiki/*.md`. This command has **no visibility into and makes no attempt to trigger** that
project's reindexing — its job ends at leaving `docs/wiki/` (and its own log) in a correct,
committed state. If reindexing needs to be signaled later, that's a separate, explicit
follow-up — do not guess at a mechanism here.

---

## Input

`$ARGUMENTS` — a section name (same convention as `/fetch-section`/`/audit-section`), or `all` for
every section that has either a wiki page or a published `cases-*.json` file. Optionally trailing
`--verify=auto|always|never` (default `auto`) — see Step 3.

A section can map to **multiple** wiki pages (e.g. `cases-organisation-and-sites.json` backs three
separate pages — Organisation Management, Site Management, Site Transfer — per
`docs/wiki/README.md`'s table). Resolve section → page(s) via that table's **Source** column, not
by guessing a filename transform. If a section has no wiki page yet at all (see the "Not yet
documented" call-outs in `docs/wiki/README.md`), that's Step 4's addition case, not an error —
report it as "no page yet" and proceed to draft one if there's enough source material.

---

## Step 1 — Gather candidate sources

Pull from every source that exists for this section — don't assume only one applies.

### 1a. Stray progress/handoff files

`ls ai-context/*.md` and grep each for this section's name or its `cases-<slug>.json` filename.
Any match is a candidate source — these are the ad hoc sweep/handoff notes
(`business-details-matrix-sweep-progress.md` and `plan-gates-ppg-resweep-progress.md` were two
real examples this project produced and later had to reconcile by hand; this step exists so that
reconciliation stops being a manual archaeology exercise).

### 1b. Published case notes

Load `ai-context/cases-<slug>.json`. Pull every `rewrite_notes` / `audit_notes` / `grill_note` /
`grill_notes` field. This is the primary, ongoing source once migration itself winds down — new
cases written by any future workflow will keep populating these fields regardless of whether this
specific command's pipeline authored them.

### 1c. The wiki page itself and its freshness

Read the page(s) resolved above, plus its row in `docs/wiki/README.md`'s table (Source, Cases,
Freshness columns) and any per-page "Source"/freshness note in the page's own header block. This
tells you what's already documented and how recently it was last verified — read it before
proposing anything, so you're diffing against current state, not guessing at it.

---

## Step 2 — Classify each candidate fact

Every note pulled in Step 1 falls into one of three buckets. Getting this right is what keeps this
command from drowning its own output in noise — most notes in a well-covered section just say
"confirmed matches source," which is not new information.

- **Routine confirmation** — "confirmed," "matches source," "verbatim-confirmed" with nothing
  else notable. No new information. Skip; do not surface in the report.
- **Change-signaling** — language like "resolved," "corrected," "previously undocumented,"
  "contradicts," "gap found," "reworded-fixed," or anything describing a finding rather than a
  routine pass. These are candidates for a wiki update — carry them to Step 3.
- **Unverified source** — `grill_status`/`audit_status` literally `"not-tracked-by-repo"`, or
  `rewrite_notes` language like "backfilled from live TestRail," "outside this repo's pipeline,"
  or similar. **Never let one of these alone back a wiki fact.** Either:
  - a second, verified source corroborates the same fact (then proceed using that source), or
  - it goes through Step 3's live-check unconditionally before it can back anything, or
  - it doesn't get used as documentation material at all — instead, surface it as **flagged
    pipeline debt** in the final report ("N cases in this section have never been through
    `/grill-section` or `/audit-section`") and stop there. Fixing that debt is those commands'
    job, not this one's.

---

## Step 3 — Decide whether a live check is needed

For each change-signaling candidate fact, apply these triggers before trusting it as-is:

1. **Conflicting sources** — two notes disagree and text alone can't resolve which is current.
2. **Unverified-only source** — per Step 2, a `not-tracked-by-repo`-only fact always triggers this.
3. **High-stakes content** — anything touching legally/functionally load-bearing text, the same
   bar `migration-conventions.md` §4 already uses for consent/banner copy, warnings, transactional
   emails.
4. **Stale past the tracked freshness** — read the page's own freshness note / the README's
   Freshness column (Step 1c) rather than inferring age from a note's own date; if it says
   "not live-verified" or is old enough that the feature area plausibly changed since, this
   triggers too.

None of these fire → trust the note, no live check, proceed to Step 4.

**`--verify` override:** `always` forces a live check on every change-signaling fact regardless of
the triggers above (expensive — use before something like a release, not routinely). `never` skips
all live checks; any fact that would have triggered one is instead reported as "needs live
verification" rather than silently trusted or silently dropped. `auto` (default) applies the
triggers as written.

**Mechanism — do not write new Playwright-driving instructions.** Construct a synthetic,
throwaway case object in the same shape `/grill-section` already consumes —
`{title, preconditions, customStepsSeparated: [{content, expected}]}` — either lifted directly
from an existing case if the fact is tied to one, or authored fresh in the same shape if it's a
synthesized cross-cutting conclusion from a progress file. Then run `/grill-section`'s Step 3
(3a navigate, 3b execute and compare, 3c record) against that one synthetic case exactly as
written there — reuse its login/session-switching (its Step 2) rather than re-deriving it.

**Ask the user before starting a browser session** — same courtesy `/audit-section` Step 4
already extends, for the same reason (real cost proportional to how many facts need checking).

---

## Step 4 — Reconcile against the wiki page

For each fact that's now either trusted-as-is or live-checked, compare it against the current wiki
page text. Three outcomes:

- **Already matches** — no action.
- **Addition** — the wiki doesn't cover this at all yet (a new fact, or an entire missing page per
  Step "Input"). Draft it.
- **Contradiction** — the wiki says one thing, the verified fact says another.

**On a contradiction, do not assume the wiki is what's wrong.** There are two readings, and picking
the wrong one silently is worse than doing nothing:
1. The wiki was never correct (a stale draft, a paraphrase drift, a bug in how it was first
   written).
2. The wiki was correct when written and **the app has changed since** — meaning this contradiction
   is evidence of a real product regression or intentional change, not a documentation bug.

**Always escalate both readings to the user for review. Never auto-resolve a contradiction, even
one that looks obviously like stale documentation.** This project's own explicit decision on this:
auto-fixing risks quietly turning a real regression into "documented, working as intended" — and
if that happens, there is no later signal that would ever catch it. This is a hard rule, not a
default that can be skipped when a case looks clear-cut.

**Every drafted addition or correction must pass `migration-conventions.md` §0** (0a newcomer test,
0b isolation test, 0c RAG accuracy test) before being proposed — this is the wiki's own stated
completeness bar per `docs/wiki/README.md`'s header, not a new rule invented for this command.

---

## Step 5 — Present for approval

Never write to `docs/wiki/*.md` without explicit approval — the same discipline this project
already holds for TestRail cases ("cases are never created without explicit user approval"),
extended here to documentation. Present:
- Every proposed addition/correction, in full drafted text.
- Every contradiction, with both readings from Step 4 laid out for the user to judge, not resolved
  for them.
- Every fact flagged as pipeline debt (Step 2) or needing a live check that wasn't run
  (`--verify=never`).

Wait for explicit approval before Step 6. Partial approval is fine — apply only what's approved.

---

## Step 6 — Apply and log

For each approved change:
1. Apply it to the wiki page directly (Edit tool, exact-match discipline — no new files
   alongside the existing page).
2. Update that page's own freshness/source note, and its row in `docs/wiki/README.md`'s
   Freshness column, to reflect what was just verified/changed and when.
3. Append an entry to `docs/wiki/log.md` (create it if it doesn't exist yet, with a one-line header
   explaining it's an append-only record) in the form:
   ```
   ## [YYYY-MM-DD] <ingest|lint> | <section/page>
   - <one line per change: what changed, why, source (case id / live check / progress file)>
   ```
   This is both this project's own audit trail and a clean feed for the separate project that
   consumes `docs/wiki/` — it should never need to diff the whole tree to figure out what moved.

**If this run was closing out a stray progress file (Step 1a):** only offer to delete it after
every one of its findings has been traced to a resolution — already captured elsewhere, applied
in this run, or explicitly declined by the user. Do not delete on the assumption that "the main
finding is handled." Real precedent from this exact project: closing out one progress file missed
an entire unactioned wiki correction on the first pass, and closing out another required checking
every side-finding individually before it was actually safe to remove — treat that level of
verification as the required bar, not a thorough-if-you-feel-like-it option.

---

## Step 7 — Report

```
## Documentation report — <section name>

**Candidate facts found:** N (X routine-skip, Y change-signaling, Z unverified-source)
**Live checks run:** N (M confirmed existing text, K found a contradiction)
**Wiki changes applied:** N addition(s), N correction(s)
**Contradictions escalated (unresolved):** N
**Pipeline debt flagged:** N case(s) never grilled/audited
**Log entry:** appended to docs/wiki/log.md | not written (nothing applied)

### Applied
- [page] — added/corrected: ... (source: ...)

### Escalated — needs your judgment
- [page] — wiki says: "..." | verified fact says: "..." | reading 1: stale doc | reading 2: possible
  app change since — recommend: ...

### Pipeline debt
- [case id/title] — never grilled/audited, not used as a documentation source
```

If `$ARGUMENTS` was `all`, run Steps 1–6 per section, then prepend a cross-section summary before
the per-section reports — same shape as `/audit-section`'s `all` mode.

---

## Rules

- Never write to `docs/wiki/*.md` (or `docs/wiki/log.md`) without explicit approval — same bar as
  case creation.
- Never auto-resolve a wiki-vs-verified-fact contradiction. Always present both readings (stale
  doc / possible app regression) and let the user decide. No exceptions for "obvious" cases.
- A `not-tracked-by-repo` (or equivalent unverified) note never solely backs a wiki fact — corroborate,
  live-check, or flag as pipeline debt instead.
- Live-check mechanism is always a reused `/grill-section` Step 3 run against a synthetic
  case-shaped object — never invent new Playwright-driving instructions here.
- Every applied change gets a `docs/wiki/log.md` entry. No silent edits.
- Every drafted addition/correction is held to `migration-conventions.md` §0 before being
  proposed.
- This command does not know about, and must not guess at, how the separate consumer project
  reindexes `docs/wiki/`. Its job stops at a correct, logged, committed wiki.
- Don't delete a stray progress file until every one of its findings is individually traced to a
  resolution — see Step 6's real-precedent note.
