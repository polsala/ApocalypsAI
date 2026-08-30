# nightly-commit-reverter

Utility to automatically revert commits whose messages match a given pattern.

## Usage

```bash
./commit-reverter.sh <regex>
```

Scans the current git repository's history (from HEAD backwards) for commits whose commit message matches the provided regular expression. For each matching commit, creates a new revert commit preserving the original author.

## Options

- `<regex>`: POSIX extended regular expression to match commit messages.

## Example

```bash
# Revert all commits containing the word "WIP"
./commit-reverter.sh "WIP"
```

## Safety

- The script operates on the current branch only.
- It creates revert commits; original commits remain in history.
