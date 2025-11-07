from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.base import AgentBase, AgentContext
from agents.llm_clients import LLMError, cheap_mix
from agents.util_generation import (
    PayloadError,
    list_existing_utils,
    parse_payload,
    write_utility,
)


class IntegratorAgent(AgentBase):
    def run(self, ctx: AgentContext) -> int:
        if (ctx.mode or "").lower() != "nightly":
            print("ERROR: --mode nightly is required for the integrator agent.")
            return 1
        try:
            prompt = self._compose_prompt(ctx)
            response = cheap_mix(prompt, ctx.models)
            cleaned = response.strip()
            if cleaned == "NO_CHANGES":
                print("LLM returned NO_CHANGES; skipping nightly drop.")
                return 2
            try:
                payload = parse_payload(cleaned)
                target_dir = write_utility(payload, prefix="nightly")
            except PayloadError as exc:
                print(f"ERROR: Invalid utility payload: {exc}")
                return 2
            print(f"Nightly utility created under {target_dir}")
            return 0
        except LLMError as exc:
            print(f"ERROR: LLM call failed: {exc}")
            return 1
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: Unexpected failure: {exc}")
            return 1

    def _compose_prompt(self, ctx: AgentContext) -> str:
        files = self._git_ls_files()
        utilities = list_existing_utils()
        readme_excerpt = self._read_file_excerpt("README.md")
        agents_excerpt = self._read_file_excerpt("AGENTS.md")
        prompt_parts = [
            "You are the ApocalypsAI Nightly Integrator agent.",
            "Invent a whimsical-yet-useful standalone utility for the community:",
            "- Always create a brand-new folder under utils/<util_name>/ (kebab-case).",
            "- Pack README + runnable code + automated tests inside the folder.",
            "- Focus on something genuinely useful (any language/tooling) while staying self-contained.",
            "- Tests must be deterministic and offline (use mocks with '# Mock rationale:').",
            "- Respond with JSON only; no prose outside the payload.",
            "",
            f"Repository: {ctx.repo}",
            "Existing utils:",
            "\n".join(utilities) or "(none yet)",
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
                "If nothing safe or novel comes to mind, respond exactly `NO_CHANGES`.",
                "Otherwise output pure JSON per AGENTS.md describing util_name/summary/files.",
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
    code = IntegratorAgent().run(ctx)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
