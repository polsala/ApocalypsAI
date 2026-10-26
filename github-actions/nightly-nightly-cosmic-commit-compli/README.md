# Nightly Cosmic Commit Complimenter

Bestow celestial praise upon your team's stellar code contributions with the Nightly Cosmic Commit Complimenter! This GitHub Action automatically posts whimsical, cosmic-themed compliments on successfully merged Pull Requests or direct pushes, adding a touch of intergalactic joy to your development workflow.

## ✨ Features

-   **Cosmic Compliments**: A curated list of delightful, space-themed messages.
-   **Flexible Triggering**: Works on `pull_request_target` (for merges) or `push` events.
-   **Customizable**: Use your own compliments or let the cosmos decide!

## 🚀 Usage

Create a workflow file (e.g., `.github/workflows/cosmic-compliments.yml`) in your repository:

```yaml
name: Cosmic Compliments

on:
  pull_request_target:
    types: [closed] # Trigger when a PR is closed (to check for merge)
  push:
    branches:
      - main # Trigger on pushes to main branch

jobs:
  compliment:
    runs-on: ubuntu-latest
    steps:
      - name: Bestow Cosmic Compliment
        uses: polsala/ApocalypsAI/utils/nightly-cosmic-commit-complimenter@main # Adjust 'main' to your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          compliment-target: 'pr-merge' # or 'push'
          # compliment-message: "Your code shines brighter than a supernova!" # Optional: provide a custom message
```

### Inputs

| Name                | Description                                                                 | Required | Default      |
| :------------------ | :-------------------------------------------------------------------------- | :------- | :----------- |
| `github-token`      | Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`.                   | `true`   |              |
| `compliment-target` | The event type to target: `pr-merge` for merged PRs, `push` for direct pushes. | `false`  | `pr-merge`   |
| `compliment-message`| An optional custom compliment message. If provided, overrides random selection. | `false`  | (random)     |

## 🛠️ How it Works

The action listens for `pull_request_target` (closed event) or `push` events.
-   For `pull_request_target`, it checks if the PR was merged. If so, it posts a comment on the PR.
-   For `push` events, it posts a comment on the latest commit.
It selects a random cosmic compliment from its internal list or uses a custom message if provided, then uses the `github-token` to interact with the GitHub API.
