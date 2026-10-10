# Nightly Commit Mood Ring

A GitHub Action that adds a whimsical emoji reaction to Pull Requests based on the sentiment or length of the latest commit message. Give your PRs a little extra personality and feedback!

## ✨ Features

- Analyzes the latest commit message in a Pull Request.
- Assigns an emoji reaction based on keywords (e.g., `fix`, `feat`, `docs`) or message length.
- Supports a variety of fun, apocalypse-appropriate emojis.

## 🚀 Usage

To use the `nightly-commit-mood-ring` action, add it to your workflow, typically on `pull_request` events.

```yaml
name: Commit Mood Ring
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  react_to_commit:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to add reactions
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Get latest commit message
        id: get_message
        run: |
          # Fetch the latest commit message from the PR head
          COMMIT_SHA="${{ github.event.pull_request.head.sha }}"
          COMMIT_MESSAGE=$(git log -1 --format=%B $COMMIT_SHA)
          echo "commit-message=$COMMIT_MESSAGE" >> $GITHUB_OUTPUT

      - name: Add Commit Mood Ring reaction
        uses: polsala/ApocalypsAI/nightly-commit-mood-ring@main # Replace 'main' with your branch/tag if needed
        with:
          commit-message: ${{ steps.get_message.outputs.commit-message }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

- `commit-message`: (Optional) The commit message string to analyze. If not provided, the action will attempt to fetch the latest commit message from the PR context. **For best results and determinism, especially in complex scenarios, it's recommended to explicitly provide this.**
- `github-token`: (Required) Your GitHub token, typically `${{ secrets.GITHUB_TOKEN }}`, with `pull-requests: write` permission to add reactions.

### Outputs

- `reaction-emoji`: The emoji character that was chosen for the reaction.

## 🎭 Emoji Logic

The action prioritizes keyword matches over message length. The order of checks is:

1.  **🚨 Breaking Change**: If message contains "breaking" or "major".
2.  **🩹 Fix/Bug**: If message contains "fix", "bug", or "error".
3.  **🚀 Feature/Add**: If message contains "feat", "add", or "new".
4.  **🧹 Refactor/Clean**: If message contains "refactor" or "clean".
5.  **📚 Docs**: If message contains "docs" or "doc".
6.  **🐛 Short Message**: If message length is less than 10 characters (and no keywords matched).
7.  **📜 Long Message**: If message length is greater than 50 characters (and no keywords matched).
8.  **✨ Medium Message**: If message length is between 10 and 50 characters (and no keywords matched).
9.  **🤖 Default**: If none of the above conditions are met.

## 🧪 Testing

Refer to `tests/test_action.yml` for examples of how the action is tested with various commit messages to ensure deterministic emoji assignment.
