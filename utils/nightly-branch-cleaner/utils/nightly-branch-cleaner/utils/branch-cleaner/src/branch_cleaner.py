"""Branch Cleaner utility.

Provides functions to detect stale git branches based on last commit timestamps
and to delete them (mock implementation).
"""

from __future__ import annotations

import datetime
from typing import Dict, List


def _parse_iso(date_str: str) -> datetime.datetime:
    """Parse an ISO‑8601 timestamp (with optional Z) into a timezone‑aware datetime.

    Accepts both ``2024-10-01T12:00:00Z`` and ``2024-10-01T12:00:00+00:00``.
    """
    if date_str.endswith("Z"):
        date_str = date_str[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(date_str)


def is_branch_stale(last_commit_iso: str, days_threshold: int, now: datetime.datetime | None = None) -> bool:
    """Return ``True`` if the branch's last commit is older than *days_threshold* days.

    Parameters
    ----------
    last_commit_iso: str
        ISO‑8601 timestamp of the last commit on the branch.
    days_threshold: int
        Number of days a branch must be inactive to be considered stale.
    now: datetime, optional
        Reference time; defaults to ``datetime.datetime.now(datetime.timezone.utc)``.
    """
    now = now or datetime.datetime.now(datetime.timezone.utc)
    last_commit = _parse_iso(last_commit_iso)
    age = now - last_commit
    return age > datetime.timedelta(days=days_threshold)


def get_stale_branches(
    branches: Dict[str, str],
    days_threshold: int,
    now: datetime.datetime | None = None,
) -> List[str]:
    """Given a mapping ``branch -> last_commit_iso`` return a list of stale branch names.
    """
    stale = [
        name
        for name, iso in branches.items()
        if is_branch_stale(iso, days_threshold, now=now)
    ]
    return stale


def delete_branches(branch_names: List[str]) -> List[str]:
    """Mock deletion of branches.

    In a real implementation this would invoke ``git push origin --delete``.
    Here we simply return the list to indicate success.
    """
    # Mock rationale: no side‑effects, safe for CI.
    return branch_names
