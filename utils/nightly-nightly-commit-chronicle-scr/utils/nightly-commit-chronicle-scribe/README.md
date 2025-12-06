# Nightly Commit Chronicle Scribe

## Purpose

The `nightly-commit-chronicle-scribe` is a whimsical utility designed to distill the essence of your recent Git commits into a structured, human-readable summary. Think of it as your personal historian, documenting the 'chronicle' of changes in your repository. It's particularly useful for generating quick changelogs, release notes, or simply getting an overview of development activity.

It parses commit messages, categorizing them by conventional commit types (e.g., `feat:`, `fix:`, `docs:`, `chore:`) and presenting them in a clean, consolidated format.

## Usage

Navigate to the root of your Git repository and run the `scribe.py` script.

```bash
python3 utils/nightly-commit-chronicle-scribe/src/scribe.py
```

### Options

*   `--count <N>`: Summarize the last `N` commits. Defaults to 10.
*   `--since <DATE>`: Summarize commits since a specific date (e.g., `2023-01-01`).
*   `--until <DATE>`: Summarize commits until a specific date (e.g., `2023-12-31`).
*   `--format <FORMAT>`: Output format. Currently only `markdown` is supported (default).

### Examples

Summarize the last 5 commits:
```bash
python3 utils/nightly-commit-chronicle-scribe/src/scribe.py --count 5
```

Summarize commits since a specific date:
```bash
python3 utils/nightly-commit-chronicle-scribe/src/scribe.py --since 2023-10-26
```

## Example Output (Markdown)

```markdown
# Commit Chronicle

## ✨ Features

*   `abcdef1` (Alice) Add new user authentication module
*   `fedcba9` (Bob) Implement dark mode toggle

## 🐛 Bug Fixes

*   `1234567` (Charlie) Fix pagination issue on search results

## 📚 Documentation

*   `7654321` (David) Update README with new usage instructions

## 🧹 Chores

*   `abcabc1` (Eve) Bump dependency 'requests' to 2.28.1
```
