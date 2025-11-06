from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents import agent_utils
from agents.base import AgentBase, AgentContext
from agents.llm_clients import LLMError, cheap_mix

MAX_WORDS = 1500


class ReviewerAgent(AgentBase):
    def run(self, ctx: AgentContext) -> int:
        if ctx.pr_number is None:
            print("ERROR: --pr is required for the reviewer agent.")
            return 1
        try:
            pr = agent_utils.get_pr(ctx.repo, ctx.pr_number)
            files = agent_utils.get_pr_files(ctx.repo, ctx.pr_number)
            comments = agent_utils.get_issue_comments(ctx.repo, ctx.pr_number)
            diff = agent_utils.get_pr_diff(ctx.repo, ctx.pr_number)
        except agent_utils.GitHubError as exc:
            print(f"ERROR: Failed to collect PR details: {exc}")
            return 1

        try:
            prompt = self._compose_prompt(pr, files, comments, diff)
            response = cheap_mix(prompt, ctx.models)
            comment = self._prepare_comment(response)
            if not comment:
                print("ERROR: Reviewer LLM returned empty response.")
                return 1
            agent_utils.post_pr_comment(ctx.repo, ctx.pr_number, comment)
            return 0
        except LLMError as exc:
            print(f"ERROR: LLM call failed: {exc}")
            return 1
        except agent_utils.GitHubError as exc:
            print(f"ERROR: Failed to post review comment: {exc}")
            return 1
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: Unexpected reviewer failure: {exc}")
            return 1

    def _compose_prompt(
        self,
        pr: Dict[str, object],
        files: list[Dict[str, object]],
        comments: list[Dict[str, object]],
        diff: str,
    ) -> str:
        pr_title = pr.get("title", "")
        pr_body = pr.get("body", "")
        file_summaries = []
        for file_info in files:
            filename = file_info.get("filename", "")
            status = file_info.get("status", "")
            additions = file_info.get("additions", 0)
            deletions = file_info.get("deletions", 0)
            summary = f"- {filename} ({status}, +{additions}/-{deletions})"
            file_summaries.append(summary)
        summarized_comments = []
        for item in comments[-5:]:
            user = (item.get("user") or {}).get("login", "unknown")
            body = (item.get("body") or "").strip()
            if body:
                summarized_comments.append(f"- {user}: {body[:400]}")
        trimmed_diff = self._trim_diff(diff, 12000)

        prompt_sections = [
            "You are the ApocalypsAI Reviewer agent.",
            "Produce a single consolidated review comment in Markdown (≤1500 words).",
            "Follow this exact structure:",
            "✅ What’s solid",
            "🧪 Tests",
            "🔒 Security",
            "🧩 Docs/DX",
            "🧱 Mocks/Fakes",
            "Each section must contain actionable feedback. Use bullet lists when multiple points exist. Include code snippets where helpful.",
            "Do not approve or request changes explicitly; only provide review commentary.",
            "",
            f"PR Title: {pr_title}",
            "PR Body:",
            pr_body or "(no description)",
            "",
            "Changed files:",
            "\n".join(file_summaries) or "(none listed)",
            "",
            "Recent PR comments (latest first):",
            "\n".join(reversed(summarized_comments)) or "(no comments)",
            "",
            "Diff snippet (truncated to maintain context):",
            trimmed_diff,
        ]
        return "\n".join(prompt_sections)

    def _trim_diff(self, diff: str, limit: int) -> str:
        if len(diff) <= limit:
            return diff
        head = diff[: limit // 2]
        tail = diff[-limit // 2 :]
        return f"{head}\n...\n{tail}"

    def _prepare_comment(self, response: str) -> str:
        comment = response.strip()
        if not comment:
            return ""
        words = comment.split()
        if len(words) > MAX_WORDS:
            comment = " ".join(words[:MAX_WORDS])
        if "✅" not in comment:
            comment = f"✅ What’s solid\n- (not provided)\n\n{comment}"
        required_sections = ["✅", "🧪", "🔒", "🧩", "🧱"]
        if not all(section in comment for section in required_sections):
            # Encourage structure by inserting headers when missing
            segments = []
            for label in ["✅ What’s solid", "🧪 Tests", "🔒 Security", "🧩 Docs/DX", "🧱 Mocks/Fakes"]:
                if label.split()[0] in comment:
                    continue
                segments.append(f"{label}\n- (pending)")
            if segments:
                comment = "\n\n".join(segments) + "\n\n" + comment
        return comment.strip()


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
    code = ReviewerAgent().run(ctx)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
