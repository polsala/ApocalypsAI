# nightly-emoji-commit-suggester

Suggests the perfect emoji for your commit message, making your git history more expressive.

## Installation

```bash
npm install -g ./path/to/nightly-emoji-commit-suggester
```

## Usage

```bash
emoji-commit \"feat: add new login flow\"
🚀 Feature

# Or pipe a commit message
cat commit.txt | emoji-commit
🐛 Bug
```

## How it works

The tool scans the commit message for keywords and maps them to a set of emojis. It supports common Conventional Commits types such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, and `BREAKING CHANGE`.
