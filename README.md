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
│   ├── agent_builder.py     # Issue-driven generator (creates new utils/)
│   ├── agent_guardian.py    # Issue content safety triage
│   ├── agent_integrator.py  # Nightly drops of fresh utilities
│   ├── agent_reviewer.py    # Cross-provider PR reviewer
│   ├── agent_utils.py       # GitHub REST helpers (issues/PRs/comments/diffs)
│   ├── base.py              # AgentContext + AgentBase contract
│   └── llm_clients.py       # OpenRouter/Groq/Gemini adapters + cheap_mix fallback
├── utils/                   # Generated utilities (each run adds utils/<util_name>)
└── .github/workflows/       # Automation surface; see below
```

## GitHub Workflows

| Workflow | Purpose | Trigger |
| --- | --- | --- |
| `gen_openrouter.yml` | Runs the generator agent with OpenRouter provider to mint a brand-new utility under V2 classifier paths (code + README + tests) and open a PR. Uses only OpenRouter API; fails if provider is unavailable. | Cron `0 * * * *` (hourly at :00) & manual |
| `gen_groq.yml` | Runs the generator agent with Groq provider. Uses only Groq API; fails if provider is unavailable. | Cron `20 * * * *` (hourly at :20) & manual |
| `gen_gemini.yml` | Runs the generator agent with Gemini provider. Uses only Gemini API; fails if provider is unavailable. | Cron `40 * * * *` (hourly at :40) & manual |
| `nightly_self_heal.yml` | Uses the integrator agent to craft a surprise community utility under V2 classifier paths. Uses provider fallback (cheap_mix). | Daily cron `42 2 * * *` |
| `agent_pr_path_check.yml` | Periodically scans open PRs from provider agents (gemini/groq/openrouter) for path isolation violations. Automatically closes conflicting PRs with a detailed explanation. Does not affect copilot or other PRs. | Cron `0 8,14,20 * * *` (3x daily) & manual |
| `pr_review.yml` | Executes the reviewer agent to post a single consolidated Markdown review comment (✅/🧪/🔒/🧩/🧱). | PR opened/synchronized/ready_for_review |
| `pr_auto_review.yml` | Multi-agent review system: assigns PR reviews to the other two AI agents (not the PR author). Each agent posts a tagged review comment. | PR opened/synchronized/ready_for_review |
| `pr_auto_approve_merge.yml` | Automatically approves and merges PRs when all agent reviews are complete and CI checks pass. | PR review submitted, check suite completed |
| `pr_cron_review_merge.yml` | Periodically processes open PRs, triggers missing reviews, and auto-merges eligible PRs to clear backlog. | Cron `0 */4 * * *` (every 4 hours) & manual |
| `test_and_eval.yml` | Enforces isolation: per-pack Python venvs, Node/Go/Rust toolchains, socket blocking, and workspace cleanliness. | PR activity + push to `main` |
| `issue_guardian.yml` | Runs the guardian agent to classify issue content and optionally label `triage/blocked`. | Issue opened/edited |
| `docs_check.yml` | Verifies new packs include README quickstart, runnable examples/CLI `--help`, and changelog fragment. | PR activity |
| `newsletter_gemini.yml` | Generates daily Gemini newsletter content and opens a PR. Auto-approved and merged when CI passes. | Daily cron `0 6 * * *` (6:00 AM UTC) & manual |
| `newsletter_groq.yml` | Generates daily Groq newsletter content and opens a PR. Auto-approved and merged when CI passes. | Daily cron `20 6 * * *` (6:20 AM UTC) & manual |
| `newsletter_openrouter.yml` | Generates daily OpenRouter newsletter content and opens a PR. Auto-approved and merged when CI passes. | Daily cron `40 6 * * *` (6:40 AM UTC) & manual |
| `apocalypse_site_build.yml` | Validates apocalypse-site builds successfully when PR touches site files. Runs linting, builds, and checks newsletter JSON validity. | PR activity on `apocalypse-site/**` files |

**For detailed information on the automated PR review and merge system, see [docs/PR_AUTOMATION.md](docs/PR_AUTOMATION.md).**

All workflows share:

- `ubuntu-latest` runners
- Python 3.11 via `actions/setup-python@v5`
- Minimal deps installed (`requests`, `rich`, `pyyaml`, `pytest`)
- Secrets: `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY`, `GITHUB_TOKEN`
- Generator/integrator jobs write code directly beneath `utils/` (no diff artifacts)

## Utils Directory

**V2 Path Classification System**: Utilities are now organized by classifier-based paths (e.g., `rust-utils/`, `react-webpage/`, `bash-utils/`) instead of a flat `utils/` directory. See [docs/V2_PATH_CLASSIFICATION.md](docs/V2_PATH_CLASSIFICATION.md) for details.

Every autonomous run must add a fully self-contained utility to an appropriate classifier path. Requirements:

- Pick a unique slug (kebab-case is preferred) per run; never mutate existing folders.
- Choose the BEST language/technology for the task (Rust, Go, Bash, TypeScript, React, Python, etc.)
- Ship everything inside that folder: README/usage docs, source, tests/fixtures, config, etc.
- Tests must run without network access (use mocks/fakes with `# Mock rationale:` comments).
- Prefer lightweight tooling and document how to execute the util (CLI usage, API example, etc.)
- Utilities are placed in classifier paths like `rust-utils/<name>/`, `python-utils/<name>/`, etc.
- Legacy `utils/<name>/` paths are supported for backward compatibility but discouraged for new utilities.

## Agents

Each agent follows the API defined in `AGENTS.md`:

- **Builder (`agents/agent_builder.py`)**  
  CLI: `python agents/agent_builder.py --repo owner/name --issue-number <id> [--models provider=model]`  
  Fetches issue context, prompts LLM (respects `APOCALYPSAI_PROVIDER` env var), and materializes a fresh `utils/<slug>` folder. Exit codes: `0` (utility created), `2` (no-op), `1` (failure). Outputs JSON metadata for PR generation.

- **Integrator (`agents/agent_integrator.py`)**  
  CLI requires `--mode nightly`. Produces a spontaneous `utils/nightly-<slug>` utility with docs/tests or exits `2` when nothing safe emerges. Respects `APOCALYPSAI_PROVIDER` env var. Outputs JSON metadata for PR generation.

- **Reviewer (`agents/agent_reviewer.py`)**  
  CLI: `--repo`, `--pr`. Downloads PR metadata, changed files, diff, and prior comments to prompt a cross-provider review. Posts a single Markdown comment via GitHub API.

- **Guardian (`agents/agent_guardian.py`)**  
  CLI: `--repo`, `--issue-number`. Classifies issue content (`Safe`, `Suspicious`, `Blocked`) and labels blocked issues.

Supporting modules:

- `agents/base.py` — `AgentContext` dataclass & abstract `AgentBase.run`.
- `agents/llm_clients.py` — `call_openrouter`, `call_groq`, `call_gemini`, `call_provider` (respects `APOCALYPSAI_PROVIDER`), and `cheap_mix` with retries/jitter + sanitization.
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
   export APOCALYPSAI_PROVIDER=gemini  # Optional: specify provider (gemini/groq/openrouter)
   ```

3. **Testing**  
   No monolithic test suite yet; follow per-pack instructions enforced by `test_and_eval.yml`. Run pack-specific tests via their native toolchain (Python `pytest`, Node `npm test`, Go `go test`, Rust `cargo test`), ensuring no network calls (mock or stub as required).

## Contributing

- All changes must land through Pull Requests; no direct pushes to `main`.
- Keep commits focused and reversible.
- Every agent-generated utility must include tests + docs.
- No secrets in logs, diffs, or artifacts.
- Prefer mocks/fakes for third-party integrations; include a nearby `# Mock rationale:` comment describing why.
- Follow security and ethical guidelines when proposing automation features.

For deeper requirements (prompt shapes, acceptance checklist, error-handling rules), refer to [AGENTS.md](AGENTS.md).

For security and ethics guidelines, see [docs/SECURITY_AND_ETHICS.md](docs/SECURITY_AND_ETHICS.md).
