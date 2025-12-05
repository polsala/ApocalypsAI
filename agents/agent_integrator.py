from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.base import AgentBase, AgentContext
from agents.llm_clients import LLMError, call_provider
from agents.util_generation import (
    PayloadError,
    list_existing_utils,
    parse_payload,
    summarize_payload,
    write_utility,
)


class IntegratorAgent(AgentBase):
    def run(self, ctx: AgentContext) -> int:
        if (ctx.mode or "").lower() != "nightly":
            print("ERROR: --mode nightly is required for the integrator agent.")
            return 1
        try:
            prompt = self._compose_prompt(ctx)
            response, provider = call_provider(prompt, ctx.models)
            cleaned = response.strip()
            if cleaned == "NO_CHANGES":
                print("LLM returned NO_CHANGES; skipping nightly drop.")
                return 2
            try:
                payload = parse_payload(cleaned)
                target_dir = write_utility(payload, prefix="nightly")
            except PayloadError as exc:
                print(f"ERROR: Invalid utility payload: {exc}")
                self._log_payload_preview(cleaned)
                return 2
            # Output metadata for PR description (JSON format for easy parsing)
            metadata = {
                "util_name": payload.name,
                "summary": payload.summary,
                "provider": provider,
                "target_dir": str(target_dir),
                "file_count": len(payload.files),
            }
            print(f"__METADATA_START__{json.dumps(metadata)}__METADATA_END__")
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
        
        # Rotate through different language/tech suggestions to encourage diversity
        tech_suggestions = [
            ("Rust", "rust-utils", "a high-performance CLI tool, system utility, or performance-critical component"),
            ("Go", "go-utils", "a concurrent service, network tool, or distributed utility"),
            ("Bash", "bash-utils", "a shell script for automation, system administration, or DevOps tasks"),
            ("TypeScript", "typescript-utils", "a type-safe utility, library, or command-line tool"),
            ("React", "react-webpage", "an interactive web interface, dashboard, or visualization tool"),
            ("JavaScript/Node", "node-utils", "a cross-platform utility, API, or automation script"),
            ("Docker", "docker-tools", "a containerized tool, service, or development environment"),
            ("GitHub Actions", "github-actions", "a reusable workflow, action, or CI/CD component"),
            ("Terraform", "terraform-modules", "an infrastructure-as-code module or cloud resource template"),
            ("Ansible", "ansible-playbooks", "an automation playbook, role, or configuration management tool"),
        ]
        suggestion = random.choice(tech_suggestions)
        
        prompt_parts = [
            "You are the ApocalypsAI Nightly Integrator agent.",
            "Invent a whimsical-yet-useful standalone utility for the community.",
            "",
            "=== V2 PATH CLASSIFICATION ===",
            "Utilities are now organized by classifier-based paths:",
            "- Choose the MOST APPROPRIATE language and technology for your creative idea",
            "- Specify a 'classifier' field in your JSON response",
            "- Available classifiers: python-utils, rust-utils, bash-utils, react-webpage, github-actions,",
            "  devops-tools, docker-tools, cli-apps, web-apis, js-utils, node-utils, typescript-utils,",
            "  data-scripts, test-suite-tools, monitoring-scripts, infra-automation, go-utils, java-utils,",
            "  cpp-utils, ansible-playbooks, terraform-modules, k8s-resources, ci-cd-pipelines,",
            "  database-scripts, ml-notebooks, api-clients, and more.",
            "",
            "=== TECHNOLOGY DIVERSITY CHALLENGE ===",
            f"TODAY'S SUGGESTION: Try building {suggestion[2]} using {suggestion[0]} (classifier: {suggestion[1]})!",
            "",
            "Other great options to explore:",
            "- Rust for blazing-fast CLI tools and system utilities",
            "- Go for concurrent services and network tools",
            "- Bash for quick automation and DevOps scripts",
            "- TypeScript/React for web UIs and interactive tools",
            "- Docker for containerized applications",
            "- GitHub Actions for workflow automation",
            "- Terraform/Ansible for infrastructure tools",
            "- SQL for database utilities",
            "",
            "BE CREATIVE! Explore different languages and tools. Avoid repetitive Python scripts.",
            "Consider what would be fun, useful, AND showcase different technologies.",
            "",
            "=== CORE REQUIREMENTS ===",
            "- Pack README + runnable code + automated tests inside the folder.",
            "- Focus on something genuinely useful while staying self-contained.",
            "- Tests must be deterministic and offline (use mocks with '# Mock rationale:').",
            "- Respond with JSON only; no prose outside the payload.",
            "",
            f"Repository: {ctx.repo}",
            "Existing utils (organized by classifier):",
            "\n".join(utilities[-50:]) if len(utilities) > 50 else "\n".join(utilities) or "(none yet)",
            "" if len(utilities) <= 50 else f"... and {len(utilities) - 50} more. AVOID duplicating existing utilities!",
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
                "JSON Response Schema:",
                "{",
                '  "util_name": "nightly-<creative-name> (kebab-case, ≤ 32 chars)",',
                '  "summary": "one sentence overview",',
                '  "classifier": "appropriate-category (e.g., rust-utils, react-webpage, bash-utils)",',
                '  "files": [',
                '    {"path": "README.md", "description": "docs + usage", "content": "<full file contents>"},',
                '    {"path": "src/main.ext", "description": "implementation", "content": "<code>"},',
                '    {"path": "tests/test_main.ext", "description": "tests", "content": "<tests>"}',
                "  ]",
                "}",
                "",
                "CRITICAL JSON FORMATTING RULES:",
                "1. ALL content fields MUST use proper JSON string escaping",
                "2. Escape backslashes: \\ becomes \\\\",
                "3. Escape quotes: \" becomes \\\"",
                "4. Use \\n for newlines, \\t for tabs",
                "5. Do NOT use markdown formatting inside JSON strings",
                "6. Do NOT truncate the JSON - ensure it's complete and valid",
                "7. Test your JSON is valid before responding",
                "",
                "If nothing safe or novel comes to mind, respond exactly `NO_CHANGES`.",
                "Otherwise output pure JSON describing util_name/summary/classifier/files.",
                "Utilities without at least one tests/ file will be rejected, so include runnable tests.",
                "CHALLENGE YOURSELF: Use a different language/technology than you used last time!",
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
