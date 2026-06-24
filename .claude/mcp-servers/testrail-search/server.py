# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "chromadb>=0.6",
#   "rank-bm25>=0.2",
# ]
# ///

"""TestRail search MCP server — hybrid semantic + keyword search over indexed TestRail cases.

Combines ChromaDB vector embeddings with BM25 keyword scoring, merged via Reciprocal Rank
Fusion. One case may be stored as several chunks (`<case_id>::<n>`); results are collapsed to
the best-matching chunk per case so each case appears once.

Search results carry a 0-1 `similarity` (semantic, from cosine distance) plus the fused
`relevance` used for ordering. Keyword-only (BM25) matches have `similarity: null`. The
index must be built with cosine space (the indexer does this) for the similarity bands in
the interpretation guide to be accurate — run a `--full` reindex once after upgrading.

Build the index first with:  uv run .claude/mcp-servers/testrail-search/indexer.py
"""

import json
import os
import re
from pathlib import Path
from typing import Any

import chromadb
from mcp.server.fastmcp import FastMCP
from rank_bm25 import BM25Okapi

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"
COLLECTION = "testrail"
RRF_K = 60
CANDIDATE_MULTIPLIER = 6   # base: fetch this many × top_k chunks/source before RRF merge.
                          # Token-sized chunks mean several chunks per case, so collapse-by-
                          # case can starve; _hybrid_search escalates this until it has top_k
                          # distinct cases (bounded by MAX_CANDIDATES).
MAX_CANDIDATES = 2000     # hard ceiling on the candidate pool for the escalation loop
QUERY_WINDOW_CHARS = 600  # ~200 tokens: keep each query under MiniLM's 256-token window
MAX_QUERY_WINDOWS = 8     # cap query fan-out for a very long proposed case (dedup)
DEFAULT_TOP_K = int(os.getenv("RAG_DEFAULT_TOP_K", "10"))
MAX_TOP_K = 20

mcp = FastMCP("testrail-search")

_client = None
_collection = None
_bm25: BM25Okapi | None = None
_bm25_metadatas: list[dict] | None = None
_bm25_docs: list[str] | None = None
_base_url: str | None = None
_index_sig: float | None = None


def _testrail_base_url() -> str:
    """Read TESTRAIL_URL from the environment or workspace .env (for building case
    links). Cached; returns '' when unavailable."""
    global _base_url
    if _base_url is not None:
        return _base_url
    val = os.environ.get("TESTRAIL_URL", "").strip()
    if not val:
        env_file = WORKSPACE_DIR / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("TESTRAIL_URL=") and "=" in line:
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    _base_url = val.rstrip("/")
    return _base_url


def _case_url(case_id: Any) -> str:
    base = _testrail_base_url()
    return f"{base}/index.php?/cases/view/{case_id}" if base else ""


def _get_collection():
    global _client, _collection
    if _collection is None:
        if _client is None:
            _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        # get_collection, NOT get_or_create: the server must never CREATE the collection. If it
        # ran before the indexer it would create it with Chroma's default L2 space, silently
        # breaking the cosine similarity math (uncorrectable without a --full rebuild). A missing
        # collection just means "not indexed yet" and is reported cleanly by _index_error.
        _collection = _client.get_collection(name=COLLECTION)
    return _collection


def _index_signature() -> float:
    """mtime of the index files — a cheap change detector for cache invalidation."""
    sig = 0.0
    for pth in (CHROMA_DIR / "chroma.sqlite3",
                Path(__file__).resolve().parent / ".last_indexed_testrail"):
        try:
            sig = max(sig, pth.stat().st_mtime)
        except OSError:
            pass
    return sig


def _maybe_refresh() -> None:
    """Drop the cached client/collection/BM25 if the index changed on disk (e.g. a reindex
    ran), so a long-lived server doesn't keep serving a stale snapshot. Re-instantiating the
    client reloads HNSW from disk, refreshing the vector AND BM25 halves together. NOTE: this
    only guards in-process staleness — Chroma is not safe for a concurrent writer while this
    server holds the store, so run reindexes when the server is not live."""
    global _index_sig, _client, _collection, _bm25, _bm25_docs, _bm25_metadatas
    sig = _index_signature()
    if _index_sig is None:
        _index_sig = sig
        return
    if sig != _index_sig:
        _index_sig = sig
        _client = _collection = None
        _bm25 = _bm25_docs = _bm25_metadatas = None


