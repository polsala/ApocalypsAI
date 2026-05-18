# Nightly Whimsical Changelog Action

A GitHub Action to automatically compile a delightful changelog from whimsically tagged commit messages.

## ✨ What it does

This action scans your repository's recent commit history for messages that start with a specified prefix (e.g., `[whimsy]`, `[joyful]`). It then compiles these messages into a formatted markdown changelog, which can be saved to a file and used in your release notes, project updates, or just for a daily dose of cheer!

It's perfect for projects that embrace a playful development culture and want to highlight the fun, quirky, or unexpectedly delightful changes alongside the serious ones.

## 🚀 Usage

To use the `nightly-whimsical-changelog-action` in your workflow, add a step like this:

```yaml
name: Generate Whimsical Changelog

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate Whimsical Changelog
        id: generate_changelog
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsical-changelog-action@main # Replace 'main' with your branch/tag
        with:
          commit-prefix: '[whimsy]' # Or '[delight]', '[sparkle]', etc.
          output-file: 'WHIMSICAL_CHANGELOG.md'
          max-commits: '100'
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Changelog as Artifact
        uses: actions/upload-artifact@v4
        with:
          name: whimsical-changelog
          path: WHIMSICAL_CHANGELOG.md

      - name: Read Changelog Content (Optional)
        run: |
          echo "--- Whimsical Changelog Content ---"
          cat WHIMSICAL_CHANGELOG.md
          echo "-----------------------------------"
```

## ⚙️ Inputs

| Input           | Description                                                                 | Required | Default                    |
|-----------------|-----------------------------------------------------------------------------|----------|----------------------------|
| `commit-prefix` | The prefix to look for in commit messages (e.g., `[whimsy]`, `[joyful]`). | `true`   | `[whimsy]`                 |
| `output-file`   | The path to the markdown file where the changelog will be written.          | `true`   | `WHIMSICAL_CHANGELOG.md`   |
| `max-commits`   | The maximum number of recent commits to scan for whimsical messages.        | `true`   | `50`                       |
| `github-token`  | GitHub token with `contents: read` permission. Usually `${{ github.token }}`. | `true`   | `${{ github.token }}`      |

## 📤 Outputs

| Output            | Description                                        |
|-------------------|----------------------------------------------------|
| `changelog-content` | The full content of the generated whimsical changelog as a string. |
| `changelog-path`    | The path to the file where the changelog was written. |

## 🧪 Development & Testing

To run tests locally:

1.  **Install dependencies**:
    ```bash
    npm install
    ```
2.  **Run tests**:
    ```bash
    npm test
    ```
