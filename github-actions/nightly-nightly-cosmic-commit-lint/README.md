# Nightly Cosmic Commit Lint

A GitHub Action that brings cosmic order to your commit messages! This utility enforces conventional commit standards and adds a touch of whimsical cosmic wisdom or space-themed emojis if your commit message is deemed too bland or earthly.

## ✨ Features

- **Conventional Commit Enforcement**: Checks if your commit message adheres to standard prefixes like `feat:`, `fix:`, `docs:`, etc.
- **Cosmic Whimsy**: For short or generic commit messages, it suggests a random space-themed emoji or a piece of "cosmic wisdom" to inspire more descriptive commits.
- **Configurable Strictness**: Choose your desired "cosmic level" of linting, from gentle "stardust" nudges to "blackhole" strictness that can fail your CI.
- **Action Outputs**: Provides `lint-status` (success, warning, failure) and `cosmic-suggestion` for further workflow logic.

## 🚀 Usage

To use the Nightly Cosmic Commit Lint in your GitHub Actions workflow, add it as a step in your `.github/workflows/*.yml` file.

```yaml
name: Cosmic CI

on:
  pull_request:
    types: [opened, reopened, synchronize]
  push:
    branches:
      - main
      - master

jobs:
  lint_commits:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required to get commit history for some scenarios

      - name: Get commit message (for push events)
        id: get_commit_message
        if: github.event_name == 'push'
        run: |
          echo "commit_message=$(git log -1 --pretty=%B)" >> $GITHUB_OUTPUT

      - name: Run Cosmic Commit Lint (Pull Request)
        if: github.event_name == 'pull_request'
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-commit-lint@main # Replace 'main' with your branch/tag
        id: pr_lint
        with:
          # The action will automatically try to get the PR title if commit-message is not provided
          # commit-message: ${{ github.event.pull_request.title }}
          cosmic-level: 'nebula' # Options: 'stardust', 'nebula', 'blackhole'

      - name: Run Cosmic Commit Lint (Push)
        if: github.event_name == 'push'
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-commit-lint@main # Replace 'main' with your branch/tag
        id: push_lint
        with:
          commit-message: ${{ steps.get_commit_message.outputs.commit_message }}
          cosmic-level: 'stardust' # Options: 'stardust', 'nebula', 'blackhole'

      - name: Check Lint Results
        if: always()
        run: |
          # For PRs
          if [ "${{ github.event_name }}" == "pull_request" ]; then
            echo "PR Lint Status: ${{ steps.pr_lint.outputs.lint-status }}"
            echo "PR Cosmic Suggestion: ${{ steps.pr_lint.outputs.cosmic-suggestion }}"
            if [ "${{ steps.pr_lint.outputs.lint-status }}" == "failure" ]; then
              echo "::error::Cosmic Lint failed for PR. Please refine your commit message."
              exit 1
            fi
          fi
          # For Pushes
          if [ "${{ github.event_name }}" == "push" ]; then
            echo "Push Lint Status: ${{ steps.push_lint.outputs.lint-status }}"
            echo "Push Cosmic Suggestion: ${{ steps.push_lint.outputs.cosmic-suggestion }}"
            if [ "${{ steps.push_lint.outputs.lint-status }}" == "failure" ]; then
              echo "::error::Cosmic Lint failed for Push. Please refine your commit message."
              exit 1
            fi
          fi
```

### Inputs

| Name             | Description                                                                  | Required | Default      |
| :--------------- | :--------------------------------------------------------------------------- | :------- | :----------- |
| `commit-message` | The commit message string to lint. If empty, the action attempts to derive it from `github.event.pull_request.title` (for PRs) or `github.event.head_commit.message` (for pushes). | `false`  | `''`         |
| `cosmic-level`   | Determines the strictness and whimsy level.                                  | `false`  | `'stardust'` |
|                  | - `stardust`: Gentle warnings for non-conventional or bland messages.        |          |              |
|                  | - `nebula`: Warnings for non-conventional or bland messages, more assertive suggestions. |          |              |
|                  | - `blackhole`: Fails the workflow for non-conventional or bland messages, strict suggestions. |          |              |

### Outputs

| Name                | Description                                                              |
| :------------------ | :----------------------------------------------------------------------- |
| `lint-status`       | The overall status of the linting: `success`, `warning`, or `failure`. |
| `cosmic-suggestion` | A whimsical cosmic suggestion if the commit message was deemed bland.   |

## 🌌 Cosmic Levels Explained

- **Stardust (Default)**: Your commit messages are like nascent stars. We'll gently guide them towards conventionality and add a sprinkle of cosmic charm if they're a bit dim. Warnings are issued, but the workflow won't fail.
- **Nebula**: Your commits are forming complex structures. We expect more clarity. Non-conventional or bland messages will result in warnings, and suggestions will be more direct.
- **Black Hole**: Only the most perfectly formed, descriptive, and conventional commits can escape the gravitational pull of this level. Any deviation results in a workflow failure, demanding a re-evaluation of your message.

## 🧪 Testing

The action includes a `tests/test_lint.sh` script that can be run locally to verify the core logic of the `src/lint.sh` script.

```bash
cd github-actions/nightly-cosmic-commit-lint
./tests/test_lint.sh
```

This script mocks the GitHub Actions environment by directly passing commit messages and cosmic levels, capturing stdout for assertions.