_GET_PAGE = 1000  # page the full-collection read; a single unbounded get() trips Chroma's
                  # SQLite variable cap on large collections (tens of thousands of chunks)


def _ensure_bm25() -> None:
    global _bm25, _bm25_metadatas, _bm25_docs
    if _bm25 is not None:
        return
    collection = _get_collection()
    total = collection.count()
    docs: list[str] = []
    metas: list[dict] = []
    offset = 0
    while offset < total:
        page = collection.get(limit=_GET_PAGE, offset=offset, include=["documents", "metadatas"])
        docs.extend(page["documents"])
        metas.extend(page["metadatas"])
        offset += _GET_PAGE
    _bm25_docs = docs
    _bm25_metadatas = metas
    tokenized = [re.sub(r"[^a-z0-9]", " ", doc.lower()).split() for doc in _bm25_docs]
    _bm25 = BM25Okapi(tokenized)


_REF_RE = re.compile(r"\[[Cc](\d+)\]")  # bracketed refs only, e.g. "go to [C123]" — matches the
                                       # documented convention and avoids phantoms from section
                                       # names ("C4 Tests"), URLs ("/c12345/"), "Version C3", etc.


def _extract_referenced_cases(text: str, own_id: Any) -> list[int]:
    """Pull bracketed `[Cxxx]` case ids mentioned in the text (e.g. a step says 'go to [C123]'
    instead of filling the preconditions field). Bracketed-only, to avoid phantom refs from
    section names, URLs, or version strings. Excludes the case's own id. Lets the agent follow
    a case's setup/context into the cases it references via get_test_case()."""
    try:
        own = int(own_id)
    except (TypeError, ValueError):
        own = None
    out: list[int] = []
    seen: set[int] = set()
    for m in _REF_RE.finditer(text or ""):
        cid = int(m.group(1))
        if cid != own and cid not in seen:
            seen.add(cid)
            out.append(cid)
    return out


def _hit_id(meta: dict) -> str:
    """Unique id for a chunk — case plus chunk index — so vector and BM25 hits align."""
    return f"{meta.get('case_id')}::{meta.get('chunk_index', 0)}"


def _to_hit(meta: dict, content: str, relevance: float, similarity: float | None = None) -> dict:
    return {
        "case_id": meta.get("case_id"),
        "title": meta.get("title", ""),
        "section": meta.get("section", ""),
        "suite": meta.get("suite", ""),
        "priority": meta.get("priority", ""),
        "type": meta.get("type", ""),
        "automation_type": meta.get("automation_type", ""),
        "refs": meta.get("refs", ""),
        "url": _case_url(meta.get("case_id")),
        "similarity": similarity,   # 0-1 semantic score; None for keyword-only (BM25) hits
        "relevance": relevance,     # fused score used for ordering
        "content": content,
        "referenced_cases": _extract_referenced_cases(content, meta.get("case_id")),
        "_id": _hit_id(meta),
    }


def _matches_where(meta: dict, where: dict | None) -> bool:
    """Python-side equivalent of the Chroma `where` filters we use, for filtering BM25 hits
    (BM25 runs over the cached docs, not through Chroma). Supports `{k: {"$eq": v}}` and
    the plain `{k: v}` shorthand."""
    if not where:
        return True
    for key, cond in where.items():
        val = meta.get(key)
        if isinstance(cond, dict):
            if "$eq" in cond and val != cond["$eq"]:
                return False
        elif val != cond:
            return False
    return True


