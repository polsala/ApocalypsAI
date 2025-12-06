# Nightly Issue Summarizer

## Overview

`nightly-issue-summarizer` reads a JSON file containing a list of GitHub issues (as returned by the GitHub REST API) and produces a concise **Markdown** report:

* Total open issues
* Issues per label
* Issues per assignee
* Age buckets ( <1 day, 1‑7 days, >7 days )

The tool is completely self‑contained, has no external dependencies beyond the Python standard library, and can be run locally or in CI pipelines.

## Installation

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

## Usage

```bash
python -m utils.nightly-issue-summarizer.src.summarizer path/to/issues.json > report.md
```

The script prints the markdown to **stdout**; redirect it to a file or feed it into another workflow step.

## Example

Given a file `sample-issues.json`:

```json
[
  {
    "title": "Fix typo in README",
    "labels": [{"name": "documentation"}],
    "assignee": null,
    "created_at": "2025-11-20T12:00:00Z",
    "state": "open"
  },
  {
    "title": "Add unit tests",
    "labels": [{"name": "testing"}, {"name": "enhancement"}],
    "assignee": {"login": "alice"},
    "created_at": "2025-11-15T08:30:00Z",
    "state": "open"
  }
]
```

Running the summarizer yields:

```markdown
# Open Issues Summary (2 total)

## By Label
- documentation: 1
- testing: 1
- enhancement: 1

## By Assignee
- Unassigned: 1
- alice: 1

## By Age
- < 1 day: 0
- 1‑7 days: 1
- > 7 days: 1
```

## Testing

Run the bundled tests with:

```bash
pytest utils/nightly-issue-summarizer/tests
```
