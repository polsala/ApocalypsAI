from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentContext:
    repo: str
    issue_number: Optional[int] = None
    pr_number: Optional[int] = None
    mode: Optional[str] = None
    models: Optional[Dict[str, str]] = None


class AgentBase:
    def run(self, ctx: AgentContext) -> int:
        """
        Execute the agent and return an exit code.

        0 -> success, 2 -> no-op, 1 -> failure.
        Implementations must catch all exceptions and return a code rather than raising.
        """
        raise NotImplementedError