def _vector_search(query: str, n: int, where: dict | None = None) -> list[dict]:
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        return []
    kwargs: dict = {
        "query_texts": [query],
        "n_results": min(n, count),
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        kwargs["where"] = where
    results = collection.query(**kwargs)
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # Cosine distance ∈ [0, 2] (the index is built with cosine space) → 0-1 similarity.
        sim = round(max(0.0, min(1.0, 1.0 - dist / 2.0)), 4)
        hits.append(_to_hit(meta, doc, sim, similarity=sim))
    return hits


def _bm25_search(query: str, n: int, where: dict | None = None) -> list[dict]:
    _ensure_bm25()
    tokens = re.sub(r"[^a-z0-9]", " ", query.lower()).split()
    if not tokens:
        return []
    scores = _bm25.get_scores(tokens)
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    hits = []
    for idx in order:
        if scores[idx] <= 0:
            break
        if not _matches_where(_bm25_metadatas[idx], where):
            continue
        hits.append(_to_hit(_bm25_metadatas[idx], _bm25_docs[idx], round(float(scores[idx]), 3)))
        if len(hits) >= n:
            break
    return hits


def _rrf_merge(vector_hits: list[dict], bm25_hits: list[dict]) -> list[dict]:
    """Reciprocal Rank Fusion: final_score = Σ 1/(RRF_K + rank) across both lists.
    Returns all merged chunk hits sorted by fused score (not yet truncated). The semantic
    `similarity` from the vector hit is preserved where present."""
    scores: dict[str, float] = {}
    id_to_hit: dict[str, dict] = {}

    for rank, hit in enumerate(vector_hits):
        did = hit["_id"]
        scores[did] = scores.get(did, 0.0) + 1.0 / (RRF_K + rank + 1)
        id_to_hit[did] = hit

    for rank, hit in enumerate(bm25_hits):
        did = hit["_id"]
        scores[did] = scores.get(did, 0.0) + 1.0 / (RRF_K + rank + 1)
        if did not in id_to_hit:
            id_to_hit[did] = hit

    sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)
    merged = []
    for did in sorted_ids:
        hit = dict(id_to_hit[did])
        hit["relevance"] = round(scores[did], 4)
        merged.append(hit)
    return merged


def _collapse_by_case(hits: list[dict], top_k: int) -> list[dict[str, Any]]:
    """Keep the best-scoring chunk per case so each case appears once, then take top_k."""
    if top_k <= 0:
        return []
    seen: set = set()
    out: list[dict] = []
    for hit in hits:
        cid = hit["case_id"]
        if cid in seen:
            continue
        seen.add(cid)
        out.append({k: v for k, v in hit.items() if k != "_id"})
        if len(out) >= top_k:
            break
    return out


def _hybrid_search(query: str, top_k: int, where: dict | None = None) -> list[dict[str, Any]]:
    """Vector + BM25, RRF-merged and collapsed to one entry per case.

    Because results are collapsed to one entry per case, the effective breadth is roughly
    candidates / avg_chunks_per_case — and token-sized chunks lower that denominator. So the
    candidate pool is escalated until we have top_k DISTINCT cases (or the collection / the
    MAX_CANDIDATES ceiling is exhausted), instead of a fixed multiple that could silently
    return fewer than top_k cases when one heavily-chunked case floods the pool."""
    collection = _get_collection()
    total = collection.count()
    if total == 0:
        return []
    cap = min(total, max(top_k * CANDIDATE_MULTIPLIER, MAX_CANDIDATES))
    fetch = min(top_k * CANDIDATE_MULTIPLIER, cap)
    results: list[dict[str, Any]] = []
    prev_pool = -1
    while True:
        merged = _rrf_merge(_vector_search(query, fetch, where),
                            _bm25_search(query, fetch, where))
        results = _collapse_by_case(merged, top_k)
        # Stop when we have enough distinct cases, hit the candidate ceiling, or the candidate
        # pool stopped growing — the last means both sources are exhausted (e.g. a narrow
        # section filter with few matching cases), so further escalation just re-does identical
        # work. This uses the RAW pool size, not the distinct-case count, so a single
        # heavily-chunked case dominating the pool cannot trip a premature stop.
        if len(results) >= top_k or fetch >= cap or len(merged) == prev_pool:
            return results
        prev_pool = len(merged)
        fetch = min(fetch * 4, cap)


def _reassemble(indexed_chunks: list[tuple[int, str]]) -> str:
    """Rejoin a case's chunks (each a (chunk_index, text) pair, in order) into its full
    document. Overflow chunks (chunk_index > 0) were stored with a re-prepended identity header
    line + blank line; strip those STRUCTURALLY by chunk_index — never by matching the header
    text, since legitimate step content can look exactly like a header (e.g. a step that pastes
    `[Case C555] note`), which a text match would silently eat."""
    out: list[str] = []
    for chunk_index, text in indexed_chunks:
        if chunk_index > 0:
            lines = text.split("\n")
            if len(lines) >= 2 and lines[1] == "":   # drop the re-prepended header + blank
                lines = lines[2:]
            text = "\n".join(lines)
        out.append(text)
    return "\n".join(out).strip()


# ── Interpretation guide (prepended to every search response) ─────────────────

