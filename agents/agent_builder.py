from __future__ import annotations

import argparse
import secrets
import subprocess
import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

INSPIRATIONS = [
    "pan-galactic emoji dialect compiler",
    "self-healing ascii circuit simulator",
    "probabilistic haiku refactoring engine",
    "time-splitting graphql cache visualizer",
    "ultra-minimalist synthwave sequencer",
    "holomorphic markdown anomaly detector",
    "browser-history noir narrative generator",
    "neural tarot inspired CLI prompt oracle",
    "chaotic container stress choreographer",
    "fractal-based log entropy grapher",
    "tactile keyboard heatmap cartographer",
    "quantumish git blame storyteller",
    "meme-driven api contract validator",
    "sentiment-tuned release note remixer",
    "procedural emoji city builder",
    "bio-luminescent cron visualizer",
    "retro fax art rasterizer",
    "stochastic dependency rumor mill",
    "l-system powered test name synthesizer",
    "anomalous unit test archaeologist",
    "hypergraph knowledge garden planter",
    "pseudorandom palette stabilizer",
    "cryptic error limerick composer",
    "emoji-first incident command console",
    "spectral git bisect fortune teller",
    "command line karaoke scorer",
    "cascading style spell checker",
    "subatomic accessibility advocate",
    "procedural feature flag storybook",
    "entropy-maximized backlog shuffler",
    "waxing-waning code coverage oracle",
    "lunar phase driven ci orchestrator",
    "spherical cow performance profiler",
    "theorem prover inspired merge planner",
    "civic data glitch notebook",
    "holographic changelog sculptor",
    "temporal diff hologram projector",
    "syntax-aware sticker pack generator",
    "pulsar-tuned config drift detector",
    "cli-based aroma diffuser simulator",
    "chaos garden of semantic versions",
    "hyperdimensional json topologist",
    "cloud-native origami pattern foundry",
    "c64 palette live coding sandbox",
    "oblique strategy code reviewer",
    "multiverse-ready backlog weaver",
    "radioactive yaml containment unit",
    "steampunk ascii blueprint printer",
    "aurora borealis inspired load tester",
    "telepathic rubber duck debugger",
]

from agents import agent_utils
from agents.base import AgentBase, AgentContext
from agents.llm_clients import LLMError, cheap_mix
from agents.util_generation import (
    PayloadError,
    list_existing_utils,
    parse_payload,
    summarize_payload,
    write_utility,
)


class BuilderAgent(AgentBase):
    def run(self, ctx: AgentContext) -> int:
        if ctx.issue_number is None:
            print("ERROR: --issue-number is required for the builder agent.")
            return 1
        try:
            issue = agent_utils.get_issue(ctx.repo, ctx.issue_number)
        except agent_utils.GitHubError as exc:
            print(f"ERROR: Failed to fetch issue #{ctx.issue_number}: {exc}")
            return 1
        try:
            prompt = self._compose_prompt(ctx, issue)
            response = cheap_mix(prompt, ctx.models)
            cleaned = response.strip()
            if cleaned == "NO_CHANGES":
                print("LLM returned NO_CHANGES; skipping generation.")
                return 2
            try:
                payload = parse_payload(cleaned)
                target_dir = write_utility(payload, prefix=f"issue-{ctx.issue_number}")
            except PayloadError as exc:
                print(f"ERROR: Invalid utility payload: {exc}")
                self._log_payload_preview(cleaned)
                return 2
            print(f"Utility created under {target_dir}")
            return 0
        except LLMError as exc:
            print(f"ERROR: LLM call failed: {exc}")
            return 1
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: Unexpected failure: {exc}")
            return 1

    def _compose_prompt(self, ctx: AgentContext, issue: dict) -> str:
        title = issue.get("title") or ""
        body = issue.get("body") or ""
        files = self._git_ls_files()
        utilities = list_existing_utils()
        readme_excerpt = self._read_file_excerpt("README.md")
        agents_excerpt = self._read_file_excerpt("AGENTS.md")

        prompt_parts = [
            "You are the ApocalypsAI Builder agent. Design a brand-new community utility.",
            "Follow the repository contract strictly:",
            "- Every run must create a unique folder under utils/<util_name>/ (kebab-case).",
            "- Ship README + code + tests entirely inside that folder.",
            "- Tests cannot use live network calls (use mocks with '# Mock rationale: ...').",
            "- Build something fully documented, tested, and genuinely useful for the community (any language).",
            "- Respond with JSON only; no prose outside the payload.",
            "",
            f"Repository: {ctx.repo}",
            f"Issue #{ctx.issue_number}: {title}",
            "Issue body:",
            body,
            "",
            "Existing utils:",
            "\n".join(utilities) or "(none yet)",
            "",
            f"Random inspiration (feel free to subvert it): {self._random_inspiration()}",
            "Avoid repeating recent themes—especially date/time trackers—unless the issue explicitly demands it.",
            "",
            "Repository files (git ls-files):",
            files,
        ]
        if readme_excerpt:
            prompt_parts.extend(["", "README.md excerpt:", readme_excerpt])
        if agents_excerpt:
            prompt_parts.extend(["", "AGENTS.md excerpt:", agents_excerpt])
        prompt_parts.extend(
            [
                "",
                "Requirements:",
                "- Respond with pure JSON following the schema in AGENTS.md.",
                "- util_name must be unique (≤ 32 chars, kebab-case).",
                "- Include README + at least one tests/ file (runs will fail without tests).",
                "- Document how to run the utility/tests.",
                "- If nothing valuable can be produced, respond exactly `NO_CHANGES`.",
                "- Embrace anarchic creativity: any language/stack is fine if the output is self-contained.",
            ]
        )
        return "\n".join(prompt_parts)

    def _git_ls_files(self) -> str:
        try:
            output = subprocess.check_output(["git", "ls-files"], text=True, stderr=subprocess.DEVNULL)
            lines = output.strip().splitlines()
            return "\n".join(lines[:200])
        except subprocess.CalledProcessError:
            return ""

    def _read_file_excerpt(self, path: str, max_chars: int = 2000) -> str:
        file_path = Path(path)
        if not file_path.exists():
            return ""
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        return text[:max_chars]

    def _log_payload_preview(self, raw: str) -> None:
        preview = summarize_payload(raw)
        if preview:
            print("Payload preview:\n" + preview)

    def _random_inspiration(self) -> str:
        return secrets.choice(INSPIRATIONS)


def _parse_models(value: Optional[str]) -> Optional[dict]:
    if not value:
        return None
    pairs = {}
    entries = value.split(",")
    for entry in entries:
        if "=" not in entry:
            continue
        provider, model = entry.split("=", 1)
        provider = provider.strip()
        model = model.strip()
        if provider and model:
            pairs[provider] = model
    return pairs or None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--pr", type=int)
    parser.add_argument("--mode")
    parser.add_argument(
        "--models",
        help="Comma-separated provider=model overrides (e.g. groq=modelA,openrouter=modelB)",
    )
    args = parser.parse_args()
    ctx = AgentContext(
        repo=args.repo,
        issue_number=args.issue_number,
        pr_number=args.pr,
        mode=args.mode,
        models=_parse_models(args.models),
    )
    code = BuilderAgent().run(ctx)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
