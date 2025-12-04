# Nightly Commit Message Analyzer

This utility validates and parses commit messages according to the [Conventional Commits](https://www.conventionalcommits.org/) specification. It is intentionally lightweight, written in pure Python 3.11, and has no external dependencies.

## Features

- Detects the commit type, optional scope, and subject.
- Extracts body paragraphs and footers (e.g., `BREAKING CHANGE`).
- Returns a structured dictionary with validation status and detailed errors.
- Can be imported into CI scripts, pre‑commit hooks, or used as a standalone CLI.

## Usage

```python
from commit_message_analyzer import analyze

msg = "feat(parser): add new parsing logic\n\nThis improves performance.\n\nBREAKING CHANGE: parser API changed"
result = analyze(msg)
print(result)
```

## API

```python
analyze(message: str) -> Dict[str, Any]
```

The returned dictionary contains:

- `is_valid` (bool)
- `type` (str or None)
- `scope` (str or None)
- `subject` (str or None)
- `body` (List[str])
- `footers` (Dict[str, str])
- `errors` (List[str])

## Testing

Run the tests with `pytest`:

```bash
pytest utils/nightly-commit-message-analyzer/utils/commit-message-analyzer/tests
```

All tests are deterministic and offline; no external network calls are required.
