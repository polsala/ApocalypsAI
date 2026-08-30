# nightly-commit-emoji-annotator

A tiny GitHub Action that reads a commit message and posts an emoji reaction to the commit. The emoji is chosen based on simple keyword heuristics, adding a splash of fun to your repository history.

## Features

- Detects common commit prefixes (`fix`, `feat`, `docs`, etc.)
- Posts a reaction emoji via the GitHub REST API
- Fully offline‑testable with a mock `curl`

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github_token` | A token with `repo` scope used to authenticate the API request. | Yes |
| `commit_sha`   | The SHA of the commit to react to. | Yes |
| `message`      | The commit message (if omitted, the action will fetch it via the API). | No |

## Example Workflow

```yaml
name: Emoji‑ify Commits
on:
  push:
    branches: [ main ]

jobs:
  annotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Add Emoji Reaction
        uses: ./nightly-commit-emoji-annotator
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          commit_sha: ${{ github.sha }}
          # optional: message: ${{ github.event.head_commit.message }}
```

## How It Works

The action runs a small Bash script (`src/annotate.sh`). The script:
1. Determines the appropriate emoji based on the commit message.
2. Calls the GitHub Reactions API (`POST /repos/:owner/:repo/commits/:sha/reactions`).
3. Handles errors gracefully and prints a helpful log.

## Testing

Run the tests locally with:
```bash
bash tests/test_annotate.sh
```
The test suite mocks `curl` to avoid network calls and verifies that the correct emoji is selected for various messages.
