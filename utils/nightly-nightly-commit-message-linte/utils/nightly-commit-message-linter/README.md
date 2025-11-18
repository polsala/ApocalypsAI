# Nightly Commit Message Linter

## Overview

`nightly-commit-message-linter` is a lightweight, zero‑dependency Python utility that checks whether a commit message follows the **Conventional Commits** format:

```
<type>(<scope>)?: <description>

<body>

<footer>
```

Only the first line (the *subject*) is validated; the body and footer are optional and ignored for the purpose of this linter.

## Why?

* Enforce a consistent commit style across a repository.
* Plug into CI workflows (GitHub Actions, GitLab CI, etc.) to fail builds on malformed messages.
* No external services – runs entirely offline.

## Installation

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-commit-message-linter
```

## Usage

```bash
# Lint a commit message file
python -m nightly_commit_message_linter src/commit_message.txt

# Pipe a message via stdin
echo "feat(parser): add new AST node" | python -m nightly_commit_message_linter
```

The command exits with:
* `0` – the message is valid.
* `1` – the message is invalid (details printed to stdout).

## Development

Run the test suite with:

```bash
pytest utils/nightly-commit-message-linter/tests
```

## License

MIT – see the top‑level `LICENSE` file.
