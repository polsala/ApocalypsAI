# nightly-commit-emoji-annotator

A whimsical Bash utility that reads the git commit history and annotates each commit with an emoji representing its type (e.g., 🚀 for features, 🐛 for bug fixes, 📚 for docs). Useful for a quick visual overview of a repository.

## Usage

```sh
./src/commit-emoji.sh [options] [<git-repo-path>]
```

**Options**
- `-n <num>`: number of recent commits to show (default `10`).
- `-h`      : display this help message.

If no repository path is supplied, the current directory is used.

## How it works

The script runs `git log` and matches keywords in the commit subject line to emojis via an associative array. If no keyword matches, a question‑mark emoji (❓) is shown.

## Testing

```sh
bash tests/test_commit_emoji.sh
```

The test replaces the `git` binary with a mock that returns a deterministic log, then verifies the script's output.
