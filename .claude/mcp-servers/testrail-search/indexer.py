# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "chromadb>=0.6",
#   "certifi",
# ]
# ///

"""Index TestRail cases into ChromaDB for semantic search.

Incremental by default: reads `.last_indexed_testrail` (a cutoff = newest `updated_on` from
the last successful run, plus one second) and fetches only cases updated since
(`updated_after = cutoff`), across every suite in the project. TestRail's `updated_after`
is inclusive (>=), so the stored cutoff is `max(updated_on) + 1` — this prevents the newest
case being re-fetched on every run while still capturing anything genuinely newer. Comparing
against the server's own timestamp means a skewed host clock can never cause missed or
re-fetched cases. A failed or empty run leaves the previous value untouched (no gaps). Long
cases are split into multiple chunks sized to a token budget to keep them within the
embedder's window (best-effort; see chunk_document); chunk ids are `<case_id>` or
`<case_id>::<n>`.

Note: the cutoff is exact (no overlap), so a case edited in the same second as the newest
case but after that run's snapshot would not be re-fetched. Run `--full` periodically to
reconcile.

`updated_after` never reports deletions, so cases removed in TestRail go stale in the index.
The same applies to shared steps: editing a shared step does not bump `updated_on` on the
cases that reference it, so incremental runs won't re-inline the new text. Run a full rebuild
(`--full`) periodically to clear both kinds of drift — it builds into a temp collection and
swaps atomically, so a crash mid-rebuild leaves the live index intact.

Run:
    uv run .claude/mcp-servers/testrail-search/indexer.py            # incremental
    uv run .claude/mcp-servers/testrail-search/indexer.py --full     # full rebuild

Env (read from workspace .env or the environment):
    TESTRAIL_URL         e.g. https://yourcompany.testrail.io
    TESTRAIL_USERNAME    TestRail account email
    TESTRAIL_API_KEY     TestRail API key  (My Settings > API Keys)
    TESTRAIL_PROJECT_ID  numeric project id
    TESTRAIL_SUITE_ID    optional; pins a single suite (else all suites are synced)
    TESTRAIL_REQUEST_DELAY  optional; seconds to sleep after each successful API call
                            (default 0 = no throttle). Set e.g. 0.5 to be gentle on the
                            API and avoid the 429 rate limiter on large projects.
"""

import json
import os
import re
import ssl
import sys
import time
from base64 import b64encode
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import chromadb

# ── Paths ────────────────────────────────────────────────────────────────────

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CHROMA_DIR = HERE / "chroma_db"
SENTINEL = HERE / ".last_indexed_testrail"

COLLECTION = "testrail"
PAGE_LIMIT = 250          # TestRail caps get_cases at 250 per page
MAX_RETRIES = 5
UPSERT_BATCH = 100
# Chunk by an estimated token budget, NOT chars: MiniLM (Chroma's default embedder) silently
# truncates beyond 256 tokens, and a 1500-char chunk is ~375 tokens — so char-capped chunks
# were losing their tails from the vector. ~230 leaves headroom for [CLS]/[SEP] + the
# re-prepended header. BM25 still sees the full text either way.
MAX_CHUNK_TOKENS = 230
WHERE_IN_BATCH = 200      # cap ids per Chroma `$in` delete

# Fallbacks used when the API lookup is unavailable (graceful degradation).
_DEFAULT_PRIORITIES = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
_DEFAULT_TYPES = {
    1: "Acceptance", 2: "Accessibility", 3: "Automated", 4: "Compatibility",
    5: "Destructive", 6: "Functional", 7: "Other", 8: "Performance",
    9: "Regression", 10: "Security", 11: "Smoke & Sanity", 12: "Usability",
}

# Automation type is an instance-specific TestRail custom dropdown, so the real id->label
# map is loaded from get_case_fields at runtime. 0 is the conventional "not automated".
_DEFAULT_AUTOMATION = {0: "None"}

# ── SSL ──────────────────────────────────────────────────────────────────────

try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = ssl.create_default_context()


# ── .env loading ───────────────────────────────────────────────────────────────

def _load_dotenv() -> None:
    """Populate os.environ from workspace .env for direct `uv run` (the Makefile exports
    these already, but a bare run would otherwise see nothing). Never overrides a value
    already present in the environment."""
    env_file = WORKSPACE_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


# ── TestRail API client ─────────────────────────────────────────────────────────