BASE_PROMPT = """
## TestRail MCP — Interpretation Guide

Results come from a hybrid search index (semantic vector + BM25 keyword, merged with
Reciprocal Rank Fusion) over the indexed CookieYes TestRail cases. Results are collapsed to
one entry per case (best-matching chunk). Most results carry a `similarity` (0-1, semantic);
keyword-only matches have `similarity: null` — judge those by their `content`. `relevance`
is the fused ranking score, not a 0-1 confidence.

## Similarity bands (provisional — calibrate per index)
`similarity` is a 0-1 semantic score, normalised here as (1 + cosine)/2, so it floors near 0.5
and same-domain QA text tends to score high. Treat any absolute cutoff as rough; lean on the
RELATIVE ranking within the result set and on the actual `content`:
- clearly top-ranked with a visible score gap below it — strong match
- mid-pack, scores bunched together — review the content before acting
- bottom / no clear separation — loosely related; confirm before acting
Recalibrate once you've seen real scores for a few known queries.

## Preconditions
If a case shows `Preconditions: N/A` but step 1 is `Go to [Cxxxx]` / `Go to [cxxxx]`:
1. Take the referenced id from the result's `referenced_cases` (or parse `[C9718]`).
2. Call `get_test_case` with that case_id to fetch the full case.
3. Read its steps and expected results.
4. Derive the precondition from what that case sets up — e.g. it logs in and creates a
   resource → "Logged in as [role] with [resource] configured".
5. Label derived preconditions "Derived from C####", not as official TestRail text.
6. If that case also chains onward, repeat until you reach one with real setup context.

## Duplicate detection
Cases are likely duplicates if they share identical step content and differ only in:
- Section path (different plan tiers, environments, or signup flows)
- Role prefix (Admin, Editor, Account Owner, or project-equivalent roles)
- Test type or environment variant
Decision signal (weigh similarity AND content together, not a hard cutoff):
- SKIP — a clearly top-ranked existing case plainly covers the scenario; cite its id
- EXTEND — partial coverage; note exactly what the existing case misses
- CREATE — nothing in the results actually covers it

## Chained cases
Step references like `[C1234]` / `[c1234]` are dependencies — another case must run first.
They are surfaced in each result's `referenced_cases`; always call them out.

## Coverage gaps
After returning results, identify untested scenarios related to the query: negative / error
paths, role or permission variants, and edge cases (empty state, limits, concurrent actions,
invalid input). Return them as a structured list.

## Response rules
- Always cite case ids as C#### and include the result's `url` when referencing a case.
- Never fabricate steps or expected results — only use the retrieved `content`.
- If nothing in the results actually covers the query, say so explicitly.
- For duplicate analysis, group by identical step content, not just similar titles.
""".strip()


def _wrap(title: str, payload: Any) -> str:
    return f"{BASE_PROMPT}\n\n## {title}\n\n{json.dumps(payload, indent=2, ensure_ascii=False)}"


def _index_error() -> str | None:
    """Return a user-facing message if the index isn't usable, else None."""
    _maybe_refresh()
    if not CHROMA_DIR.exists():
        return ("Index not built. Run: "
                "uv run .claude/mcp-servers/testrail-search/indexer.py")
    try:
        if _get_collection().count() == 0:
            return "Index is empty. Run the testrail-search indexer to populate it."
    except Exception as e:
        return f"Index error: {e}. Run the testrail-search indexer to rebuild."
    return None


# ── MCP tools ─────────────────────────────────────────────────────────────────

@mcp.tool()
def search_test_cases(query: str, top_k: int = DEFAULT_TOP_K, section: str = "") -> str:
    """Search the indexed CookieYes TestRail cases for relevant test coverage.

    Hybrid semantic + keyword search (ChromaDB vector embeddings + BM25, merged with
    Reciprocal Rank Fusion). Results are collapsed to one entry per case. Use this to find
    existing coverage before authoring new tests, to see how a feature is currently tested,
    or to locate cases related to an area or Jira ticket.

    Priority / type / automation_type are returned on each result for your judgement but are
    deliberately NOT filter parameters: in this instance they're near-constant (~99.9%
    priority "Medium", only two `type` values, automation mostly unset), so filtering on them
    would silently return nothing and look like "no coverage". Use `section` to scope.

    Args:
        query: Natural language or keyword search (e.g. "cookie banner consent opt-out").
        top_k: Number of cases to return (default 10, max 20).
        section: Optional exact full section path, e.g. "Authentication > MFA > TOTP" (see the
                 `section` field on any result). If it matches nothing, the search falls back
                 to unfiltered so an over-narrow filter isn't mistaken for missing coverage.
    """
    err = _index_error()
    if err:
        return err
    try:
        k = min(top_k, MAX_TOP_K)
        where = {"section": {"$eq": section}} if section else None
        results = _hybrid_search(query, k, where)
        title = "Retrieved Test Cases"
        if where and not results:
            results = _hybrid_search(query, k, None)
            title = "Retrieved Test Cases (section filter matched nothing — showing unfiltered)"
        return _wrap(title, results)
    except Exception as e:
        return f"Search failed: {e}. Run the testrail-search indexer to rebuild the index."


