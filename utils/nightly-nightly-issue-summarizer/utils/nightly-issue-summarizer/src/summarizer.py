import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Any


def _parse_iso8601(ts: str) -> datetime:
    """Parse an ISO‑8601 timestamp returned by GitHub.

    GitHub timestamps are always UTC and end with a ``Z``.
    """
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _age_bucket(created: datetime, now: datetime) -> str:
    """Return a human‑readable age bucket.

    * ``< 1 day`` – created less than 24 h ago
    * ``1‑7 days`` – between 1 and 7 days
    * ``> 7 days`` – older than a week
    """
    delta = now - created
    if delta < timedelta(days=1):
        return "< 1 day"
    if delta <= timedelta(days=7):
        return "1‑7 days"
    return "> 7 days"


def summarize_issues(issues: List[Dict[str, Any]]) -> str:
    """Generate a markdown summary for a list of GitHub issue objects.

    The function expects the *raw* JSON objects as returned by the GitHub API
    (i.e. dictionaries with keys like ``title``, ``labels``, ``assignee``,
    ``created_at`` and ``state``). Only issues with ``state == "open"`` are
    considered.
    """
    now = datetime.now(timezone.utc)
    open_issues = [i for i in issues if i.get("state") == "open"]
    total = len(open_issues)

    label_counter: Counter[str] = Counter()
    assignee_counter: Counter[str] = Counter()
    age_counter: Counter[str] = Counter()

    for issue in open_issues:
        # Labels
        for label in issue.get("labels", []):
            label_name = label.get("name", "unknown")
            label_counter[label_name] += 1
        # Assignee (may be null)
        assignee = issue.get("assignee")
        assignee_name = assignee.get("login") if assignee else "Unassigned"
        assignee_counter[assignee_name] += 1
        # Age bucket
        created_at = issue.get("created_at")
        if created_at:
            created_dt = _parse_iso8601(created_at)
            bucket = _age_bucket(created_dt, now)
            age_counter[bucket] += 1
        else:
            age_counter["unknown"] += 1

    lines = [f"# Open Issues Summary ({total} total)", ""]

    # By Label
    lines.append("## By Label")
    if label_counter:
        for label, cnt in sorted(label_counter.items()):
            lines.append(f"- {label}: {cnt}")
    else:
        lines.append("- *No labels*")
    lines.append("")

    # By Assignee
    lines.append("## By Assignee")
    for assignee, cnt in sorted(assignee_counter.items()):
        lines.append(f"- {assignee}: {cnt}")
    lines.append("")

    # By Age
    lines.append("## By Age")
    for bucket in ["< 1 day", "1‑7 days", "> 7 days"]:
        cnt = age_counter.get(bucket, 0)
        lines.append(f"- {bucket}: {cnt}")
    lines.append("")

    return "\n".join(lines)


def _load_issues(path: Path) -> List[Dict[str, Any]]:
    """Load a JSON file containing a list of issue objects.

    # Mock rationale: In unit tests we bypass file I/O by calling ``summarize_issues``
    directly with a Python list, so this helper is exercised only in the CLI path.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON root must be a list of issues")
            return data
    except Exception as exc:
        sys.stderr.write(f"Failed to read issues from {path}: {exc}\n")
        sys.exit(1)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate a markdown summary of open GitHub issues from a JSON export."
    )
    parser.add_argument(
        "issues_json",
        type=Path,
        help="Path to a JSON file containing a list of GitHub issue objects.",
    )
    args = parser.parse_args(argv)
    issues = _load_issues(args.issues_json)
    markdown = summarize_issues(issues)
    sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
