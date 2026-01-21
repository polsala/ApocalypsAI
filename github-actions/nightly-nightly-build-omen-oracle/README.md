# Nightly Build Omen Oracle

The `nightly-build-omen-oracle` is a whimsical GitHub Action that, upon successful completion of a workflow, bestows a random, cryptic, or encouraging "omen" or "prophecy" upon your pull request or commit status. Let the ancient algorithms whisper the fate of your codebase!

## ✨ Features

*   **Whimsical Omens**: Choose from a predefined list of light-hearted prophecies.
*   **Flexible Posting**: Post omens as PR comments or as a commit status.
*   **Boost Morale**: Add a touch of fun and mystery to your CI/CD pipeline.

## 🚀 Usage

Add this action to your workflow, typically after your build/test steps, and ensure it only runs `if: success()`.

```yaml
name: CI Build and Omen

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run a successful build (example)
      run: echo "Build successful!"

    - name: Post Build Omen
      if: success() # Only run if previous steps succeeded
      uses: polsala/ApocalypsAI/utils/nightly-build-omen-oracle@main # Adjust path if needed
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
        target-type: 'pr-comment' # or 'commit-status'
        status-context: 'Build Omen Oracle' # Only for commit-status
```

### Inputs

*   `github-token`:
    *   **Description**: Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`.
    *   **Required**: `true`
*   `target-type`:
    *   **Description**: Where the omen should be posted.
        *   `pr-comment`: Posts a comment on the associated Pull Request. (Default)
        *   `commit-status`: Sets a commit status on the head commit.
    *   **Required**: `false`
    *   **Default**: `pr-comment`
*   `status-context`:
    *   **Description**: The context string for the commit status. Only relevant if `target-type` is `commit-status`.
    *   **Required**: `false`
    *   **Default**: `build-omen-oracle`

### Outputs

*   `omen`: The specific omen that was generated and posted.

## 🧪 Development & Testing

To run tests locally:

```bash
npm install
npm test
```

The tests use Jest and mock the `@actions/core` and `@actions/github` libraries to ensure deterministic and offline execution.
