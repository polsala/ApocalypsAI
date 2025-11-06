# ApocalypsAI

Collective of autonomous AIs building, reviewing, refactoring, and safeguarding repositories through GitHub Actions workflows.

> Philosophy: “Anarchy with discipline” — each agent is free-form internally, but all automation is isolated, testable, and documented.

## Repository Layout

```
.
├── AGENTS.md                # Contract describing every agent’s runtime + expectations
├── LICENSE
├── README.md
├── agents/                  # Python 3.11 agent implementations
│   ├── __init__.py
│   ├── agent_builder.py     # Issue-driven generator (packs/docs/tests diffs)
│   ├── agent_guardian.py    # Issue content safety triage
│   ├── agent_integrator.py  # Nightly micro-refactors and doc/test touch-ups
│   ├── agent_reviewer.py    # Cross-provider PR reviewer
│   ├── agent_utils.py       # GitHub REST helpers (issues/PRs/comments/diffs)
│   ├── base.py              # AgentContext + AgentBase contract
│   └── llm_clients.py       # OpenRouter/Groq/Gemini adapters + cheap_mix fallback
├── tools/
│   └── apply_diff.py        # Utility invoked inside workflows to apply .apocalypsai/last.diff
└── .github/workflows/       # Automation surface; see below
```

## GitHub Workflows

| Workflow | Purpose | Trigger |
| --- | --- | --- |
| `gen_openrouter.yml` | Runs the generator agent (OpenRouter provider) to propose a pack/doc/test diff, commits to `ai/openrouter-<timestamp>`, and opens a PR. | Cron `0,30 * * * *` |
| `gen_groq.yml` | Same generator flow but pinned to Groq. | Cron `10,40 * * * *` |
| `gen_gemini.yml` | Same generator flow but pinned to Gemini. | Cron `20,50 * * * *` |
| `nightly_self_heal.yml` | Runs the integrator agent via `cheap_mix` to ship tiny self-healing PRs (`ai/nightly-<date>`). | Daily cron `42 2 * * *` |
| `pr_review.yml` | Executes the reviewer agent to post a single consolidated Markdown review comment (✅/🧪/🔒/🧩/🧱). | PR opened/synchronized/ready_for_review |
| `test_and_eval.yml` | Enforces isolation: per-pack Python venvs, Node/Go/Rust toolchains, socket blocking, and workspace cleanliness. | PR activity + push to `main` |
| `issue_guardian.yml` | Runs the guardian agent to classify issue content and optionally label `triage/blocked`. | Issue opened/edited |
| `docs_check.yml` | Verifies new packs include README quickstart, runnable examples/CLI `--help`, and changelog fragment. | PR activity |

All workflows share:

- `ubuntu-latest` runners
- Python 3.11 via `actions/setup-python@v5`
- Minimal deps installed (`requests`, `rich`, `pyyaml`, `pytest`)
- Secrets: `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY`, `GITHUB_TOKEN`
- Generator/integrator jobs write unified diff artifacts to `.apocalypsai/last.diff`

## Agents

Each agent follows the API defined in `AGENTS.md`:

- **Builder (`agents/agent_builder.py`)**  
  CLI: `python agents/agent_builder.py --repo owner/name --issue-number <id> [--models provider=model]`  
  Fetches issue context, prompts LLM (via `llm_clients.cheap_mix`), writes `.apocalypsai/last.diff`, exits with code `0` (diff), `2` (no change), or `1` (failure).

- **Integrator (`agents/agent_integrator.py`)**  
  CLI requires `--mode nightly`. Produces tiny additive diffs for nightly self-heal workflow.

- **Reviewer (`agents/agent_reviewer.py`)**  
  CLI: `--repo`, `--pr`. Downloads PR metadata, changed files, diff, and prior comments to prompt a cross-provider review. Posts a single Markdown comment via GitHub API.

- **Guardian (`agents/agent_guardian.py`)**  
  CLI: `--repo`, `--issue-number`. Classifies issue content (`Safe`, `Suspicious`, `Blocked`) and labels blocked issues.

Supporting modules:

- `agents/base.py` — `AgentContext` dataclass & abstract `AgentBase.run`.
- `agents/llm_clients.py` — `call_openrouter`, `call_groq`, `call_gemini`, and `cheap_mix` with retries/jitter + sanitization.
- `agents/agent_utils.py` — Minimal GitHub REST helpers (issues, PRs, comments, labels, diffs).

## Tooling & Local Development

1. **Python setup**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip requests rich pyyaml pytest
   ```

2. **Environment variables**  
   Export the provider keys and `GITHUB_TOKEN` before running agents locally:
   ```bash
   export OPENROUTER_API_KEY=...
   export GROQ_API_KEY=...
   export GOOGLE_API_KEY=...
   export GITHUB_TOKEN=ghp_xxx
   ```

3. **Testing**  
   No monolithic test suite yet; follow per-pack instructions enforced by `test_and_eval.yml`. Run pack-specific tests via their native toolchain (Python `pytest`, Node `npm test`, Go `go test`, Rust `cargo test`), ensuring no network calls (mock or stub as required).

4. **Diff application helper**
   ```bash
   python tools/apply_diff.py .apocalypsai/last.diff
   ```

## Contributing

- All changes must land through Pull Requests; no direct pushes to `main`.
- Keep diffs tiny (< ~200 LOC) and reversible.
- Every agent-generated change must include tests + docs updates.
- No secrets in logs, diffs, or artifacts.
- Prefer mocks/fakes for third-party integrations; include a nearby `# Mock rationale:` comment describing why.

For deeper requirements (prompt shapes, acceptance checklist, error-handling rules), refer to [AGENTS.md](AGENTS.md).
