"""emoji_status_broadcaster
================================

Utility functions for converting textual status descriptors into emojis and for creating a concise summary string.

The module is deliberately lightweight – only the Python standard library is used – so it can be dropped into any project without additional dependencies.
"""

from __future__ import annotations

from typing import List, Mapping

# Mapping of known statuses to emojis. Extend as needed.
_STATUS_EMOJI_MAP: Mapping[str, str] = {
    "success": "✅",
    "passed": "✅",
    "ok": "✅",
    "failure": "❌",
    "failed": "❌",
    "error": "❌",
    "in-progress": "⏳",
    "running": "⏳",
    "pending": "⏳",
    "queued": "⏳",
}

# Default emoji for unknown statuses.
_DEFAULT_EMOJI = "❓"


def _normalize_status(status: str) -> str:
    """Return a lower‑cased, stripped version of *status* for lookup.

    The function is isolated to make testing easier and to keep the public API clean.
    """
    return status.strip().lower()


def status_to_emoji(status: str) -> str:
    """Convert a single status string to its corresponding emoji.

    Parameters
    ----------
    status: str
        Human‑readable status (e.g., "success", "failure", "in‑progress").

    Returns
    -------
    str
        The emoji representing the status, or the default unknown emoji.
    """
    normalized = _normalize_status(status)
    return _STATUS_EMOJI_MAP.get(normalized, _DEFAULT_EMOJI)


def summarize_statuses(statuses: List[str]) -> str:
    """Create a compact summary line for a list of statuses.

    The summary consists of the emojis for each status separated by spaces, followed by the total count in parentheses.

    Example
    -------
    >>> summarize_statuses(["success", "failure", "unknown"])
    '✅ ❌ ❓ (3)'
    """
    emojis = [status_to_emoji(s) for s in statuses]
    count = len(statuses)
    return f"{' '.join(emojis)} ({count})"


if __name__ == "__main__":
    # Simple demo when run as a script.
    demo_statuses = ["success", "failure", "in-progress", "unknown"]
    print(summarize_statuses(demo_statuses))