class TestRail:
    def __init__(self, base_url: str, user: str, api_key: str, delay: float = 0.0):
        self.base = base_url.rstrip("/") + "/index.php?/api/v2/"
        self.delay = max(0.0, delay)   # seconds to pause after each successful call
        token = b64encode(f"{user}:{api_key}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    def get(self, endpoint: str):
        """GET an endpoint, retrying on 429/5xx with backoff. Raises RuntimeError on a
        hard failure so callers can choose to abort or fall back. `endpoint` is everything
        after the api/v2/ prefix, e.g. 'get_cases/3&suite_id=5&limit=250&offset=0'."""
        url = self.base + endpoint
        for attempt in range(MAX_RETRIES):
            req = Request(url, headers=self.headers, method="GET")
            try:
                with urlopen(req, context=_SSL, timeout=60) as resp:
                    data = json.loads(resp.read().decode())
                if self.delay:
                    time.sleep(self.delay)
                return data
            except HTTPError as e:
                if e.code == 429:
                    wait = int(e.headers.get("Retry-After", 2 ** attempt))
                    print(f"  rate limited (429), retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                if 500 <= e.code < 600 and attempt < MAX_RETRIES - 1:
                    wait = 2 ** attempt
                    print(f"  server error ({e.code}), retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                body = e.read().decode(errors="replace")[:500]
                raise RuntimeError(f"TestRail API error {e.code} on {endpoint}: {body}")
            except URLError as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"Network error reaching TestRail: {e.reason}")
        raise RuntimeError(f"Gave up on {endpoint} after {MAX_RETRIES} retries")

    def get_bulk(self, endpoint: str, key: str) -> list[dict]:
        """Fetch a paginated bulk endpoint, returning the full list. Handles both the
        newer paginated response ({offset, limit, size, _links, <key>: [...]}) and the
        older bare-array response."""
        results: list[dict] = []
        offset = 0
        while True:
            page = self.get(f"{endpoint}&limit={PAGE_LIMIT}&offset={offset}")
            if isinstance(page, list):           # legacy: bare array, no pagination
                results.extend(page)
                break
            items = page.get(key, [])
            results.extend(items)
            links = page.get("_links") or {}
            if links.get("next"):
                offset += PAGE_LIMIT
                continue
            if page.get("size", len(items)) < PAGE_LIMIT:
                break
            offset += PAGE_LIMIT
        return results


# ── Lookups & enrichment ────────────────────────────────────────────────────────

def _build_section_path_map(sections: list[dict]) -> dict[int, str]:
    """Map each section id to its full hierarchical path ('Parent > Child > Leaf')."""
    id_map = {s["id"]: s for s in sections}

    def resolve(section_id: Optional[int]) -> str:
        if section_id is None:
            return ""
        section = id_map.get(section_id)
        if not section:
            return ""
        parent = resolve(section.get("parent_id"))
        return f"{parent} > {section['name']}" if parent else section["name"]

    return {s["id"]: resolve(s["id"]) for s in sections}


def _load_priorities(tr: TestRail) -> dict[int, str]:
    try:
        return {p["id"]: p["name"] for p in tr.get_bulk("get_priorities", "priorities")}
    except RuntimeError:
        print("  warning: could not fetch priorities; using defaults")
        return dict(_DEFAULT_PRIORITIES)


def _load_case_types(tr: TestRail) -> dict[int, str]:
    try:
        return {t["id"]: t["name"] for t in tr.get_bulk("get_case_types", "case_types")}
    except RuntimeError:
        print("  warning: could not fetch case types; using defaults")
        return dict(_DEFAULT_TYPES)


def _load_automation_types(tr: TestRail) -> dict[int, str]:
    """Build the automation-type id->label map from the `custom_automation_type` case field.
    It's an instance-specific dropdown, so options are parsed at runtime; falls back to a
    minimal default if the field is absent or the lookup fails. (get_case_fields returns a
    bare array, not a paginated wrapper.)"""
    automation = dict(_DEFAULT_AUTOMATION)
    try:
        fields = tr.get("get_case_fields")
    except RuntimeError:
        print("  warning: could not fetch case fields; automation types limited to defaults")
        return automation
    if not isinstance(fields, list):
        return automation
    for field in fields:
        if field.get("system_name") != "custom_automation_type":
            continue
        configs = field.get("configs") or []
        items = (configs[0].get("options") or {}).get("items", "") if configs else ""
        for line in (items or "").splitlines():
            num, _, label = line.partition(",")
            if num.strip().isdigit() and label.strip():
                automation[int(num.strip())] = label.strip()
    return automation


_MISSING = object()


def _resolve_shared_steps(tr: "TestRail", case: dict, cache: dict) -> None:
    """TestRail Shared Steps: a `custom_steps_separated` entry can reference a shared step by
    `shared_step_id` with no inline `content`, which would otherwise index as a blank numbered
    step (content silently missing from both the vector and BM25 text). Resolve such entries
    via `get_shared_step` and inline the shared step's own separated steps. Fail-safe: any
    lookup error (or an instance/version without shared steps) leaves the case untouched —
    strictly no worse than before. Cached per run since shared steps are reused across cases.
    """
    steps = case.get("custom_steps_separated")
    if not isinstance(steps, list) or not steps:
        return
    resolved: list[dict] = []
    changed = False
    for step in steps:
        sid = step.get("shared_step_id") if isinstance(step, dict) else None
        if sid and not (step.get("content") or "").strip():
            shared = cache.get(sid, _MISSING)
            if shared is _MISSING:
                try:
                    shared = tr.get(f"get_shared_step/{sid}")
                except RuntimeError:
                    shared = None
                cache[sid] = shared
            sub = (shared or {}).get("custom_steps_separated") if isinstance(shared, dict) else None
            if sub:
                resolved.extend(sub)
                changed = True
                continue
        resolved.append(step)
    if changed:
        case["custom_steps_separated"] = resolved


def fetch_all_cases(tr: TestRail, project_id: str, pinned_suite: str, priorities: dict,
                    types: dict, automation: dict, updated_after: Optional[int]) -> list[dict]:
    """Fetch cases across every suite (or the pinned suite), optionally only those updated
    after `updated_after`, enriching each with suite name, full section path, priority
    name, and type name."""
    if pinned_suite:
        suites = [{"id": int(pinned_suite), "name": f"Suite {pinned_suite}"}]
        print(f"Using pinned suite {pinned_suite}")
    else:
        try:
            raw = tr.get_bulk(f"get_suites/{project_id}", "suites")
            suites = [s for s in raw if "id" in s]   # drop single-suite-mode error objects
        except RuntimeError:
            suites = []
        if not suites:
            # Single-suite-mode project: no suite_id in any call.
            suites = [{"id": None, "name": ""}]
        print(f"Found {len(suites)} suite(s)")

    after_q = f"&updated_after={updated_after}" if updated_after is not None else ""

    all_cases: list[dict] = []
    shared_cache: dict = {}   # shared_step_id -> resolved shared step (reused across cases)
    for suite in suites:
        sid = suite["id"]
        suite_name = suite.get("name", "")
        suite_q = f"&suite_id={sid}" if sid is not None else ""

        sections = tr.get_bulk(f"get_sections/{project_id}{suite_q}", "sections")
        section_paths = _build_section_path_map(sections)

        cases = tr.get_bulk(f"get_cases/{project_id}{suite_q}{after_q}", "cases")
        print(f"  suite '{suite_name or '(default)'}': {len(cases)} case(s)")

        for case in cases:
            case["_suite_name"] = suite_name
            case["_section_path"] = section_paths.get(case.get("section_id"), suite_name)
            case["_priority_name"] = priorities.get(case.get("priority_id"), "")
            case["_type_name"] = types.get(case.get("type_id"), "")
            case["_automation_name"] = automation.get(case.get("custom_automation_type"), "None")
            _resolve_shared_steps(tr, case, shared_cache)
        all_cases.extend(cases)

    return all_cases


# ── HTML → text ─────────────────────────────────────────────────────────────────

class _TextExtractor(HTMLParser):
    """Flatten TestRail rich-text HTML to readable plain text. Block tags become line
    breaks, list items get a '- ' prefix; entities are decoded automatically."""
    _BLOCK = {"p", "div", "br", "tr", "ul", "ol", "table",
              "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.parts.append("\n- ")
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self._BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def _html_to_text(value: Optional[str]) -> str:
    """Convert a possibly-HTML rich-text value to clean plain text. Plain strings (no tags
    or entities) pass through untouched; malformed HTML falls back to a tag-strip regex."""
    if not value:
        return ""
    if "<" not in value and "&" not in value:
        return value.strip()
    parser = _TextExtractor()
    try:
        parser.feed(value)
        parser.close()
        text = "".join(parser.parts)
    except Exception:
        text = re.sub(r"<[^>]+>", " ", value)
    text = text.replace("\xa0", " ")             # &nbsp; → regular space
    text = re.sub(r"[ \t]+\n", "\n", text)      # trailing space before newlines
    text = re.sub(r"\n{3,}", "\n\n", text)       # collapse runs of blank lines
    return text.strip()


# ── Case → document ───────────────────────────────────────────────────────────

def build_document(case: dict) -> tuple[str, dict]:
    """Render an enriched TestRail case into searchable text + Chroma metadata."""
    cid = case["id"]
    title = _html_to_text(case.get("title", ""))
    section = case.get("_section_path", "")
    suite = case.get("_suite_name", "")
    priority = case.get("_priority_name", "")
    ctype = case.get("_type_name", "")
    automation = case.get("_automation_name", "")
    refs = (case.get("refs") or "").strip()

    lines = [f"[Case C{cid}] {title}"]
    # Embed only high-signal context (suite + section path). Priority/Type/Automation are
    # near-constant in this instance (~99.9% one value), so embedding them only adds noise to
    # the vector; they're still kept as metadata for display, not embedded.
    meta_line = " | ".join(
        f"{k}: {v}" for k, v in (("Suite", suite), ("Section", section)) if v
    )
    if meta_line:
        lines.append(meta_line)
    if refs:
        lines.append(f"Refs: {refs}")

    preconds = _html_to_text(case.get("custom_preconds"))
    if preconds:
        lines.append(f"\nPreconditions:\n{preconds}")

    # Separated steps take precedence; fall back to the single text field.
    steps_sep = case.get("custom_steps_separated")
    if isinstance(steps_sep, list) and steps_sep:
        lines.append("\nSteps:")
        for i, step in enumerate(steps_sep, start=1):
            content = _html_to_text(step.get("content"))
            extra = _html_to_text(step.get("additional_info"))   # TestRail per-step extra notes
            expected = _html_to_text(step.get("expected"))
            if extra:
                content = f"{content}\n   {extra}" if content else extra
            lines.append(f"{i}. {content}")
            if expected:
                lines.append(f"   Expected: {expected}")
    else:
        steps = _html_to_text(case.get("custom_steps"))
        if steps:
            lines.append(f"\nSteps:\n{steps}")

    expected = _html_to_text(case.get("custom_expected"))
    if expected:
        lines.append(f"\nExpected Result:\n{expected}")

    metadata = {
        "case_id": cid,
        "title": title,
        "section": section,
        "suite": suite,
        "priority": priority,
        "type": ctype,
        "automation_type": automation or "None",
        "refs": refs,                       # comma-joined Jira keys — the cross-ref bridge
        "updated_on": int(case.get("updated_on") or 0),
        "milestone_id": int(case.get("milestone_id") or 0),
        "suite_id": int(case.get("suite_id") or 0),
        "section_id": int(case.get("section_id") or 0),
        "estimate": str(case.get("estimate") or ""),
    }
    return "\n".join(lines), metadata


def _est_tokens(text: str) -> int:
    """Conservative upper-bound estimate of MiniLM (WordPiece) tokens — no tokenizer dep.
    Biased to OVER-count (≈3 chars/token, or words×1.4, whichever is larger) so chunks stay
    safely under the 256-token window even for the id/number/punctuation-dense text in
    TestRail steps, which WordPiece splits aggressively. Over-counting only costs a few extra
    chunks; under-counting would silently truncate, so we err high."""
    if not text:
        return 0
    # CJK (and other non-spaced scripts) tokenize ~1 token/char, vs ~3 chars/token for Latin —
    # count those codepoints at 1 token each so non-Latin cases don't silently under-count and
    # truncate. The Latin remainder keeps the over-counting bias.
    cjk = sum(1 for ch in text if ord(ch) >= 0x3000)
    non_cjk = len(text) - cjk
    return int(cjk + max(non_cjk / 3.0, len(text.split()) * 1.4)) + 1


def _split_token_by_chars(token: str, budget: int) -> list[str]:
    """Last-resort split of a single over-budget token (long URL / JWT / base64 / minified
    JSON, or a run of CJK) on character boundaries. The char→token ratio is derived from the
    token itself (~3 chars/token for Latin, ~1 for CJK) so pieces stay within budget for any
    script; a trim loop guards against an over-optimistic estimate."""
    est = _est_tokens(token)
    if est <= budget:
        return [token]
    chars_per_tok = max(1.0, len(token) / est)            # ~1 for CJK, ~3 for Latin
    width = max(1, int((budget - 1) * chars_per_tok))
    out: list[str] = []
    i, n = 0, len(token)
    while i < n:
        piece = token[i:i + width]
        while len(piece) > 1 and _est_tokens(piece) > budget:
            piece = piece[:max(1, int(len(piece) * 0.8))]
        out.append(piece)
        i += len(piece)
    return out


def _split_line_to_budget(line: str, budget: int) -> list[str]:
    """Split a line that exceeds the token budget on word boundaries; a single word that is
    itself over budget is then hard-split on character boundaries. Best-effort: _est_tokens
    is a heuristic, so this targets the budget rather than guaranteeing it."""
    if _est_tokens(line) <= budget:
        return [line]
    out: list[str] = []
    cur: list[str] = []
    for w in line.split(" "):
        if _est_tokens(w) > budget:                 # no-space token larger than the budget
            if cur:
                out.append(" ".join(cur))
                cur = []
            out.extend(_split_token_by_chars(w, budget))
            continue
        cur.append(w)
        if len(cur) > 1 and _est_tokens(" ".join(cur)) > budget:
            cur.pop()
            out.append(" ".join(cur))
            cur = [w]
    if cur:
        out.append(" ".join(cur))
    return out


def chunk_document(text: str, section: str = "") -> list[str]:
    """Split a case document into pieces that aim to stay within MiniLM's 256-token window
    (the default embedder truncates silently beyond it). Splits at line boundaries; an
    identity header is re-prepended to every overflow piece so each chunk keeps its context,
    and an over-budget line is hard-split on word — then, if needed, character — boundaries.
    Best-effort (the token count is a heuristic), so it targets the budget rather than
    guaranteeing it. Chunk ids stay `<case_id>` / `<case_id>::<n>`.

    The re-prepended header folds the section path onto the single `[Case C…] title` line so
    multi-chunk cases keep their section context in every chunk's embedding (section is one of
    the two high-signal fields we embed). It stays one line + blank so the search server's
    reassembly (strip line 0 + blank) still recovers the original text exactly."""
    if _est_tokens(text) <= MAX_CHUNK_TOKENS:
        return [text]

    lines = text.split("\n")
    header = f"{lines[0]} — Section: {section}" if section else lines[0]
    # Never let the re-prepended header crowd out content: cap it at ~half the window so every
    # overflow chunk still has room for real text (deep section paths / very long titles would
    # otherwise floor piece_budget at 1 and truncate every chunk). Reassembly strips the header
    # structurally by chunk_index, so truncating it here is safe.
    max_header_chars = max(1, (MAX_CHUNK_TOKENS // 2) * 3)
    if _est_tokens(header) > MAX_CHUNK_TOKENS // 2:
        header = header[:max_header_chars]
    header_tok = _est_tokens(header) + 1
    # Pieces must leave room for the header (+ blank line) re-prepended to overflow chunks,
    # so split to a reduced budget — otherwise a single max-size piece plus the header would
    # push the assembled chunk back over the window.
    piece_budget = max(1, MAX_CHUNK_TOKENS - header_tok - 2)
    chunks: list[str] = []
    cur: list[str] = []
    cur_tok = 0
    for raw in lines:
        for piece in _split_line_to_budget(raw, piece_budget):
            ptok = _est_tokens(piece) + 1
            if cur and cur_tok + ptok > MAX_CHUNK_TOKENS:
                chunks.append("\n".join(cur))
                cur = [header, ""]
                cur_tok = header_tok + 1
            cur.append(piece)
            cur_tok += ptok
    if cur:
        chunks.append("\n".join(cur))
    return chunks


# ── Main ─────────────────────────────────────────────────────────────────────

def _require_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise SystemExit(f"Missing required env var: {name} (set it in workspace .env)")
    return val


def main() -> None:
    full = "--full" in sys.argv[1:]
    _load_dotenv()

    base_url = _require_env("TESTRAIL_URL")
    user = _require_env("TESTRAIL_USERNAME")
    api_key = _require_env("TESTRAIL_API_KEY")
    project_id = _require_env("TESTRAIL_PROJECT_ID")
    pinned_suite = os.environ.get("TESTRAIL_SUITE_ID", "").strip()

    # Incremental cutoff: TestRail server `updated_on` from the last successful run.
    last_indexed = None
    if not full and SENTINEL.exists():
        raw = SENTINEL.read_text(encoding="utf-8").strip()
        last_indexed = int(raw) if raw.isdigit() else None
    query_after = last_indexed

    request_delay = float(os.environ.get("TESTRAIL_REQUEST_DELAY", "0") or 0)
    tr = TestRail(base_url, user, api_key, delay=request_delay)

    print("Fetching lookup tables (priorities, case types, automation types)...")
    priorities = _load_priorities(tr)
    types = _load_case_types(tr)
    automation = _load_automation_types(tr)

    if query_after is not None:
        print(f"Incremental: fetching cases updated after {query_after}...")
    else:
        print("Full index: fetching all cases...")
    try:
        cases = fetch_all_cases(tr, project_id, pinned_suite, priorities, types, automation, query_after)
    except RuntimeError as e:
        raise SystemExit(f"Aborting — failed to fetch cases: {e}")
    print(f"Fetched {len(cases)} case(s) total")

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if not cases:
        print("No cases to index — index is up to date.")
        return

    # Atomic full rebuild: build into a temp collection and swap on success, so a crash
    # mid-rebuild leaves the live collection (and sentinel) untouched.
    target_name = COLLECTION + "__rebuild" if full else COLLECTION
    if full:
        try:
            client.delete_collection(target_name)
        except Exception:
            pass
    # Create with cosine space so the search server's 0-1 similarity (1 - dist/2) is a true
    # cosine score. Space is fixed at creation, so switching an existing L2 collection over
    # requires a --full rebuild. The metadata kwarg is ignored for an already-existing
    # collection (and we fall back if a Chroma build rejects it).
    try:
        collection = client.get_or_create_collection(
            name=target_name, metadata={"hnsw:space": "cosine"}
        )
    except Exception:
        collection = client.get_or_create_collection(name=target_name)

    # Build chunks. One case may expand to several chunks; ids are `<cid>` (single chunk)
    # or `<cid>::<n>` (multi). On incremental runs, clear any prior chunks for the changed
    # cases first so a case whose chunk count shrank doesn't leave orphans (migration-safe:
    # matches by case_id regardless of old id format).
    if not full:
        changed = [int(c["id"]) for c in cases]
        for i in range(0, len(changed), WHERE_IN_BATCH):
            collection.delete(where={"case_id": {"$in": changed[i: i + WHERE_IN_BATCH]}})

    ids, texts, metadatas = [], [], []
    max_updated = last_indexed or 0
    for case in cases:
        text, meta = build_document(case)
        max_updated = max(max_updated, meta["updated_on"])
        parts = chunk_document(text, meta.get("section", ""))
        for idx, part in enumerate(parts):
            cid = case["id"]
            ids.append(str(cid) if len(parts) == 1 else f"{cid}::{idx}")
            texts.append(part)
            metadatas.append({**meta, "chunk_index": idx})

    for i in range(0, len(ids), UPSERT_BATCH):
        collection.upsert(
            ids=ids[i: i + UPSERT_BATCH],
            documents=texts[i: i + UPSERT_BATCH],
            metadatas=metadatas[i: i + UPSERT_BATCH],
        )
        print(f"  upserted {min(i + UPSERT_BATCH, len(ids))}/{len(ids)} chunk(s)...")

    # Swap the freshly built collection into place (full rebuild only).
    if full:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
        collection.modify(name=COLLECTION)
        print(f"Swapped rebuilt collection into '{COLLECTION}'")

    # Success → advance the cutoff PAST the newest case we saw. TestRail's `updated_after`
    # is inclusive (>=), so storing max+1 stops the boundary case being re-fetched on every
    # run while still capturing anything genuinely newer next time.
    next_cutoff = max_updated + 1
    if max_updated > 0:
        SENTINEL.write_text(str(next_cutoff), encoding="utf-8")

    print(f"\nDone — {len(cases)} case(s) → {len(ids)} chunk(s); collection holds {collection.count()} total")
    print(f".last_indexed_testrail = {next_cutoff}")


if __name__ == "__main__":
    main()
