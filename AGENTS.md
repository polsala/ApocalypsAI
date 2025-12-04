# AGENTS.md — Contract for ApocalypsAI Agents

*Make it wild, but make it work.*

This document is the **single source of truth** for implementing the autonomous agents used by ApocalypsAI. Any model (Codex, GPT-5, etc.) generating or modifying agent code MUST follow this spec **exactly**, or the workflows will reject the PR.

---

## 0) Philosophy

* **Anarchy with discipline**: use any language/tech *inside* a pack, but agents themselves are **Python 3.11**, minimal deps.
* **Always via PR**: no direct pushes to `main`. Human merges.
* **Isolation & tests**: every new feature brings tests, docs, and a clear test plan.
* **Self-contained utilities**: every change is additive, isolated, and easy to revert.
* **No secrets in logs**. Ever.

---

## 1) Files & Layout

```
agents/
  __init__.py
  base.py
  llm_clients.py
  agent_builder.py
  agent_reviewer.py
  agent_guardian.py
  agent_integrator.py
  agent_utils.py
utils/
  <util_name>/
    README.md
    src/...            # language/tooling chosen per utility
    tests/...          # self-contained tests/mock fixtures
```

* **Language**: Python 3.11
* **Allowed deps**: `requests`, `pyyaml`, `rich` (for pretty logs), `typing` stdlib
* **Optional**: `tomli` for reading pyproject TOML (no heavy frameworks)

---

## 2) Common Runtime Contract

### CLI (all agents)

* Must accept `--repo <owner/name>`
* Must accept one of:

  * `--issue-number <int>` (for Builder/Guardian)
  * `--pr <int>` (for Reviewer)
  * `--mode nightly` (for Integrator)
* Must exit with:

  * `0` success
  * `2` no-op (nothing to change)
  * `1` failure (print actionable error)

### Env vars (exported by workflows)

* `OPENROUTER_API_KEY` (optional)
* `GROQ_API_KEY` (optional)
* `GOOGLE_API_KEY` (optional)
* `GROQ_MODEL_POOL` (optional) — JSON array of Groq model names for fallback sequence
  * Example: `["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"]`
  * Default: `["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"]`
* `GITHUB_TOKEN` (**required** for GitHub API)
* Agents MAY choose any available provider via `llm_clients.py`. If none available → fail with code `1`.

### Networking

* Allowed: GitHub API, LLM provider APIs
* Forbidden: any other outbound network at agent runtime

### Output artifacts

* Successful runs **must** create a brand-new directory under `utils/<util_name>/`.
* All generated source, docs, fixtures, and tests live inside that folder (self-contained).
* No `.apocalypsai` artifacts or repo edits outside `utils/<util_name>/`.

### Logging

* Use plain stdout, single-line JSON or compact text.
* Prefix errors with `ERROR:`.
* Never print env values or tokens.

---

## 3) LLM Client Adapter (`agents/llm_clients.py`)

**Purpose**: Provide a simple, deterministic interface to multiple providers with graceful fallback.

```python
# Required interface (do not rename)
from typing import Optional, Dict

class LLMError(RuntimeError): ...
def call_openrouter(prompt: str, model: str = "google/gemini-1.5-flash-8b") -> str: ...
def call_groq(
    prompt: str,
    model: Optional[str] = None,
    model_pool: Optional[list[str]] = None,
) -> str:
    """
    Call Groq with configurable model fallback.
    
    Args:
        prompt: The prompt to send
        model: Single model to use (overrides pool)
        model_pool: List of models to try in sequence
        
    If neither model nor model_pool is provided, reads from GROQ_MODEL_POOL
    env var (JSON array format), or uses default pool:
    ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"]
    """
def call_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str: ...
def cheap_mix(prompt: str, models: Optional[Dict[str, str]] = None) -> str:
    """
    Try providers in order: Groq -> Gemini -> OpenRouter.
    Return first successful text response.
    Raise LLMError if all fail.
    Must set conservative timeouts and basic retry with jitter.
    """
```

* **Retries**: up to 2 retries/provider, exponential backoff (≤ 8s total/provider)
* **Timeouts**: 60s per HTTP request
* **Sanitization**: strip ANSI, trailing fences; never assume markdown formatting

