# Nightly Commit Message Linter

A tiny, dependency‑free Python utility that checks whether a Git commit message follows the **Conventional Commits** format.

## Features

- Validates the `<type>(<scope>)?: <description>` header.
- Optional body and footer sections are allowed.
- Returns exit code `0` for a valid message, `1` otherwise.
- Can read from a file or STDIN.

## Installation

```sh
pip install .
# or just copy src/commit_linter.py somewhere in your PATH
```

## Usage

```sh
# Validate a file
python -m src.commit_linter path/to/COMMIT_MSG

# Pipe a message
git log -1 --pretty=%B | python -m src.commit_linter
```

## Supported Types

`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

## License

MIT
