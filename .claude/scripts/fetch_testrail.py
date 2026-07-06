#!/usr/bin/env python3
"""
Thin CLI wrapper around TestRail REST API v2.
Each invocation performs exactly one TestRail operation and exits.

Usage:  python fetch_testrail.py <subcommand> [args...]

Subcommands:
  get-projects
  get-suites       <project_id>
  get-sections     <project_id> <suite_id>   [--all] [--compact] [--match-keywords "kw1,kw2"] [--match "kw1,kw2"] [--limit N] [--offset N]
  get-cases        <project_id> <suite_id>   [--section-id ID] [--limit N] [--offset N]
  get-cases-for-sections <project_id> <suite_id> [--section-ids 1,2,3] [--match-keywords "kw1,kw2"] [--match "kw1,kw2"] [--merge-into <path>] [--max-sections N] [--max-cases N]
  get-case-types
  get-case-fields
  get-priorities
  batch-add-cases  <section_id> --json-file <path> [--from-draft] [--only-new] [--write-back]
  update-case      <case_id> <json_payload>
  batch-update-cases --json-file <path> [--from-draft]
  add-section      <project_id> <suite_id> <name> <parent_id>
  add-case         <section_id> <json_payload>
  add-run          <project_id> <suite_id> <name> <case_ids_csv>
  add-results      <run_id> <json_payload>
  log-gap          <description> --ticket <ticket-id> [--context ...] [--workaround python|jq|shell|none]

All successful output → stdout (JSON).
Progress + errors    → stderr.

Retry policy:
  429                     → retried on all methods (request was never processed)
  5xx / network / timeout → retried on GET only
  POST failures           → never replayed; single clear failure

Exit codes (so an orchestrator can route failures without parsing stderr):
  0 ok · 1 generic · 2 usage/config · 3 auth (401/403) · 4 not-found (404)
  5 rate-limited (429 exhausted) · 6 transient (network/timeout) · 7 server (5xx)
  8 local (file I/O or JSON)

Required env vars (in .env):
  TESTRAIL_URL       https://yourorg.testrail.io
  TESTRAIL_USERNAME  qa-bot@yourorg.com
  TESTRAIL_API_KEY   API key from TestRail profile → API Keys
"""

import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

# ── Exit codes ───────────────────────────────────────────────────────────────────
EXIT_OK           = 0
EXIT_GENERIC      = 1
EXIT_USAGE        = 2
EXIT_AUTH         = 3
EXIT_NOT_FOUND    = 4
EXIT_RATE_LIMITED = 5
EXIT_TRANSIENT    = 6
EXIT_SERVER       = 7
EXIT_LOCAL        = 8

# ── Path safety ──────────────────────────────────────────────────────────────────
ARTIFACT_ROOT   = "ai-context"
MAX_INPUT_BYTES = 5 * 1024 * 1024

REQUEST_TIMEOUT = 30  # seconds


# ── Env ────────────────────────────────────────────────────────────────────────

def load_env(env_path: str) -> None:
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            eq = line.index("=")
            k = line[:eq].strip()
            v = line[eq + 1:].strip().strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v


def find_workspace_root() -> str:
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    for start in [os.getcwd(), script_dir]:
        candidate = start
        for _ in range(6):
            if os.path.exists(os.path.join(candidate, ".env")) or \
               os.path.exists(os.path.join(candidate, "docker-compose.yml")):
                return candidate
            parent = os.path.dirname(candidate)
            if parent == candidate:
                break
            candidate = parent
    return os.path.realpath(os.path.join(script_dir, "..", ".."))


# ── Path safety ──────────────────────────────────────────────────────────────────

def assert_safe_segment(value: str, label: str) -> None:
    if not re.match(r'^[A-Za-z0-9_-]+$', value):
        stderr(f"Error: {label} must match /^[A-Za-z0-9_-]+$/ (got {json.dumps(value)})")
        sys.exit(EXIT_USAGE)


def confine_to_artifact_root(user_path: str, label: str, must_exist: bool) -> str:
    if "\0" in user_path:
        stderr(f"Error: {label} contains a null byte")
        sys.exit(EXIT_USAGE)
    root     = os.path.realpath(os.path.join(os.getcwd(), ARTIFACT_ROOT))
    resolved = os.path.realpath(os.path.join(os.getcwd(), user_path))
    if resolved != root and not resolved.startswith(root + os.sep):
        stderr(f"Error: {label} must resolve inside {ARTIFACT_ROOT}/ (got {json.dumps(user_path)})")
        sys.exit(EXIT_USAGE)
    if os.path.exists(resolved):
        if os.path.islink(resolved):
            stderr(f"Error: {label} is a symlink; refusing to follow it ({json.dumps(user_path)})")
            sys.exit(EXIT_USAGE)
    elif must_exist:
        stderr(f"Error: file not found: {user_path}")
        sys.exit(EXIT_LOCAL)
    return resolved


def assert_file_size_ok(file_path: str, label: str) -> None:
    size = os.path.getsize(file_path)
    if size > MAX_INPUT_BYTES:
        stderr(f"Error: {label} is {size} bytes; exceeds the {MAX_INPUT_BYTES}-byte limit")
        sys.exit(EXIT_LOCAL)


# ── HTTP ───────────────────────────────────────────────────────────────────────

def build_auth(username: str, api_key: str) -> str:
    token = base64.b64encode(f"{username}:{api_key}".encode()).decode()
    return f"Basic {token}"


