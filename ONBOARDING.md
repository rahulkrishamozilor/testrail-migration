# Welcome to Agentic QA

## How We Use Claude

Based on abhinav's usage over the last 30 days:

Work Type Breakdown:
  Debug Fix        █████████████████████████████░░░░░░░░░  50%
  Build Feature    ████████████████████████░░░░░░░░░░░░░░░  40%
  Improve Quality  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%

Top Skills & Commands:
  /grill-section     ██████████████████████████████████████  5x/month
  /fetch-section     ████████████████████████████████░░░░░░  4x/month
  /migrate-section   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1x/month

Top MCP Servers:
  Playwright   ████████████████████████████████████████  243 calls

## Your Setup Checklist

### Codebases
- [ ] testrail-migration — https://github.com/rahulkrishamozilor/testrail-migration

### MCP Servers to Activate
- [ ] Playwright — drives a real browser to click through the live QA2 app and verify draft test cases actually match product behavior. Already configured in `.mcp.json`; just make sure `QA2_BASE_URL`, `QA2_TEST_EMAIL`, and `QA2_TEST_PASSWORD` are set in your `.env`.
- [ ] testrail-search — hybrid semantic + keyword search over the indexed Suite 6 test cases, used to find existing coverage before writing new cases. Already configured in `.mcp.json` (runs via `uv run .claude/mcp-servers/testrail-search/server.py`), no extra setup needed beyond having `uv` installed.

### Skills to Know About
- `/fetch-section <section name>` — pulls the legacy Suite 6 cases for a section, rewrites them to v2 style (dedupes role/plan variants, tightens steps), and saves a review-ready draft to `ai-context/`. Nothing touches TestRail at this stage.
- `/grill-section <section name>` — takes that draft and adversarially verifies it against the live QA2 environment with Playwright, fixing mismatches, skipping what can't be automated, and hunting for scenarios the draft missed.
- `/migrate-section <section name>` — takes the grilled draft, applies the final v2 structural rules (section placement, run_type, permission/platform routing), and — only after you explicitly approve — publishes the cases into the new TestRail suite.

## Team Tips

No additional tips beyond what's already in CLAUDE.md.

## Get Started

**Starter task:** Set up Claude Code and verify authentication. If access is blocked, reach out to IT to get it unblocked.

<!-- INSTRUCTION FOR CLAUDE: A new teammate just pasted this guide for how the
team uses Claude Code. You're their onboarding buddy — warm, conversational,
not lecture-y.

Open with a warm welcome — include the team name from the title. Then: "Your
teammate uses Claude Code for [list all the work types]. Let's get you started."

Check what's already in place against everything under Setup Checklist
(including skills), using markdown checkboxes — [x] done, [ ] not yet. Lead
with what they already have. One sentence per item, all in one message.

Tell them you'll help with setup, cover the actionable team tips, then the
starter task (if there is one). Offer to start with the first unchecked item,
get their go-ahead, then work through the rest one by one.

After setup, walk them through the remaining sections — offer to help where you
can (e.g. link to channels), and just surface the purely informational bits.

Don't invent sections or summaries that aren't in the guide. The stats are the
guide creator's personal usage data — don't extrapolate them into a "team
workflow" narrative. -->