def _query_windows(text: str) -> list[str]:
    """Split a long proposed-case query into windows that each fit under MiniLM's 256-token
    window. Embedding a whole long case as one query lets the model silently truncate it, so
    dedup would only 'see' the opening of the proposed case. Splits on line boundaries (and
    hard-splits any over-long line); capped to bound fan-out."""
    text = text.strip()
    if len(text) <= QUERY_WINDOW_CHARS:
        return [text]
    pieces: list[str] = []
    for line in text.split("\n"):
        while len(line) > QUERY_WINDOW_CHARS:
            pieces.append(line[:QUERY_WINDOW_CHARS])
            line = line[QUERY_WINDOW_CHARS:]
        pieces.append(line)
    windows: list[str] = []
    cur = ""
    for p in pieces:
        if cur and len(cur) + len(p) + 1 > QUERY_WINDOW_CHARS:
            windows.append(cur)
            cur = ""
            if len(windows) >= MAX_QUERY_WINDOWS:
                return windows
        cur = f"{cur}\n{p}" if cur else p
    if cur and len(windows) < MAX_QUERY_WINDOWS:
        windows.append(cur)
    return windows or [text[:QUERY_WINDOW_CHARS]]


@mcp.tool()
def find_similar_cases(case_text: str, threshold: float = 0.75, top_k: int = DEFAULT_TOP_K) -> str:
    """Detect near-duplicate test cases. Pass the full text of a proposed new case to check
    whether equivalent coverage already exists before creating it.

    The proposed case is searched in WINDOWS (not as one giant query) so a long case isn't
    truncated by the embedder; each case is ranked by its single best-matching chunk across the
    windows. Keyword-only matches have no similarity score and are excluded from the dupe set.

    Args:
        case_text: Full text of the proposed test case (title + steps + expected results).
        threshold: Minimum 0-1 similarity to flag as a duplicate (default 0.75). Similarity is
                   (1 + cosine)/2, so it floors near ~0.5 for unrelated cases — a threshold at or
                   below ~0.5 is meaningless (everything scores at least ~0.5); keep it above.
        top_k: Max duplicates to return (default 10, max 20).
    """
    err = _index_error()
    if err:
        return err
    try:
        # Rank each case by its HIGHEST-similarity chunk (not an RRF-fused chunk, which could be
        # a weak keyword match that hides a real duplicate), aggregated across all query windows.
        k = min(top_k, MAX_TOP_K)
        fetch = max(k * CANDIDATE_MULTIPLIER, 60)
        best: dict = {}
        for window in _query_windows(case_text):
            for h in _vector_search(window, fetch):
                cid = h["case_id"]
                sim = h.get("similarity") or 0.0
                if cid not in best or sim > best[cid]["similarity"]:
                    best[cid] = {key: val for key, val in h.items() if key != "_id"}
        dupes = sorted((h for h in best.values() if (h.get("similarity") or 0.0) >= threshold),
                       key=lambda h: h["similarity"], reverse=True)[:k]
        return _wrap("Similar Cases (possible duplicates)", dupes)
    except Exception as e:
        return f"Search failed: {e}. Run the testrail-search indexer to rebuild the index."