def build_base_url(testrail_url: str) -> str:
    return testrail_url.rstrip("/") + "/index.php?/api/v2"


def validate_url(url: str) -> None:
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https":
            stderr(f"Blocked: only https:// URLs are allowed (got {parsed.scheme}:)")
            sys.exit(EXIT_USAGE)
    except Exception:
        stderr(f"Blocked: invalid URL {json.dumps(url)}")
        sys.exit(EXIT_USAGE)


def build_url(base: str, endpoint_path: str, params: dict[str, Any] = {}) -> str:
    url = f"{base}/{endpoint_path}"
    if params:
        query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url += "&" + query
    return url


def api_request(method: str, url: str, auth_header: str, body: Any = None, retries: int = 3) -> Any:
    idempotent = method.upper() == "GET"

    for attempt in range(retries + 1):
        req = urllib.request.Request(url, method=method)
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", auth_header)

        data: bytes | None = None
        if body is not None:
            data = json.dumps(body).encode()

        try:
            with urllib.request.urlopen(req, data=data, timeout=REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            status = e.code
            if status == 429:
                if attempt < retries:
                    retry_after = e.headers.get("retry-after", "")
                    try:
                        delay = int(retry_after)
                    except (ValueError, TypeError):
                        delay = 2 ** (attempt + 1)
                    stderr(f"Rate limited (429). Retrying in {delay}s… (attempt {attempt + 1}/{retries})")
                    time.sleep(delay)
                    continue
                stderr(f"TestRail API error 429 — rate limit exceeded after {retries} retries")
                sys.exit(EXIT_RATE_LIMITED)

            if 500 <= status <= 599 and idempotent and attempt < retries:
                delay = 2 ** (attempt + 1)
                stderr(f"Server error {status}. Retrying in {delay}s… (attempt {attempt + 1}/{retries})")
                time.sleep(delay)
                continue

            try:
                detail = e.read().decode(errors="replace")
            except Exception:
                detail = ""
            detail = " ".join(detail.split())[:500]

            if status == 401:
                stderr("TestRail API error 401 — invalid credentials. Check TESTRAIL_USERNAME and TESTRAIL_API_KEY in .env")
                sys.exit(EXIT_AUTH)
            elif status == 403:
                stderr("TestRail API error 403 — access denied. Check that the TestRail account has project access")
                sys.exit(EXIT_AUTH)
            elif status == 404:
                stderr("TestRail API error 404 — not found. Check the project/suite/section/run ID")
                sys.exit(EXIT_NOT_FOUND)
            elif status >= 500:
                stderr(f"TestRail API error {status} {method} {url}\n{detail}")
                sys.exit(EXIT_SERVER)
            else:
                stderr(f"TestRail API error {status} {method} {url}\n{detail}")
                sys.exit(EXIT_GENERIC)

        except (urllib.error.URLError, TimeoutError, OSError) as e:
            reason = str(e)
            if idempotent and attempt < retries:
                delay = 2 ** (attempt + 1)
                stderr(f"Network error ({reason}). Retrying in {delay}s… (attempt {attempt + 1}/{retries})")
                time.sleep(delay)
                continue
            stderr(f"TestRail request failed — {method} {url}\n{reason}")
            sys.exit(EXIT_TRANSIENT)

    sys.exit(EXIT_GENERIC)


# ── Output helpers ─────────────────────────────────────────────────────────────

def out(data: Any) -> None:
    sys.stdout.write(json.dumps(data, indent=2) + "\n")


def stderr(msg: str) -> None:
    sys.stderr.write(msg + "\n")


# ── Arg parsing ────────────────────────────────────────────────────────────────

def parse_args(argv: list[str]) -> tuple[list[str], dict[str, str]]:
    positional: list[str] = []
    flags: dict[str, str] = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                flags[key] = "true"
            else:
                i += 1
                flags[key] = argv[i]
        else:
            positional.append(argv[i])
        i += 1
    return positional, flags


def require_positional(pos: list[str], count: int, usage: str) -> None:
    if len(pos) < count:
        stderr(f"Usage: python fetch_testrail.py {usage}")
        sys.exit(EXIT_USAGE)


def to_int(value: str, name: str) -> int:
    try:
        return int(value)
    except ValueError:
        stderr(f"Error: {name} must be an integer, got {json.dumps(value)}")
        sys.exit(EXIT_USAGE)


def parse_json(raw: str, context: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        stderr(f"Error: invalid JSON for {context}: {e}")
        sys.exit(EXIT_LOCAL)


# ── Field translation ──────────────────────────────────────────────────────────

CASE_FIELD_MAP: dict[str, str] = {
    # camelCase API aliases (legacy payload format)
    "typeId":               "type_id",
    "priorityId":           "priority_id",
    "templateId":           "template_id",
    "milestoneId":          "milestone_id",
    "customPreconds":       "custom_preconds",
    "customPrerequisites":  "custom_preconds",
    "customStepsSeparated": "custom_steps_separated",
    "customSteps":          "custom_steps",
    "customExpected":       "custom_expected",
    "customRunType":        "custom_case_test_run_type",
    "customAutomationType": "custom_automation_type",
    # draft format field names
    "preconditions":        "custom_preconds",
    "steps":                "custom_steps_separated",
    "run_type":             "custom_case_test_run_type",
}

# Maps draft run_type strings to TestRail integer values
RUN_TYPE_MAP: dict[str, int] = {
    "regression": 1,
    "smoke":      2,
}

# Draft-only fields that must be stripped before POSTing to TestRail
DRAFT_STRIP_FIELDS = frozenset({
    "grill_status", "source_case_ids", "rewrite_notes",
    "permission_flag", "platform_flag",
})

RESULT_FIELD_MAP: dict[str, str] = {
    "caseId":       "case_id",
    "statusId":     "status_id",
    "assignedtoId": "assignedto_id",
}


def translate_case_fields(payload: dict[str, Any]) -> dict[str, Any]:
    return {CASE_FIELD_MAP.get(k, k): v for k, v in payload.items()}


def translate_result_fields(result: dict[str, Any]) -> dict[str, Any]:
    return {RESULT_FIELD_MAP.get(k, k): v for k, v in result.items()}


def prepare_draft_case(c: dict[str, Any]) -> dict[str, Any]:
    """Translate a draft-format case into a clean API payload.

    Strips internal-only fields, maps draft field names to API names,
    and converts run_type strings ("regression", "smoke") to integers.
    Safe to call on both draft-format and legacy camelCase payloads.
    """
    cleaned    = {k: v for k, v in c.items() if k not in DRAFT_STRIP_FIELDS and k != "id"}
    translated = translate_case_fields(cleaned)
    rt = translated.get("custom_case_test_run_type")
    if isinstance(rt, str):
        translated["custom_case_test_run_type"] = RUN_TYPE_MAP.get(rt, rt)
    translated.setdefault("template_id", 2)
    return translated


# ── Subcommand handlers ────────────────────────────────────────────────────────

def get_projects(base: str, auth: str) -> None:
    data = api_request("GET", build_url(base, "get_projects"), auth)
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ get-projects: {count} project(s)")


def get_suites(project_id: int, base: str, auth: str) -> None:
    data = api_request("GET", build_url(base, f"get_suites/{project_id}"), auth)
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ get-suites: {count} suite(s)")


def to_compact(section: dict[str, Any]) -> dict[str, Any]:
    return {
        "id":        section.get("id"),
        "name":      section.get("name"),
        "parent_id": section.get("parent_id"),
        "depth":     section.get("depth"),
    }


def flatten_steps(c: dict[str, Any]) -> str:
    separated = c.get("custom_steps_separated")
    if isinstance(separated, list) and separated:
        lines = []
        for i, raw in enumerate(separated):
            step     = raw if isinstance(raw, dict) else {}
            content  = str(step.get("content") or "").strip()
            expected = str(step.get("expected") or "").strip()
            line     = f"{i + 1}. {content}"
            lines.append(f"{line} → {expected}" if expected else line)
        return "\n".join(lines)
    custom_steps = c.get("custom_steps")
    if isinstance(custom_steps, str):
        return custom_steps.strip()
    return ""


def to_shaped_case(c: dict[str, Any]) -> dict[str, Any]:
    return {
        "id":        c.get("id"),
        "title":     c.get("title"),
        "sectionId": c.get("section_id"),
        "steps":     flatten_steps(c),
    }


def score_sections(
    sections: list[dict[str, Any]], keywords: list[str]
) -> list[dict[str, Any]]:
    """Score sections by keyword count in name; return score>=1 entries ordered best-first with 'score' added."""
    scored = []
    for s in sections:
        name_lower = str(s.get("name") or "").lower()
        score = sum(1 for k in keywords if k in name_lower)
        if score >= 1:
            entry = dict(s)
            entry["score"] = score
            scored.append(entry)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def fetch_all_sections_raw(
    project_id: int, suite_id: int, base: str, auth: str
) -> tuple[list[dict[str, Any]], bool]:
    MAX_PAGES     = 100
    current_offset = 0
    page_count     = 0
    has_more       = True
    sections: list[dict[str, Any]] = []

    while page_count < MAX_PAGES:
        page_count += 1
        params = {"suite_id": suite_id, "limit": 250, "offset": current_offset}
        data   = api_request("GET", build_url(base, f"get_sections/{project_id}", params), auth)
        page   = data.get("sections", []) if isinstance(data, dict) else []
        sections.extend(page)
        if not (isinstance(data, dict) and data.get("_links", {}).get("next")) or not page:
            has_more = False
            break
        current_offset += 250

    truncated = has_more
    if truncated:
        stderr(f"Warning: reached max pages ({MAX_PAGES}) for get-sections; results may be incomplete")
    return sections, truncated


def build_section_path(
    section: dict[str, Any],
    by_id: dict[Any, dict[str, Any]],
) -> dict[str, Any]:
    names: list[str] = []
    ids:   list[Any] = []
    seen:  set[Any]  = set()
    cur: dict[str, Any] | None = section

    while cur and cur.get("id") not in seen:
        seen.add(cur["id"])
        names.append(str(cur.get("name") or ""))
        ids.append(cur["id"])
        pid = cur.get("parent_id")
        cur = by_id.get(pid) if pid is not None else None

    names.reverse()
    ids.reverse()
    return {"path": " > ".join(names), "pathIds": ids}


def get_sections(
    project_id: int, suite_id: int,
    limit: int, offset: int,
    all_pages: bool,
    compact: bool,
    match: list[str],
    match_keywords: list[str],
    section_id: int | None,
    base: str, auth: str,
) -> None:
    if match_keywords:
        sections, truncated = fetch_all_sections_raw(project_id, suite_id, base, auth)
        by_id = {s["id"]: s for s in sections}

        def shape_kw(s: dict[str, Any]) -> dict[str, Any]:
            result = to_compact(s) if compact else dict(s)
            result.update(build_section_path(s, by_id))
            return result

        scored = score_sections([shape_kw(s) for s in sections], match_keywords)
        out({"sections": scored, "count": len(scored), "truncated": truncated})
        stderr(f"✓ get-sections --match-keywords: {len(scored)} of {len(sections)} section(s) matched (score >= 1), ordered best-first")
        return

    if section_id is not None or match:
        sections, truncated = fetch_all_sections_raw(project_id, suite_id, base, auth)
        by_id = {s["id"]: s for s in sections}

        def shape(s: dict[str, Any]) -> dict[str, Any]:
            result = to_compact(s) if compact else dict(s)
            result.update(build_section_path(s, by_id))
            return result

        if section_id is not None:
            found = by_id.get(section_id)
            if not found:
                out({"section": None, "found": False})
                stderr(f"✗ get-sections --section-id {section_id}: not found in project {project_id} / suite {suite_id}")
            else:
                out({"section": shape(found), "found": True})
                stderr(f"✓ get-sections --section-id {section_id}: found")
            return

        keywords = [k.lower() for k in match]
        matched  = [
            shape(s) for s in sections
            if any(k in str(s.get("name") or "").lower() for k in keywords)
        ]
        out({"sections": matched, "count": len(matched), "truncated": truncated})
        stderr(f"✓ get-sections --match: {len(matched)} of {len(sections)} section(s) matched")
        return

    if all_pages:
        sections, truncated = fetch_all_sections_raw(project_id, suite_id, base, auth)
        shaped = [to_compact(s) for s in sections] if compact else sections
        out({"sections": shaped, "truncated": truncated, "_links": {"next": "truncated" if truncated else None}})
        suffix = " (TRUNCATED — hit page cap)" if truncated else ""
        stderr(f"✓ get-sections --all: {len(shaped)} section(s) total{suffix}")
    else:
        params = {"suite_id": suite_id, "limit": limit, "offset": offset}
        data   = api_request("GET", build_url(base, f"get_sections/{project_id}", params), auth)
        page   = data.get("sections", []) if isinstance(data, dict) else []
        result = {**data, "sections": [to_compact(s) for s in page]} if compact else data
        out(result)
        stderr(f"✓ get-sections: {len(page)} section(s) (offset={offset})")


def get_cases(
    project_id: int, suite_id: int,
    section_id: int | None, limit: int, offset: int,
    base: str, auth: str,
) -> None:
    params: dict[str, int] = {"suite_id": suite_id, "limit": limit, "offset": offset}
    if section_id is not None:
        params["section_id"] = section_id
    data  = api_request("GET", build_url(base, f"get_cases/{project_id}", params), auth)
    out(data)
    cases = data.get("cases", []) if isinstance(data, dict) else data
    count = len(cases) if isinstance(cases, list) else "?"
    stderr(f"✓ get-cases: {count} case(s) (offset={offset})")


def fetch_all_cases(
    project_id: int, suite_id: int, section_id: int | None,
    base: str, auth: str,
) -> tuple[list[dict[str, Any]], bool]:
    MAX_PAGES = 100
    PAGE      = 250
    cases: list[dict[str, Any]] = []
    offset    = 0
    page_count = 0
    has_more   = True

    while page_count < MAX_PAGES:
        page_count += 1
        params: dict[str, int] = {"suite_id": suite_id, "limit": PAGE, "offset": offset}
        if section_id is not None:
            params["section_id"] = section_id
        data    = api_request("GET", build_url(base, f"get_cases/{project_id}", params), auth)
        is_bulk = isinstance(data, dict) and not isinstance(data, list)
        page: list[dict[str, Any]]
        if isinstance(data, list):
            page = data
        elif isinstance(data, dict) and isinstance(data.get("cases"), list):
            page = data["cases"]
        else:
            page = []
        cases.extend(page)
        has_next = bool(data.get("_links", {}).get("next")) if is_bulk else len(page) == PAGE
        if not has_next or len(page) < PAGE:
            has_more = False
            break
        offset += PAGE

    truncated = has_more
    if truncated:
        stderr(f"Warning: reached max pages ({MAX_PAGES}) for section {section_id if section_id is not None else 'ALL'}; results may be incomplete")
    return cases, truncated


def get_cases_for_sections(
    project_id: int, suite_id: int,
    section_ids: list[int], match: list[str], merge_into: str | None,
    max_sections: int, max_cases: int,
    match_keywords: list[str],
    base: str, auth: str,
) -> None:
    if match_keywords and not section_ids:
        all_sections, _ = fetch_all_sections_raw(project_id, suite_id, base, auth)
        scored = score_sections(all_sections, match_keywords)
        section_ids = [s["id"] for s in scored]
        stderr(f"✓ --match-keywords: {len(section_ids)} of {len(all_sections)} section(s) matched {match_keywords}, ordered best-first")

    sections_truncated = False
    ids = section_ids
    if len(ids) > max_sections:
        stderr(f"Warning: {len(ids)} section(s) requested; capping to --max-sections {max_sections} (dropped {len(ids) - max_sections})")
        ids = ids[:max_sections]
        sections_truncated = True

    sources: list[int | None] = ids if ids else [None]
    raw: list[dict[str, Any]] = []
    paging_truncated = False

    for sid in sources:
        page, truncated = fetch_all_cases(project_id, suite_id, sid, base, auth)
        if truncated:
            paging_truncated = True
        label = sid if sid is not None else "ALL"
        suffix = " (TRUNCATED — hit page cap)" if truncated else ""
        stderr(f"✓ section {label}: {len(page)} case(s){suffix}")
        raw.extend(page)

    keywords = [k.lower() for k in match if k]
    filtered = [
        c for c in raw
        if not keywords or any(k in str(c.get("title") or "").lower() for k in keywords)
    ]

    by_id: dict[Any, dict[str, Any]] = {}
    for c in filtered:
        by_id[c.get("id")] = c
    shaped = [to_shaped_case(c) for c in by_id.values()]

    cases_truncated = paging_truncated
    if len(shaped) > max_cases:
        stderr(f"Warning: {len(shaped)} case(s) matched; capping to --max-cases {max_cases} (dropped {len(shaped) - max_cases})")
        shaped = shaped[:max_cases]
        cases_truncated = True

    if merge_into:
        existing: dict[str, Any] = {}
        if os.path.exists(merge_into):
            assert_file_size_ok(merge_into, "--merge-into")
            existing = parse_json(open(merge_into).read(), f"merge-into {merge_into}")
        existing["testRailTests"] = shaped
        tmp = merge_into + ".tmp"
        with open(tmp, "w") as f:
            f.write(json.dumps(existing, indent=2) + "\n")
        os.replace(tmp, merge_into)
        out({"written": merge_into, "count": len(shaped), "casesTruncated": cases_truncated, "sectionsTruncated": sections_truncated})
        stderr(f"✓ get-cases-for-sections: merged {len(shaped)} case(s) into {merge_into}")
    else:
        out({"cases": shaped, "count": len(shaped), "casesTruncated": cases_truncated, "sectionsTruncated": sections_truncated})
        stderr(f"✓ get-cases-for-sections: {len(shaped)} case(s)")


def to_name_id_map(data: Any) -> dict[str, Any]:
    arr = data if isinstance(data, list) else []
    return {str(e["name"]): e.get("id") for e in arr if isinstance(e, dict) and e.get("name") is not None}


def get_case_types(as_map: bool, base: str, auth: str) -> None:
    data = api_request("GET", build_url(base, "get_case_types"), auth)
    if as_map:
        m = to_name_id_map(data)
        out(m)
        stderr(f"✓ get-case-types --map: {len(m)} type(s)")
        return
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ get-case-types: {count} type(s)")


def get_case_fields(required_only: bool, base: str, auth: str) -> None:
    data = api_request("GET", build_url(base, "get_case_fields"), auth)
    if required_only:
        fields = data if isinstance(data, list) else []
        required = [
            {"system_name": f.get("system_name"), "label": f.get("label"), "type_id": f.get("type_id")}
            for f in fields
            if isinstance(f, dict)
            and str(f.get("system_name") or "").startswith("custom_")
            and isinstance(f.get("configs"), list)
            and any(
                (c.get("options") or {}).get("is_required")
                for c in f["configs"]
                if isinstance(c, dict)
            )
        ]
        out({"requiredFields": required, "count": len(required)})
        stderr(f"✓ get-case-fields --required-only: {len(required)} required custom field(s)")
        return
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ get-case-fields: {count} field(s)")


def get_priorities(as_map: bool, base: str, auth: str) -> None:
    data = api_request("GET", build_url(base, "get_priorities"), auth)
    if as_map:
        m = to_name_id_map(data)
        out(m)
        stderr(f"✓ get-priorities --map: {len(m)} priority(s)")
        return
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ get-priorities: {count} priority(s)")


def batch_add_cases(
    section_id: int, json_file_path: str,
    from_draft: bool, only_new: bool, write_back: bool,
    base: str, auth: str,
) -> None:
    assert_file_size_ok(json_file_path, "--json-file")
    raw  = open(json_file_path).read()
    data = parse_json(raw, "batch-add-cases")

    if isinstance(data, dict) and "cases" in data:
        envelope: dict[str, Any] | None = data
        cases: list[dict[str, Any]]     = data["cases"]
    elif isinstance(data, list):
        envelope = None
        cases    = data
    else:
        stderr("Error: JSON must be an array of cases or a draft envelope with a 'cases' key")
        sys.exit(EXIT_LOCAL)

    if only_new:
        to_post = [c for c in cases if not c.get("id")]
        skipped = len(cases) - len(to_post)
        if skipped:
            stderr(f"✓ --only-new: skipping {skipped} already-published case(s)")
    else:
        to_post = list(cases)

    if not to_post:
        stderr("✓ batch-add-cases: nothing to post (all cases already have IDs)")
        out([])
        return

    results = []
    for case in to_post:
        body   = prepare_draft_case(case) if from_draft else translate_case_fields(case)
        result = api_request("POST", build_url(base, f"add_case/{section_id}"), auth, body)
        results.append(result)
        stderr(f"✓ add-case: id={result.get('id')}")

    if write_back:
        if envelope is None:
            stderr("Warning: --write-back requires a draft envelope file (JSON with a 'cases' key); skipped")
        else:
            title_to_result = {r.get("title"): r for r in results}
            for case in cases:
                matched = title_to_result.get(case.get("title"))
                if matched and matched.get("id"):
                    case["id"] = matched["id"]
            from datetime import datetime, timezone
            envelope["published_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            tmp = json_file_path + ".tmp"
            with open(tmp, "w") as f:
                f.write(json.dumps(envelope, indent=2) + "\n")
            os.replace(tmp, json_file_path)
            stderr(f"✓ --write-back: IDs patched in {os.path.basename(json_file_path)}")

            if all(c.get("id") for c in envelope.get("cases", [])):
                dirname      = os.path.dirname(json_file_path)
                basename     = os.path.basename(json_file_path)
                if basename.startswith("draft-"):
                    new_basename = "cases-" + basename[len("draft-"):]
                    new_path     = os.path.join(dirname, new_basename)
                    if not os.path.exists(new_path):
                        os.rename(json_file_path, new_path)
                        stderr(f"✓ renamed → {new_basename} (all cases published)")

    out(results)
    stderr(f"✓ batch-add-cases: {len(results)} case(s) created")


def add_section(project_id: int, suite_id: int, name: str, parent_id: int, base: str, auth: str) -> None:
    body = {"suite_id": suite_id, "name": name, "parent_id": parent_id}
    data = api_request("POST", build_url(base, f"add_section/{project_id}"), auth, body)
    out(data)
    stderr(f"✓ add-section: id={data.get('id')}")


def add_case(section_id: int, payload: dict[str, Any], base: str, auth: str) -> None:
    body = translate_case_fields(payload)
    data = api_request("POST", build_url(base, f"add_case/{section_id}"), auth, body)
    out(data)
    stderr(f"✓ add-case: id={data.get('id')}")


def update_case(case_id: int, payload: dict[str, Any], base: str, auth: str) -> None:
    body = {k: v for k, v in translate_case_fields(payload).items() if k != "id"}
    data = api_request("POST", build_url(base, f"update_case/{case_id}"), auth, body)
    out(data)
    stderr(f"✓ update-case: id={data.get('id')}")


def batch_update_cases(json_file_path: str, from_draft: bool, base: str, auth: str) -> None:
    raw  = open(json_file_path).read()
    data = parse_json(raw, "batch-update-cases")

    if from_draft:
        if isinstance(data, dict) and "cases" in data:
            all_cases = data["cases"]
        elif isinstance(data, list):
            all_cases = data
        else:
            stderr("Error: --from-draft requires a draft envelope with a 'cases' key or an array")
            sys.exit(EXIT_USAGE)
        payloads = [c for c in all_cases if c.get("id")]
        skipped  = len(all_cases) - len(payloads)
        if skipped:
            stderr(f"✓ --from-draft: skipping {skipped} case(s) without IDs")
    else:
        if not isinstance(data, list):
            stderr("Error: batch-update-cases JSON file must be a list of case objects")
            sys.exit(EXIT_USAGE)
        payloads = data

    results = []
    for payload in payloads:
        case_id = payload.get("id")
        if not case_id:
            stderr("Error: each case object must have an 'id' field")
            sys.exit(EXIT_USAGE)
        body = prepare_draft_case(payload) if from_draft else {k: v for k, v in translate_case_fields(payload).items() if k != "id"}
        result = api_request("POST", build_url(base, f"update_case/{case_id}"), auth, body)
        results.append(result)
        stderr(f"✓ update-case: id={result.get('id')}")
    out(results)
    stderr(f"✓ batch-update-cases: {len(results)} case(s) updated")


def add_run(project_id: int, suite_id: int, name: str, case_ids: list[int], base: str, auth: str) -> None:
    body = {"suite_id": suite_id, "name": name, "include_all": False, "case_ids": case_ids}
    data = api_request("POST", build_url(base, f"add_run/{project_id}"), auth, body)
    out(data)
    stderr(f"✓ add-run: id={data.get('id')}")


def add_results(run_id: int, results: list[dict[str, Any]], base: str, auth: str) -> None:
    body = {"results": [translate_result_fields(r) for r in results]}
    data = api_request("POST", build_url(base, f"add_results_for_cases/{run_id}"), auth, body)
    out(data)
    count = len(data) if isinstance(data, list) else "?"
    stderr(f"✓ add-results: {count} result(s) posted")


def log_gap(ticket_id: str, description: str, context: str | None, workaround: str | None) -> None:
    from datetime import datetime, timezone
    dir_path = os.path.join(os.getcwd(), "ai-context", ticket_id, "qa")
    os.makedirs(dir_path, exist_ok=True)
    log_path = os.path.join(dir_path, "run-log.md")
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write(f"# Run Log — {ticket_id}\n\n> Corrections and errors recorded during the QA pipeline run.\n")
    ts    = datetime.now(timezone.utc).isoformat()
    entry = (
        f"\n## {ts} · capability-gap · fetch_testrail.py\n"
        f"- **What:** {description}\n"
        f"- **Context:** {context or '—'}\n"
        f"- **Workaround:** {workaround or 'none'}\n"
    )
    with open(log_path, "a") as f:
        f.write(entry)
    out({"logged": log_path, "ticketId": ticket_id, "ts": ts})
    stderr(f"✓ log-gap: appended capability-gap entry to {log_path}")


# ── Usage ──────────────────────────────────────────────────────────────────────

def print_usage() -> None:
    stderr(f"""Usage: python fetch_testrail.py <subcommand> [args]

Subcommands:
  get-projects
  get-suites       <project_id>
  get-sections     <project_id> <suite_id>   [--all] [--compact] [--match-keywords "kw1,kw2"] [--match "kw1,kw2"] [--section-id ID] [--limit N] [--offset N]
  get-cases        <project_id> <suite_id>   [--section-id ID] [--limit N] [--offset N]
  get-cases-for-sections <project_id> <suite_id> [--section-ids 1,2,3] [--match-keywords "kw1,kw2"] [--match "kw1,kw2"] [--merge-into <path>] [--max-sections N] [--max-cases N]
  get-case-types                             [--map]
  get-case-fields                            [--required-only]
  get-priorities                             [--map]
  batch-add-cases  <section_id> --json-file <path> [--from-draft] [--only-new] [--write-back]
  update-case      <case_id> <json_payload>
  batch-update-cases --json-file <path> [--from-draft]
  add-section      <project_id> <suite_id> <name> <parent_id>
  add-case         <section_id> <json_payload>
  add-run          <project_id> <suite_id> <name> <case_ids_csv>
  add-results      <run_id> <json_payload>
  log-gap          <description> --ticket <ticket-id> [--context <what you were doing>] [--workaround python|jq|shell|none]

Notes:
  - Path args are confined to the cwd-relative {ARTIFACT_ROOT}/ root: --merge-into and
    --json-file must resolve inside it, log-gap --ticket must match /^[A-Za-z0-9_-]+$/,
    and symlinks / paths that traverse outside are rejected. Input files are size-bounded.
  - <case_ids_csv> is a comma-separated list of integers: 12345,12346,12347
  - add-results payload must have shape: '{{"results":[{{"caseId":N,"statusId":N,"comment":"..."}}]}}'
  - get-cases-for-sections paginates every section, shapes cases to {{id,title,sectionId,steps}},
    dedupes by id, and (with --merge-into) sets .testRailTests in that JSON file in place.
    Caps (defaults): --max-sections 20 and --max-cases 150.
  - get-sections --match-keywords scores the full tree by keyword count in section name (score=number
    of keywords that appear), returns sections with score>=1 ordered best-first, and adds a "score"
    field to each result. Use this instead of --match when you need ranked results for an agent to
    pick section IDs to pass to get-cases-for-sections. --match is a simple any-keyword filter.
  - get-cases-for-sections --match-keywords resolves section IDs automatically via keyword scoring
    (same logic as get-sections --match-keywords) then fetches cases from the top matches up to
    --max-sections. Eliminates the need to call get-sections first and score sections inline.
    Cannot be combined with --section-ids (explicit IDs take precedence).
  - get-sections --match filters the full tree by name keyword (any-match, case-insensitive)
    and attaches a root→leaf .path / .pathIds breadcrumb to each hit.
  - get-case-types --map / get-priorities --map emit a {{name: id}} object for direct name→id lookup.
  - get-case-fields --required-only emits {{requiredFields:[{{system_name,label,type_id}}],count}}.
  - log-gap records a missing query/capability as a markdown capability-gap entry appended to
    ai-context/<ticket-id>/qa/run-log.md. Requires --ticket; local-only — no TestRail credentials needed.
  - batch-add-cases --from-draft accepts the canonical draft envelope format (a JSON object with a
    "cases" key) in addition to raw arrays. Strips internal-only fields (grill_status, source_case_ids,
    rewrite_notes, permission_flag, platform_flag) and maps run_type strings to API integers
    ("regression"→1, "smoke"→2). Also accepts plain arrays when --from-draft is set.
  - batch-add-cases --only-new skips cases that already carry a non-null "id" — safe to re-run
    after a partial publish.
  - batch-add-cases --write-back patches returned IDs back into the source file and sets
    "published_at". When every case in the file has an ID and the file is named draft-*, it is
    automatically renamed to cases-* (the publication signal). Requires a draft envelope file.
  - batch-update-cases --from-draft accepts a draft envelope or array; skips cases without IDs;
    strips internal fields and maps run_type strings before updating.""")


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(EXIT_USAGE)

    subcmd = sys.argv[1]

    workspace = find_workspace_root()
    load_env(os.path.join(workspace, ".env"))

    if subcmd == "log-gap":
        pos, flags = parse_args(sys.argv[2:])
        require_positional(pos, 1, "log-gap <description> --ticket <ticket-id> [--context <what you were doing>] [--workaround python|jq|shell|none]")
        if not flags.get("ticket") or flags.get("ticket") == "true":
            stderr("Error: --ticket <ticket-id> is required for log-gap (selects ai-context/<ticket-id>/qa/run-log.md)")
            sys.exit(EXIT_USAGE)
        assert_safe_segment(flags["ticket"], "--ticket")
        log_gap(flags["ticket"], pos[0], flags.get("context"), flags.get("workaround"))
        return

    testrail_url = os.environ.get("TESTRAIL_URL", "").rstrip("/")
    username     = os.environ.get("TESTRAIL_USERNAME", "")
    api_key      = os.environ.get("TESTRAIL_API_KEY", "")

    if not testrail_url: stderr("Error: TESTRAIL_URL not set in .env (e.g. https://yourorg.testrail.io)"); sys.exit(EXIT_USAGE)
    if not username:     stderr("Error: TESTRAIL_USERNAME not set in .env");                               sys.exit(EXIT_USAGE)
    if not api_key:      stderr("Error: TESTRAIL_API_KEY not set in .env");                                sys.exit(EXIT_USAGE)

    validate_url(testrail_url)

    base = build_base_url(testrail_url)
    auth = build_auth(username, api_key)
    stderr(f"→ TestRail target: {urllib.parse.urlparse(testrail_url).netloc}")

    pos, flags = parse_args(sys.argv[2:])

    if subcmd == "get-projects":
        get_projects(base, auth)

    elif subcmd == "get-suites":
        require_positional(pos, 1, "get-suites <project_id>")
        get_suites(to_int(pos[0], "project_id"), base, auth)

    elif subcmd == "get-sections":
        require_positional(pos, 2, "get-sections <project_id> <suite_id> [--all] [--compact] [--match \"kw1,kw2\"] [--section-id ID] [--limit N] [--offset N]")
        get_sections(
            to_int(pos[0], "project_id"),
            to_int(pos[1], "suite_id"),
            to_int(flags["limit"], "--limit")     if "limit"  in flags else 250,
            to_int(flags["offset"], "--offset")   if "offset" in flags else 0,
            flags.get("all")     == "true",
            flags.get("compact") == "true",
            [s.strip() for s in flags.get("match", "").split(",") if s.strip()],
            [s.strip() for s in flags.get("match-keywords", "").split(",") if s.strip()],
            to_int(flags["section-id"], "--section-id") if "section-id" in flags else None,
            base, auth,
        )

    elif subcmd == "get-cases":
        require_positional(pos, 2, "get-cases <project_id> <suite_id> [--section-id ID] [--limit N] [--offset N]")
        get_cases(
            to_int(pos[0], "project_id"),
            to_int(pos[1], "suite_id"),
            to_int(flags["section-id"], "--section-id") if "section-id" in flags else None,
            to_int(flags["limit"], "--limit")   if "limit"  in flags else 250,
            to_int(flags["offset"], "--offset") if "offset" in flags else 0,
            base, auth,
        )

    elif subcmd == "get-cases-for-sections":
        require_positional(pos, 2, "get-cases-for-sections <project_id> <suite_id> [--section-ids 1,2,3] [--match \"kw1,kw2\"] [--merge-into <path>] [--max-sections N] [--max-cases N]")
        section_ids = [
            to_int(s.strip(), "--section-ids")
            for s in flags.get("section-ids", "").split(",")
            if s.strip()
        ]
        match = [s.strip() for s in flags.get("match", "").split(",") if s.strip()]
        match_keywords = [s.strip() for s in flags.get("match-keywords", "").split(",") if s.strip()]
        get_cases_for_sections(
            to_int(pos[0], "project_id"),
            to_int(pos[1], "suite_id"),
            section_ids,
            match,
            confine_to_artifact_root(flags["merge-into"], "--merge-into", False) if "merge-into" in flags else None,
            to_int(flags["max-sections"], "--max-sections") if "max-sections" in flags else 20,
            to_int(flags["max-cases"],    "--max-cases")    if "max-cases"    in flags else 150,
            match_keywords,
            base, auth,
        )

    elif subcmd == "get-case-types":
        get_case_types(flags.get("map") == "true", base, auth)

    elif subcmd == "get-case-fields":
        get_case_fields(flags.get("required-only") == "true", base, auth)

    elif subcmd == "get-priorities":
        get_priorities(flags.get("map") == "true", base, auth)

    elif subcmd == "batch-add-cases":
        require_positional(pos, 1, "batch-add-cases <section_id> --json-file <path> [--from-draft] [--only-new] [--write-back]")
        if "json-file" not in flags:
            stderr("Error: --json-file <path> is required for batch-add-cases")
            sys.exit(EXIT_USAGE)
        batch_add_cases(
            to_int(pos[0], "section_id"),
            confine_to_artifact_root(flags["json-file"], "--json-file", True),
            flags.get("from-draft") == "true",
            flags.get("only-new")   == "true",
            flags.get("write-back") == "true",
            base, auth,
        )

    elif subcmd == "add-section":
        require_positional(pos, 4, "add-section <project_id> <suite_id> <name> <parent_id>")
        add_section(to_int(pos[0], "project_id"), to_int(pos[1], "suite_id"), pos[2], to_int(pos[3], "parent_id"), base, auth)

    elif subcmd == "add-case":
        require_positional(pos, 2, "add-case <section_id> <json_payload>")
        payload = parse_json(pos[1], "add-case")
        add_case(to_int(pos[0], "section_id"), payload, base, auth)

    elif subcmd == "update-case":
        require_positional(pos, 2, "update-case <case_id> <json_payload>")
        payload = parse_json(pos[1], "update-case")
        update_case(to_int(pos[0], "case_id"), payload, base, auth)

    elif subcmd == "batch-update-cases":
        if "json-file" not in flags:
            stderr("Error: --json-file <path> is required for batch-update-cases")
            sys.exit(EXIT_USAGE)
        batch_update_cases(
            confine_to_artifact_root(flags["json-file"], "--json-file", True),
            flags.get("from-draft") == "true",
            base, auth,
        )

    elif subcmd == "add-run":
        require_positional(pos, 4, "add-run <project_id> <suite_id> <name> <case_ids_csv>")
        case_ids = []
        for token in pos[3].split(","):
            n = token.strip()
            try:
                case_ids.append(int(n))
            except ValueError:
                stderr(f"Error: case_ids must be comma-separated integers, got {json.dumps(n)}")
                sys.exit(EXIT_USAGE)
        add_run(to_int(pos[0], "project_id"), to_int(pos[1], "suite_id"), pos[2], case_ids, base, auth)

    elif subcmd == "add-results":
        require_positional(pos, 2, "add-results <run_id> <json_payload>")
        payload = parse_json(pos[1], "add-results")
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            stderr('Error: JSON payload must have shape {"results": [...]}')
            sys.exit(EXIT_USAGE)
        add_results(to_int(pos[0], "run_id"), payload["results"], base, auth)

    else:
        stderr(f"Error: unknown subcommand {json.dumps(subcmd)}")
        print_usage()
        sys.exit(EXIT_USAGE)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"Fatal: {e}\n")
        sys.exit(EXIT_GENERIC)
