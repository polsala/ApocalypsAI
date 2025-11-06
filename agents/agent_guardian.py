from __future__ import annotations

import argparse
import re
from typing import Optional, Tuple

from . import agent_utils
from .base import AgentBase, AgentContext
from .llm_clients import LLMError, cheap_mix


class GuardianAgent(AgentBase):
    def run(self, ctx: AgentContext) -> int:
        if ctx.issue_number is None:
            print("ERROR: --issue-number is required for the guardian agent.")
            return 1
        try:
            issue = agent_utils.get_issue(ctx.repo, ctx.issue_number)
        except agent_utils.GitHubError as exc:
            print(f"ERROR: Failed to fetch issue #{ctx.issue_number}: {exc}")
            return 1
        try:
            prompt = self._compose_prompt(issue)
            response = cheap_mix(prompt, ctx.models)
            verdict, reason = self._parse_response(response)
        except LLMError as exc:
            print(f"ERROR: LLM call failed: {exc}")
            return 1
        except ValueError as exc:
            print(f"ERROR: Unable to parse guardian response: {exc}")
            return 1
        try:
            comment = f"Verdict: {verdict}\n\nReason: {reason}"
            agent_utils.post_issue_comment(ctx.repo, ctx.issue_number, comment)
            if verdict == "Blocked":
                agent_utils.add_issue_labels(ctx.repo, ctx.issue_number, ["triage/blocked"])
            return 0
        except agent_utils.GitHubError as exc:
            print(f"ERROR: Failed to comment on issue: {exc}")
            return 1

    def _compose_prompt(self, issue: dict) -> str:
        title = issue.get("title") or ""
        body = issue.get("body") or ""
        return "\n".join(
            [
                "You are the ApocalypsAI Guardian agent.",
                "Classify the GitHub issue content into one of: Safe, Suspicious, Blocked.",
                "- Blocked: definite policy violations (abuse, illegal requests, secrets, hate, explicit NSFW, spam).",
                "- Suspicious: borderline or unclear content needing human review.",
                "- Safe: ordinary feature/bug/support requests without policy concerns.",
                "Respond in the format:",
                "Verdict: <Safe|Suspicious|Blocked>",
                "Reason: <short explanation>",
                "",
                "Issue title:",
                title,
                "",
                "Issue body:",
                body,
            ]
        )

    def _parse_response(self, text: str) -> Tuple[str, str]:
        verdict_match = re.search(r"Verdict:\s*(\w+)", text, re.IGNORECASE)
        reason_match = re.search(r"Reason:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
        if not verdict_match or not reason_match:
            raise ValueError("Missing verdict or reason in response")
        verdict_raw = verdict_match.group(1).strip().capitalize()
        if verdict_raw not in {"Safe", "Suspicious", "Blocked"}:
            raise ValueError(f"Invalid verdict: {verdict_raw}")
        reason = reason_match.group(1).strip()
        reason = reason.split("Verdict:", 1)[0].strip()
        if not reason:
            raise ValueError("Reason cannot be empty")
        return verdict_raw, reason


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
    code = GuardianAgent().run(ctx)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
