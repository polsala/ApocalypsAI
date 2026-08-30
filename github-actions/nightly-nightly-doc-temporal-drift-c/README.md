# Nightly Documentation Temporal Drift Check

A GitHub Action to help prevent "temporal drift" in your project's documentation. This action monitors Pull Requests for significant code changes and suggests reviewing or updating relevant documentation files if they haven't been touched in the same PR.

## 🌌 The Problem: Temporal Drift

In the ever-evolving wasteland of code, documentation can quickly become outdated, leading to confusion and misdirection. This "temporal drift" occurs when code evolves, but its accompanying explanations, guides, or `README.md` files are left behind, creating a rift between reality and perception.

## ✨ The Solution: Drift Detector

This action acts as a vigilant sentinel, detecting potential temporal drift by comparing code changes against documentation updates within a Pull Request. If a substantial amount of code changes are detected without corresponding modifications to specified documentation files, it will flag the PR with a helpful suggestion to review the docs.

## 🚀 Usage

To integrate the `nightly-doc-temporal-drift-check` into your workflow, add it to your `.github/workflows/your-workflow.yml` file, typically on `pull_request` events.

```yaml
name: Doc Drift Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  drift_detection:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required to compare base and head SHAs

      - name: Run Documentation Temporal Drift Check
        id: drift_check
        uses: polsala/ApocalypsAI/github-actions/nightly-doc-temporal-drift-check@main # Adjust path if needed
        with:
          doc-paths: 'README.md,docs/**,CONTRIBUTING.md' # Customize monitored doc files
          code-paths: 'src/**,agents/**,utils/**'         # Customize monitored code paths
          threshold-lines: 20                             # Customize line change threshold
          github-token: ${{ secrets.GITHUB_TOKEN }}       # Required for API access

      - name: Comment on PR if drift detected
        if: steps.drift_check.outputs.drift-detected == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            const comment = `${{ steps.drift_check.outputs.suggestion-comment }}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

## ⚙️ Inputs

| Input             | Description                                                                                             | Default Value               | Required |
| :---------------- | :------------------------------------------------------------------------------------------------------ | :-------------------------- | :------- |
| `doc-paths`       | Comma-separated list of glob patterns for documentation files to monitor (e.g., `"README.md,docs/**"`). | `README.md`                 | `false`  |
| `code-paths`      | Comma-separated list of glob patterns for code directories to monitor for significant changes.          | `src/**,agents/**`          | `false`  |
| `threshold-lines` | Minimum number of lines changed in `code-paths` to trigger a documentation review suggestion.           | `10`                        | `false`  |
| `github-token`    | GitHub token for API calls (e.g., commenting on PRs). Usually `${{ github.token }}`.                   | `${{ github.token }}`       | `true`   |

## 📤 Outputs

| Output             | Description                                        |
| :----------------- | :------------------------------------------------- |
| `drift-detected`   | `true` if potential documentation drift was detected, `false` otherwise. |
| `suggestion-comment` | The markdown-formatted comment text to suggest documentation review. Empty if no drift detected. |

## 🧪 Testing

The action includes a self-contained test workflow (`tests/test.yml`) that simulates various PR scenarios using a dummy git repository. This ensures deterministic and offline testing of the drift detection logic.
