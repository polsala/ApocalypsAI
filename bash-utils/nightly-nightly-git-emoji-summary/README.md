# nightly-git-emoji-summary

Summarize the emojis used in recent Git commit messages, showing a count per emoji and a simple bar chart. Handy for teams that sprinkle emojis in their commits to gauge mood.

## Usage

```bash
./src/git-emoji-summary.sh [N]
```

- `N` (optional) – number of most recent commits to analyze (default: 100).

The script prints lines like:

```
😀 5 #####
🚀 2 ##
```

## Installation

Make the script executable and ensure `git` is in your PATH.

## Testing

Run the test suite:

```bash
bash tests/test_git_emoji_summary.sh
```
