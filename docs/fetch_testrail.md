# `fetch_testrail.py` — TestRail CLI wrapper

`.claude/scripts/fetch_testrail.py` is a thin, single-purpose command-line wrapper around the
TestRail REST API v2. It is the mechanical backbone of the CookieYes Suite 6 → v2 migration
pipeline (`/fetch-section` → `/grill-section` → `/migrate-section`).

This document has two halves:

1. **[Narrative](#part-1--narrative-how-it-works)** — what the tool is, how it thinks, and how it composes into the migration pipeline.
2. **[Reference](#part-2--subcommand-reference)** — every subcommand, argument, and flag.

Followed by the **[change history](#change-history)** (initial commit → today) and **[known gaps](#known-gaps)**.

---

## Part 1 — Narrative: how it works

### Design philosophy

The tool follows one rule: **one invocation performs exactly one TestRail operation, then exits.**
There is no session, no local state, no interactive mode. This makes it trivially composable —
an orchestrating agent (or a shell script) runs it, reads the result, decides what to do next,
and runs it again.

Three consequences flow from that rule:

- **Output is split by channel.** Successful results go to **stdout as JSON** (machine-readable,
  pipeable to `jq`/`python`). Progress lines, warnings, and errors go to **stderr** (human-readable,
  prefixed `✓`/`✗`/`Warning:`). A caller can capture stdout cleanly without stderr noise.
- **Failures are typed via exit codes**, so an orchestrator can branch on *why* something failed
  without parsing stderr text (see [exit codes](#exit-codes)).
- **Retries are safe by construction.** Only idempotent operations are ever replayed
  (see [retry policy](#retry-policy)).

### Configuration

Credentials come from a `.env` file discovered by walking up from the current directory (or the
script's directory) looking for `.env`/`docker-compose.yml`:

```
TESTRAIL_URL       https://yourorg.testrail.io
TESTRAIL_USERNAME  qa-bot@yourorg.com
TESTRAIL_API_KEY   <API key from TestRail profile → API Keys>
```

The URL is forced to `https://` before any request. Credentials are checked before any
network call, so a misconfigured `.env` fails fast with a usage-level exit code.

### The request layer

`api_request()` is the single choke point for all HTTP. It sets JSON headers + Basic auth and
applies the retry policy below. Every subcommand handler builds a URL with `build_url()` and
calls `api_request()` — there is no HTTP anywhere else.

#### Retry policy

| Condition | Behaviour |
|---|---|
| `429` (rate limited) | Retried on **all** methods — the request was never processed. Honours `Retry-After`, else exponential backoff. |
| `5xx` / network / timeout | Retried on **GET only** (idempotent). |
| `POST` failure | **Never replayed** — surfaces a single clear failure so a write is never silently duplicated. |

#### Exit codes

```
0 ok · 1 generic · 2 usage/config · 3 auth (401/403) · 4 not-found (404)
5 rate-limited (429 exhausted) · 6 transient (network/timeout) · 7 server (5xx) · 8 local (file I/O or JSON)
```

### Path safety

Any subcommand that reads or writes a file (`--json-file`, `--merge-into`, `log-gap`'s ticket
directory) is **confined to the `ai-context/` directory** under the current working dir:

- Paths that resolve outside `ai-context/` are rejected.
- Symlinks are refused (no following links out of the sandbox).
- Input files are size-capped (`MAX_INPUT_BYTES`, 5 MB).
- Writes are **atomic** — written to a `.tmp` file then `os.replace()`d into place, so a crash
  mid-write never leaves a half-written draft.

### The draft-envelope translation layer

This is the conceptual heart of the tool and what makes it a *migration* tool rather than a raw
API client. The migration pipeline works with **draft JSON files** (`ai-context/draft-<slug>.json`)
in a human-friendly shape:

```jsonc
{
  "section": "Custom CSS",
  "suite_id": 16,
  "cases": [
    {
      "id": null,                       // filled in on publish
      "title": "[Cookie Banner] …",
      "preconditions": "…",             // → custom_preconds
      "steps": [{ "content": "…", "expected": "…" }],  // → custom_steps_separated
      "run_type": "smoke",              // → custom_case_test_run_type: 2
      "section_id": 1793,               // routing metadata (optional)
      "source_case_ids": [980, 1443],   // internal — stripped
      "grill_status": "fixed",          // internal — stripped
      "rewrite_notes": "…"              // internal — stripped
    }
  ]
}
```

When a command runs with `--from-draft`, `prepare_draft_case()` converts each case into a clean
TestRail payload:

- **Renames** draft field names to API names (`preconditions`→`custom_preconds`,
  `steps`→`custom_steps_separated`, `run_type`→`custom_case_test_run_type`) via `CASE_FIELD_MAP`,
  which also accepts legacy camelCase aliases.
- **Maps** `run_type` strings to integers via `RUN_TYPE_MAP` (`regression`→1, `smoke`→2).
- **Strips** internal-only fields (`DRAFT_STRIP_FIELDS`: `grill_status`, `source_case_ids`,
  `rewrite_notes`, `permission_flag`, `platform_flag`, `section_id`) so they never reach the API.
- **Defaults** `template_id` to `2` (the steps-separated template).

The draft file is the **single source of truth**. On publish, IDs are written back into it and it
is renamed `draft-*` → `cases-*` as the "published" signal.

### How it composes into the migration pipeline

```
/fetch-section   get-sections ─┐
                 get-cases-for-sections   → writes ai-context/draft-<slug>.json
                                          (Suite 6 read side)

/grill-section   (Playwright verifies the draft against the live QA app;
                  edits the draft in place)

/migrate-section get-sections (v2 tree)                 → decide placement
                 dedup-check  (per target section)      → catch existing coverage
                 add-section  (only if missing)         → create parents→children
                 batch-add-cases --dry-run              → confirm draft == intent
                 batch-add-cases --from-draft --write-back → publish, write IDs back,
                                                            rename draft-* → cases-*
```

A single `batch-add-cases` call can publish to multiple v2 sections at once: each case is routed
by its own `section_id`, and cases without one fall back to the positional `<default_section_id>`.

---

## Part 2 — Subcommand reference

Run the script with no arguments to print this list (`print_usage()` is the single source of
truth for syntax). All commands require the `.env` credentials except `log-gap`, which is local-only.

### Read / query

| Command | Purpose |
|---|---|
| `get-projects` | List all TestRail projects. |
| `get-suites <project_id>` | List suites in a project. |
| `get-sections <project_id> <suite_id>` | List/search the section tree. Flags below. |
| `get-cases <project_id> <suite_id>` | List cases (optionally in one section). |
| `get-cases-for-sections <project_id> <suite_id>` | Fetch + shape + dedupe cases across many sections. |
| `get-case-types [--map]` | Case types; `--map` emits `{name: id}`. |
| `get-case-fields [--required-only]` | Custom fields; `--required-only` emits required custom fields. |
| `get-priorities [--map]` | Priorities; `--map` emits `{name: id}`. |

**`get-sections` flags:**
- `--all` — fetch the whole paginated tree.
- `--compact` — reduce each section to `{id, name, parent_id, depth}`.
- `--match "kw1,kw2"` — any-keyword, case-insensitive name filter; attaches a `path`/`pathIds` breadcrumb.
- `--match-keywords "kw1,kw2"` — **ranked** filter: scores each section by how many keywords appear in its name, returns `score >= 1` best-first (use this to pick section IDs to feed `get-cases-for-sections`).
- `--section-id ID` — look up one section (with breadcrumb).
- `--limit N` / `--offset N` — raw pagination (default 250/0).

**`get-cases-for-sections` flags:**
- `--section-ids 1,2,3` — explicit section IDs (takes precedence over keyword matching).
- `--match-keywords "kw1,kw2"` — resolve section IDs automatically by name scoring (no need to call `get-sections` first).
- `--match "kw1,kw2"` — filter returned cases by title keyword.
- `--merge-into <path>` — write shaped cases to `.testRailTests` in an existing `ai-context/` JSON file (atomic).
- `--max-sections N` (default 20) / `--max-cases N` (default 150) — safety caps; **overflow is logged to stderr**, never silent.

Shapes each case to `{id, title, sectionId, steps}` (steps flattened to text) and dedupes by id.
Emits `casesTruncated`/`sectionsTruncated` flags so a caller knows whether to widen the caps.

### Create / update cases

| Command | Purpose |
|---|---|
| `add-case <section_id> <json_payload>` | Create one case from an inline JSON payload. |
| `batch-add-cases <default_section_id> --json-file <path>` | Create many cases from a file. Flags below. |
| `update-case <case_id> <json_payload>` | Update one case from an inline JSON payload (strips `id` from the body). |
| `batch-update-cases --json-file <path> [--from-draft]` | Update many cases; skips cases without an `id`. |

**`batch-add-cases` flags:**
- `--from-draft` — treat the file as a draft envelope (`{cases: [...]}`) or plain array; run each case through `prepare_draft_case()` (rename/map/strip/`template_id`).
- `--only-new` — skip cases that already carry a non-null `id` (safe to re-run after a partial publish).
- `--write-back` — after posting, patch returned IDs back into the draft file (matched **by position**), set `published_at`, and rename `draft-*`→`cases-*` once every case has an id. Requires an envelope file.
- `--dry-run` — **post nothing.** Print the exact payload + resolved target section per case. Use to confirm the on-disk draft matches intent before the real publish.
- **Per-case routing:** each case's own `section_id` overrides `<default_section_id>`; the `section_id` is routing metadata and is never sent in the body. Multi-section publishes print a per-section breakdown.

### Dedup

| Command | Purpose |
|---|---|
| `dedup-check <project_id> <suite_id> <default_section_id> --json-file <path> [--threshold N]` | Read-only. |

For each draft case, fetches the **live** cases in that case's target section (per-case `section_id`,
else `<default_section_id>`) and scores similarity (`0.6·title + 0.4·steps`, via `difflib`). Emits
per-case top-3 matches at/above `--threshold` (default `0.5`). Creates nothing. Interpretation:
`≈1.0` = duplicate (skip), `~0.5–0.8` = related-but-distinct (human decides), none = safe.

### Sections / runs / results

| Command | Purpose |
|---|---|
| `add-section <project_id> <suite_id> <name> <parent_id>` | Create a section under a parent. |
| `add-run <project_id> <suite_id> <name> <case_ids_csv>` | Create a run over specific case IDs (`include_all=false`). |
| `add-results <run_id> <json_payload>` | Post results; payload must be `{"results":[{"caseId":N,"statusId":N,...}]}`. |

### Utility

| Command | Purpose |
|---|---|
| `log-gap <description> --ticket <id> [--context ...] [--workaround python\|jq\|shell\|none]` | Append a capability-gap entry to `ai-context/<ticket>/qa/run-log.md`. Local-only, no credentials needed. |

---

## Change history

The script has evolved in three phases: an initial read-oriented client, a draft-aware publishing
layer, and this session's multi-section + safety additions.

### Phase 1 — Initial commit (`ff79ad7`, ~940 lines)

The foundation: a clean one-shot API client. Included the request layer (retry policy, exit codes),
path confinement, and these subcommands:

- **Read:** `get-projects`, `get-suites`, `get-sections` (with `--all`/`--compact`/`--match`/`--match-keywords`/`--section-id`), `get-cases`, `get-cases-for-sections`, `get-case-types`, `get-case-fields`, `get-priorities`.
- **Write:** `add-section`, `add-case`, `add-run`, `add-results`, and a **raw** `batch-add-cases <section_id> --json-file <path>` (arrays only — no draft awareness).
- **Utility:** `log-gap`.

At this stage the tool could *read* Suite 6 richly but had no concept of the draft format.

### Phase 2 — Draft publishing layer (`bff9b82`)

Turned the raw client into a migration tool. Added the whole draft-envelope translation layer and
the update path:

- `prepare_draft_case()` + `CASE_FIELD_MAP` draft field names + `RUN_TYPE_MAP` + `DRAFT_STRIP_FIELDS`.
- `batch-add-cases` flags `--from-draft`, `--only-new`, `--write-back` (with `draft-*`→`cases-*` rename).
- New subcommands `update-case` and `batch-update-cases`.
- **The `template_id=2` default** in `prepare_draft_case()` — the fix this commit is named for; before it, cases were created on the wrong template.

### Phase 3 — This session (multi-section + safety)

Motivated directly by friction hit while migrating the Custom CSS section. Changes (currently
uncommitted, +161/−30):

| Change | Why |
|---|---|
| **Per-case `section_id` routing** in `batch-add-cases` (+ `_resolve_target_section()` helper; `section_id` added to strip fields) | Publishing to multiple v2 sections previously required hand-writing temp files and manually merging IDs. Now one call routes each case; the positional arg is the fallback. |
| **`dedup-check` subcommand** | `testrail-search` indexes legacy Suite 6, not v2, so Step 5a dedup relied on a manual `get-cases` + eyeballing. This scores proposed cases against the live target section — no static index to go stale against a growing suite. |
| **`batch-add-cases --dry-run`** | After a `run_type` drifted between the draft and TestRail, needed a way to confirm the on-disk draft equals what will be posted *before* committing. |
| **Write-back now matches by position** (`zip(to_post, results)`) instead of by title | Title matching could cross-assign IDs when two cases shared a title — a latent bug, and higher-risk now that one call publishes many cases. |
| **Single-source usage** | The subcommand list was duplicated in the module docstring and `print_usage()`, forcing double-edits (and drift) on every new flag. The docstring now points to `print_usage()`. |

---

## Known gaps

Surfaced during code review; not yet fixed at time of writing.

1. **`template_id=2` leaks into updates.** `batch-update-cases --from-draft` calls
   `prepare_draft_case()`, whose `setdefault("template_id", 2)` is correct for *adds* but would
   silently flip a `template_id=1` case to `2` on update, potentially breaking step rendering.
   The default belongs only on the add path.
2. **`--threshold` is not range-checked.** `dedup-check` validates that `--threshold` parses as a
   float but not that it is within `[0, 1]`; `--threshold 5` passes and silently matches nothing.
3. **Minor:** `build_url()` uses a mutable default arg (`params={}`) — benign today (never
   mutated) but a footgun; `only_new` treats `id: 0` as new (harmless — TestRail never issues 0);
   `dedup-check` fetches a section's cases uncapped (fine for leaf sections).

> A workflow-backed high-effort code review was run over the script; reconcile its verified
> findings against this list.
