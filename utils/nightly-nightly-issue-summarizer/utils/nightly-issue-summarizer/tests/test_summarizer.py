import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Mock rationale: We construct issue dictionaries directly; no network calls.

from utils.nightly_issue_summarizer.src.summarizer import summarize_issues


def _make_issue(title: str, *, labels=None, assignee=None, created_offset_days: int = 0, state: str = "open"):
    """Helper to create a minimal GitHub issue dict.

    ``created_offset_days`` is the number of days *ago* the issue was created.
    """
    if labels is None:
        labels = []
    created_at = (datetime.now(timezone.utc) - timedelta(days=created_offset_days)).isoformat().replace("+00:00", "Z")
    return {
        "title": title,
        "labels": [{"name": l} for l in labels],
        "assignee": {"login": assignee} if assignee else None,
        "created_at": created_at,
        "state": state,
    }


def test_summarize_basic():
    issues = [
        _make_issue("Doc typo", labels=["documentation"], created_offset_days=0),
        _make_issue("Add tests", labels=["testing", "enhancement"], assignee="alice", created_offset_days=3),
        _make_issue("Refactor module", labels=["enhancement"], assignee="bob", created_offset_days=10),
        _make_issue("Closed issue", labels=["bug"], state="closed", created_offset_days=1),
    ]
    md = summarize_issues(issues)
    # Verify sections exist and counts are correct
    assert "# Open Issues Summary (3 total)" in md
    # Labels
    assert "- documentation: 1" in md
    assert "- testing: 1" in md
    assert "- enhancement: 2" in md
    # Assignees
    assert "- Unassigned: 1" in md  # first issue has no assignee
    assert "- alice: 1" in md
    assert "- bob: 1" in md
    # Age buckets (relative to now)
    assert "- < 1 day: 1" in md  # the doc typo created today
    assert "- 1‑7 days: 1" in md  # add tests created 3 days ago
    assert "- > 7 days: 1" in md  # refactor created 10 days ago


def test_summarize_no_issues(tmp_path: Path):
    # Empty list should produce a summary with zero counts
    md = summarize_issues([])
    assert "# Open Issues Summary (0 total)" in md
    # All counters should be zero
    assert "- *No labels*" in md
    # Age section still lists buckets with zero
    for bucket in ["< 1 day", "1‑7 days", "> 7 days"]:
        assert f"- {bucket}: 0" in md

# CLI integration test (uses a temporary file)
def test_cli_output(tmp_path: Path, capsys):
    issues = [_make_issue("Sample", labels=["bug"], assignee="carol", created_offset_days=2)]
    json_path = tmp_path / "issues.json"
    json_path.write_text(json.dumps(issues), encoding="utf-8")
    # Import the CLI entry point
    from utils.nightly_issue_summarizer.src import summarizer as cli
    cli.main([str(json_path)])
    captured = capsys.readouterr()
    assert "# Open Issues Summary (1 total)" in captured.out
    assert "- bug: 1" in captured.out
    assert "- carol: 1" in captured.out
