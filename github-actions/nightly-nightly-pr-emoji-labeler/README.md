# nightly-pr-emoji-labeler

## Overview

`nightly-pr-emoji-labeler` is a tiny GitHub Action that automatically adds an emoji‑based label to a pull request when it is opened. The label is chosen from the first word of the PR title, making it easy to spot bug fixes, new features, documentation updates, and more at a glance.

## How it works

1. The action reads the pull‑request event payload supplied by GitHub (`GITHUB_EVENT_PATH`).
2. It extracts the PR number and title.
3. Based on the first word of the title (case‑insensitive) it maps to an emoji:
   - `fix` / `bug` → 🐛
   - `feat` / `feature` → ✨
   - `docs` → 📚
   - `refactor` → 🔧
   - `test` / `tests` → ✅
   - `chore` → 🧹
   - anything else → ❓
4. It creates a label named "<emoji> PR" (e.g., "🐛 PR") and adds it to the PR via the GitHub REST API.

## Usage

Add the following step to your workflow (or use the provided example workflow):

```yaml
name: PR Emoji Labeler
on:
  pull_request:
    types: [opened]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Add emoji label
        uses: ./github-actions/nightly-pr-emoji-labeler
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

> **Note**: The action is a Docker‑based action, so it works on any runner that supports Docker.

## Testing

The utility includes an offline test script (`tests/test_action.sh`) that mocks the GitHub environment and the `curl` command to verify that the correct label payload is generated.

## License

MIT © ApocalypsAI