---

## 4) Base Class (`agents/base.py`)

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class AgentContext:
    repo: str            # "owner/name"
    issue_number: Optional[int] = None
    pr_number: Optional[int] = None
    mode: Optional[str] = None        # e.g., "nightly"
    models: Optional[Dict[str, str]] = None  # provider->model overrides

class AgentBase:
    def run(self, ctx: AgentContext) -> int:
        """
        Returns exit code (0 success / 2 no-op / 1 failure).
        Must catch and log exceptions, never raise to top.
        """
        raise NotImplementedError
```

All concrete agents must subclass `AgentBase` and implement `run`.

---

## 5) Agent Roles & IO Contracts

### A) Builder — `agents/agent_builder.py`

**Trigger**: issue labeled `idea`
**Goal**: ship a brand-new community utility inside `utils/<util_name>/` based on the issue prompt.

**Input**

* `--repo`, `--issue-number`
* Fetch issue title/body via GitHub API plus existing `utils/*` folder names.

**Prompt shape (internal)**

* Provide issue context, repository snippets, and the current `utils/` inventory.
* Instruct the LLM to answer with pure JSON shaped as:

  ```json
  {
    "util_name": "kebab-case-identifier",
    "summary": "one sentence overview",
    "files": [
      {
        "path": "README.md",
        "description": "docs + usage",
        "content": "<full file contents>"
      },
      {
        "path": "tests/test_smoke.py",
        "description": "unit tests",
        "content": "<code>"
      }
    ]
  }
  ```

* Constraints:

  * `util_name` must be unique (no collisions with existing folders) and ≤ 32 chars.
  * All file paths are relative to the new util root; include README + at least one `tests/` file.
  * Tests must avoid network access (use mocks; include `# Mock rationale:`) — runs without tests must fail fast.
  * Output can use any language/tooling as long as it stays self-contained, well documented, and fully tested.

**Output**

* Materialize the described folder/files directly under `utils/<util_name>/`.
* Exit `0` when files were created; `2` if the LLM reports “NO_CHANGES” or invalid payload; `1` on hard error.

### B) Reviewer — `agents/agent_reviewer.py`

**Trigger**: PR opened/sync/ready_for_review
**Goal**: post a **single consolidated** Markdown review comment.

**Input**

* `--repo`, `--pr`
* Fetch changed files diff (`origin/main...HEAD`), PR title/body, existing comments.

**Prompt shape**

* Checklist sections:

  * ✅ What’s solid
  * 🧪 Tests (coverage, missing, network isolation)
  * 🔒 Security (secrets, unsafe APIs)
  * 🧩 Docs/DX (README, examples)
  * 🧱 Mocks/fakes justification (if applicable)
* Output must be **Markdown**, ≤ 1500 words, with concrete suggestions and code snippets.

**Output**

* POST one PR comment via GitHub API
* Exit `0` (always; comment even if negative). Use `1` only on hard failure.

### C) Guardian — `agents/agent_guardian.py`

**Trigger**: issue opened/edited
**Goal**: verdict on issue content: `Safe` / `Suspicious` / `Blocked`

**Input**

* `--repo`, `--issue-number`
* Pull issue title+body

**Rules**

* Block content that suggests abuse, illegal activity, secrets exfiltration, hate/NSFW, spam
* Comment short verdict + reason; if `Blocked`, label `triage/blocked`

**Output**

* One issue comment
* Exit `0`

### D) Integrator — `agents/agent_integrator.py`

**Trigger**: nightly cron
**Goal**: dream up a tiny-yet-useful standalone utility (any language) and drop it in `utils/<nightly-*>/`.

**Input**

* `--repo`, `--mode nightly`

**Prompt shape**

* Summarize repository/README context and list existing `utils/*` to avoid repeats.
* Reinforce the same JSON schema as the builder, but bias toward whimsical, fully documented tools with solid tests.
* Explicitly remind the LLM that at least one `tests/` file is mandatory; no tests → reject.
* Encourage fresh ideas only; respond `NO_CHANGES` if nothing safe emerges.

**Output**

* Create the utility folder/files directly; exit `0` on success, `2` on no-op.

---

## 6) GitHub API Helpers (`agent_utils.py`)

* Minimal helpers:

  * `get_issue(repo, n) -> dict`
  * `get_pr(repo, n) -> dict`
  * `post_issue_comment(repo, n, md) -> None`
  * `post_pr_comment(repo, n, md) -> None`
  * All use `GITHUB_TOKEN` and `requests`, raise with clear messages.

---

## 7) Utility Requirements

* Every run that returns `0` must leave the workspace with exactly one new folder under `utils/<util_name>/`.
* Folder constraints:
  * Contains a README (usage, install, test instructions).
  * Contains at least one automated test under `tests/`.
  * Never touches files outside the folder (except Git metadata handled by workflows).
  * Uses relative paths only; no symlinks or filesystem escapes.
* If the LLM output is empty/invalid or violates the folder contract → exit `2` with a clear message.

---

## 8) Rate Limits & Scheduling (Guidance)

* Generators run on staggered crons (configured in workflows).
* `llm_clients` must back off on HTTP 429 with jitter, total wait ≤ 20s/provider.
* If exhausted → exit `2` (no-op) rather than fail the job.

---

## 9) Testing & Isolation Rules

* **Do not** open network sockets from tests.
* Use **mocks/fakes** for third-party calls. Provide a short comment: “Mock rationale”.
* Per-pack tests live in `packs/<name>/tests/`.
* Prefer property-based tests or golden tests where small and stable.
* Every new CLI must support `--help` and include **README usage examples**.

---

## 10) Security & Compliance

* Never write secrets to disk or logs.
* Block attempts to inject secrets into code.
* No shelling out to untrusted commands.
* Only modify files in repo workspace.

---

## 11) Error Handling & Exit Codes

* `0` = success (diff written or comment posted)
* `2` = no-op (nothing to change; rate-limit backoff exhausted; empty diff)
* `1` = hard failure (exception, invalid env, invalid API response)

Agents must catch exceptions and print human-readable failures like:

```
ERROR: Failed to fetch PR #123: 403 Forbidden (check GITHUB_TOKEN scopes)
```

---

## 12) Minimal CLI Harness (template)

```python
# template.py – copy pattern into each agent_*.py
import argparse, sys
from base import AgentContext
from my_agent_impl import MyAgent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--issue-number", type=int)
    ap.add_argument("--pr", type=int)
    ap.add_argument("--mode")
    args = ap.parse_args()

    ctx = AgentContext(repo=args.repo, issue_number=args.issue_number, pr_number=args.pr, mode=args.mode)
    code = MyAgent().run(ctx)
    sys.exit(code)

if __name__ == "__main__":
    main()
```

---

## 13) Acceptance Checklist (must pass in PR)

* [ ] Agent respects CLI & exit codes
* [ ] Uses `llm_clients.cheap_mix` only (or a subset), with retries
* [ ] Creates a brand-new folder under `utils/<util_name>` with README + tests (Builder/Integrator)
* [ ] Reviewer posts **one** consolidated Markdown comment
* [ ] Guardian labels `triage/blocked` when needed
* [ ] No secrets in logs
* [ ] Added/updated tests + README for any generated pack
* [ ] Utility is self-contained, well tested, and easy to revert

---

## 14) Mock Justification (required when used)

If tests mock external systems, include a brief comment near the mock:

```python
# Mock rationale: external API is rate-limited and not available in CI; we validate schema and behavior via recorded fixtures.
```

---

## 15) Example Prompts (internal to agents)

* **Builder**: “Design a CLI that converts CSV→JSON and ship it inside `utils/csv2json/` with README, CLI code, and pytest coverage. Respond with the required JSON payload describing each file (README, src module, tests) and ensure tests avoid network calls.”
* **Reviewer**: “Review the provided diff. Produce a concise Markdown comment with ✅, 🧪, 🔒, 🧩 sections and concrete code suggestions.”
* **Integrator (nightly)**: “Dream up a `utils/nightly-checksum-tool` folder containing README, Python/Rust code, and tests. Keep everything self-contained, explain how to run it in the README, and answer with the JSON payload schema.”
