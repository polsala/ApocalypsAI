import pytest
from commit_message_analyzer.commit_analyzer import analyze

# Mock rationale: All tests use static strings; no external I/O.


def test_valid_commit_with_scope_and_footer():
    msg = "feat(parser): add new parsing logic\n\nThis improves performance.\n\nBREAKING CHANGE: parser API changed"
    res = analyze(msg)
    assert res["is_valid"] is True
    assert res["type"] == "feat"
    assert res["scope"] == "(parser)"
    assert res["subject"] == "add new parsing logic"
    assert res["body"] == ["This improves performance."]
    assert res["footers"] == {"BREAKING CHANGE": "parser API changed"}
    assert res["errors"] == []


def test_invalid_type():
    msg = "unknown: do something"
    res = analyze(msg)
    assert res["is_valid"] is False
    assert "Unknown commit type" in res["errors"][0]


def test_missing_subject():
    msg = "feat():"
    res = analyze(msg)
    assert res["is_valid"] is False
    assert "Subject is missing" in res["errors"][0]


def test_without_scope_and_body():
    msg = "fix: correct typo"
    res = analyze(msg)
    assert res["is_valid"] is True
    assert res["type"] == "fix"
    assert res["scope"] is None
    assert res["subject"] == "correct typo"
    assert res["body"] == []
    assert res["footers"] == {}


def test_empty_message():
    msg = ""
    res = analyze(msg)
    assert res["is_valid"] is False
    assert "Commit message is empty" in res["errors"][0]