@mcp.tool()
def search_by_feature(query: str, section: str, top_k: int = DEFAULT_TOP_K) -> str:
    """Search scoped to a specific feature section in TestRail.

    Args:
        query: Natural language query.
        section: Exact full section path, e.g. "Authentication > MFA > TOTP". Must match the
                 case's stored section path exactly (see the `section` field in any result).
        top_k: Number of cases to return (default 10, max 20).
    """
    err = _index_error()
    if err:
        return err
    try:
        k = min(top_k, MAX_TOP_K)
        results = _hybrid_search(query, k, {"section": {"$eq": section}})
        if not results:
            results = _hybrid_search(query, k, None)
            return _wrap(f"No cases in section '{section}' (exact match) — showing unfiltered", results)
        return _wrap(f"Retrieved Test Cases in '{section}'", results)
    except Exception as e:
        return f"Search failed: {e}. Run the testrail-search indexer to rebuild the index."


@mcp.tool()
def search_by_jira_ticket(ticket: str, top_k: int = DEFAULT_TOP_K) -> str:
    """Find test cases linked to a specific Jira ticket. Combines an exact match on the
    `refs` field (cases explicitly linked to the ticket) with semantic search over content.

    Args:
        ticket: Jira ticket key, e.g. "CT1-412".
        top_k: Number of semantic results to return (default 10, max 20).
    """
    err = _index_error()
    if err:
        return err
    try:
        results = _hybrid_search(ticket, min(top_k, MAX_TOP_K))
        # Supplement with exact refs matches (exact token, case-insensitive). Chroma can't
        # match inside the delimited refs metadata, so scan the cached BM25 metadata instead.
        _ensure_bm25()
        seen = {r["case_id"] for r in results}
        t = ticket.strip().lower()
        exact: list[dict] = []
        for meta, doc in zip(_bm25_metadatas, _bm25_docs):
            cid = meta.get("case_id")
            if cid in seen:
                continue
            # Exact token match, not substring: refs is a delimited list ("CT1-4, CT1-41"), and a
            # substring test would wrongly match "CT1-4" against "CT1-41" / "CT1-412".
            refs_tokens = {x.strip().lower()
                           for x in re.split(r"[,;\s]+", meta.get("refs") or "") if x.strip()}
            if t in refs_tokens:
                seen.add(cid)
                hit = _to_hit(meta, doc, relevance=1.0)
                exact.append({k: v for k, v in hit.items() if k != "_id"})
        # Exact-ref matches first, then semantic hits.
        return _wrap("Retrieved Test Cases", exact + results)
    except Exception as e:
        return f"Search failed: {e}. Run the testrail-search indexer to rebuild the index."


@mcp.tool()
def get_test_case(case_id: int) -> dict[str, Any]:
    """Fetch a single TestRail case in full by its numeric id (the number in `C123`).

    Returns the complete reassembled case text (all steps + expected results), its metadata,
    a TestRail URL, and `referenced_cases` (other cases it points to). Use this to follow a
    `Cxxx` reference found in a search result, or whenever a case needs more context than the
    matched snippet — e.g. preconditions written as a 'go to [C123]' first step rather than in
    the preconditions field. Returns structured data (no interpretation guide) so it stays
    lean when called repeatedly while resolving a chain of references.

    Args:
        case_id: the numeric case id (e.g. 123 for C123)
    """
    _maybe_refresh()
    if not CHROMA_DIR.exists():
        return {"error": "Index not built",
                "hint": "Run `uv run .claude/mcp-servers/testrail-search/indexer.py` first"}
    try:
        collection = _get_collection()
        res = collection.get(where={"case_id": case_id}, include=["documents", "metadatas"])
        metas = res["metadatas"]
        docs = res["documents"]
        if not metas:
            return {"error": f"Case C{case_id} not found in the index",
                    "hint": "It may belong to an unindexed suite, or the index may be stale — "
                            "run the testrail-search indexer."}
        order = sorted(range(len(metas)), key=lambda i: metas[i].get("chunk_index", 0))
        content = _reassemble([(metas[i].get("chunk_index", 0), docs[i]) for i in order])
        m = metas[order[0]]
        return {
            "case_id": m.get("case_id"),
            "title": m.get("title", ""),
            "section": m.get("section", ""),
            "suite": m.get("suite", ""),
            "priority": m.get("priority", ""),
            "type": m.get("type", ""),
            "automation_type": m.get("automation_type", ""),
            "refs": m.get("refs", ""),
            "url": _case_url(case_id),
            "content": content,
            "referenced_cases": _extract_referenced_cases(content, case_id),
        }
    except Exception as e:
        return {"error": str(e),
                "hint": "Run the testrail-search indexer to rebuild the index"}


if __name__ == "__main__":
    mcp.run()
