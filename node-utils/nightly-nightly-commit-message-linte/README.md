# nightly-commit-message-linter

A whimsical yet practical Node.js CLI that validates your Git commit messages against the Conventional Commits specification and, if you wish, adds a friendly emoji suggestion.

## Installation

```sh
npm install -g .
```

## Usage

Validate a commit message from a file:

```sh
node src/main.js path/to/COMMIT_MSG
```

Or pipe it via stdin:

```sh
cat COMMIT_MSG | node src/main.js
```

Add `--suggest-emoji` to get a random (but deterministic) emoji prefix:

```sh
node src/main.js --suggest-emoji COMMIT_MSG
```

## What it checks

- Commit type must be one of `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`, `revert`.
- Optional scope in parentheses.
- Description must start with a lowercase letter and not end with a period.
- First line length must not exceed 72 characters.

If all checks pass, the tool prints:

```
✅ Commit message looks good 👍
```

Otherwise it prints error details to stderr and exits with code 1.
