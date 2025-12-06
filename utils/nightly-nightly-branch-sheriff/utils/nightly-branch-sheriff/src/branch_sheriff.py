import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from typing import List, Tuple


def _parse_iso(date_str: str) -> datetime:
    """Parse an ISO‑8601 timestamp (with optional Z) into a timezone‑aware datetime."""
    # datetime.fromisoformat does not understand trailing 'Z', so replace it.
    if date_str.endswith('Z'):
        date_str = date_str[:-1] + '+00:00'
    return datetime.fromisoformat(date_str)


def find_stale_branches(
    branch_info: List[Tuple[str, str]],
    max_age_days: int,
    now: datetime | None = None,
) -> List[str]:
    """Return branch names whose last commit is older than *max_age_days*.

    Parameters
    ----------
    branch_info:
        A list of ``(branch_name, last_commit_iso)`` tuples.
    max_age_days:
        Age threshold in days.
    now:
        Optional current time for testing; defaults to ``datetime.now(timezone.utc)``.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=max_age_days)
    stale: List[str] = []
    for name, iso in branch_info:
        try:
            commit_dt = _parse_iso(iso)
        except Exception as exc:
            raise ValueError(f"Invalid ISO timestamp for branch '{name}': {iso}") from exc
        if commit_dt < cutoff:
            stale.append(name)
    return stale


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Detect stale git branches.")
    parser.add_argument(
        "--branches",
        required=True,
        help="JSON list of [branch_name, last_commit_iso] tuples.",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        required=True,
        help="Age threshold in days.",
    )
    args = parser.parse_args()
    try:
        branch_list: List[Tuple[str, str]] = json.loads(args.branches)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse --branches JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        stale = find_stale_branches(branch_list, args.max_age_days)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(stale))


if __name__ == "__main__":
    _cli()
