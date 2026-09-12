# Nightly Whimsical Commit Curator

A GitHub Action that curates and summarizes recent whimsical commit messages from your repository. Perfect for generating fun release notes, boosting team morale, or simply appreciating the lighter side of development.

## ✨ Features

*   Scans commits within a specified timeframe.
*   Identifies "whimsical" commits based on keywords, emoji patterns, and a heuristic for positive language.
*   Outputs a JSON array of full whimsical commit messages.
*   Generates a human-readable summary string for easy integration into release notes or Slack messages.

## 🚀 Usage

To use the `Nightly Whimsical Commit Curator` action, add it to your workflow file (e.g., `.github/workflows/whimsy.yml`):

```yaml
name: Curate Whimsical Commits

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  curate_whimsy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Curate Whimsical Commits
        id: whimsical_curator
        uses: polsala/ApocalypsAI/utils/nightly-whimsical-commit-curator@main # Adjust path if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          days-ago: '14' # Look back 14 days
          keywords: 'sparkle, magic, joy, delight, fun, yay'
          emoji-patterns: ':sparkles:,:tada:,:rocket:,:unicorn:'

      - name: Output Whimsical Summary
        run: |
          echo "Whimsical Commits Found:"
          echo "${{ steps.whimsical_curator.outputs.whimsical-summary }}"
          echo "Raw JSON:"
          echo "${{ steps.whimsical_curator.outputs.whimsical-commits }}"

      - name: Post to Slack (Example)
        if: success() && steps.whimsical_curator.outputs.whimsical-commits != '[]'
        uses: slackapi/slack-github-action@v1.24.0
        with:
          slack-bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: '#general'
          payload: |
            {
              "text": "A fresh batch of whimsical commits has been curated! 🎉\n${{ steps.whimsical_curator.outputs.whimsical-summary }}"
            }
```

## ⚙️ Inputs

*   `github-token`:
    *   **Description**: GitHub token for API access. Usually `${{ github.token }}`.
    *   **Required**: `true`
*   `days-ago`:
    *   **Description**: Number of days to look back for commits.
    *   **Required**: `false`
    *   **Default**: `7`
*   `keywords`:
    *   **Description**: Comma-separated list of keywords (case-insensitive) to identify whimsical commits (e.g., "sparkle, magic, joy").
    *   **Required**: `false`
    *   **Default**: `''`
*   `emoji-patterns`:
    *   **Description**: Comma-separated list of regex patterns for emojis (case-insensitive) to identify whimsical commits (e.g., `":sparkles:",":tada:"`).
    *   **Required**: `false`
    *   **Default**: `''`

## 📦 Outputs

*   `whimsical-commits`:
    *   **Description**: A JSON array of the full commit messages identified as whimsical.
*   `whimsical-summary`:
    *   **Description**: A human-readable, formatted string summarizing the whimsical commits.

## 🧪 Development & Testing

This action is written in JavaScript.

1.  **Install dependencies**:
    ```bash
    npm install
    ```
2.  **Run tests**:
    ```bash
    npm test
    ```
    Tests are designed to be deterministic and offline, mocking GitHub API calls using `jest-when`.
3.  **Build for distribution (optional, handled by CI normally)**:
    ```bash
    npm run build
    ```
    This bundles `src/main.js` into `dist/index.js` for efficient execution in GitHub Actions.
