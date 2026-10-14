# Nightly PR Cheer-Up Bot

A GitHub Action that injects a dose of whimsical positivity into your Pull Requests! If a PR's title or description seems a bit too serious or lacks a certain sparkle, this bot will gently suggest adding a whimsical emoji or phrase to brighten the digital wasteland.

## ✨ Why use this?

In the grim future of the ApocalypsAI, every bit of cheer helps maintain morale. This action encourages a more positive and engaging tone in your development workflow, fostering a happier and more collaborative community.

## 🚀 How it works

1.  **Monitors PRs**: Runs on `pull_request_target` or `pull_request` events.
2.  **Scans for Sparkle**: Checks the PR title and description for the presence of predefined whimsical emojis or phrases.
3.  **Suggests Cheer**: If no "sparkle" is detected, it adds a comment to the PR, suggesting the author add a whimsical touch. The suggestion includes a randomly chosen phrase from a configurable list.

## ⚙️ Usage

Add the following step to your GitHub Actions workflow (e.g., in `.github/workflows/pr_cheer.yml`):

```yaml
name: PR Cheer-Up

on:
  pull_request_target:
    types: [opened, edited, reopened, synchronize]

jobs:
  cheer_up:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to comment on PRs
    steps:
      - name: Inject Whimsical Positivity
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-cheer-up-bot@main # Replace 'main' with your branch/tag
        id: cheer_up_step
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Customize the whimsical phrases
          # whimsical_phrases: '🚀, 🌌, 👽, 🤖, 🌟, 💖, 🎉, 🥳, 🍀, 💡, ✨'
      - name: Check if cheered up
        if: steps.cheer_up_step.outputs.cheered_up == 'true'
        run: echo "A cheer-up suggestion was made!"
```

### Inputs

*   `github_token`:
    *   **Description**: GitHub token for commenting on PRs.
    *   **Required**: `true`
    *   **Example**: `${{ secrets.GITHUB_TOKEN }}`
*   `whimsical_phrases`:
    *   **Description**: Comma-separated list of whimsical phrases/emojis to suggest. If the PR content doesn't contain any of these, a suggestion will be made.
    *   **Required**: `false`
    *   **Default**: `'✨, 🌟, 😄, 🌈, 🚀, 💖, 💡, 🎉, 🥳, 🍀'`

### Outputs

*   `cheered_up`:
    *   **Description**: `true` if a cheer-up suggestion was made, `false` otherwise.
    *   **Example**: `if: steps.cheer_up_step.outputs.cheered_up == 'true'`

## 🧪 Development & Testing

To test this action locally, you can use the provided `tests/test_main.sh` script. This script mocks the GitHub Actions environment variables (`GITHUB_EVENT_PATH`, `GITHUB_OUTPUT`) and external commands (`jq`, `gh`) to provide deterministic and offline testing.

```bash
# From the root of the nightly-pr-cheer-up-bot directory
./tests/test_main.sh
```
