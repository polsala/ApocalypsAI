# Workflow Hardening Agent

## 🛡️ Apocalypse-Proof Your GitHub Actions Workflows! 🛡️

The digital wasteland is full of lurking dangers: redundant runs, outdated actions, and ambiguous permissions. The Workflow Hardening Agent is here to help you fortify your GitHub Actions workflows, ensuring they are resilient, efficient, and secure against the inevitable.

This utility scans your `.github/workflows/` directory, identifies common anti-patterns and potential vulnerabilities, and provides actionable recommendations to "harden" your CI/CD pipelines.

## Features

*   **Concurrency Check**: Identifies workflows triggered by `pull_request` or `push` that could benefit from `concurrency` to prevent unnecessary parallel runs.
*   **Action Version Check**: Recommends updating `actions/checkout` to `v3` or later for improved security and features.
*   **Explicit Permissions**: Suggests adding explicit `permissions` blocks to `pull_request` triggered workflows for enhanced security posture.

## Usage

1.  **Install dependencies**:
    ```bash
    pip install pyyaml
    ```
2.  **Run the hardener**:
    ```bash
    python src/workflow_hardener.py --workflow-dir .github/workflows/
    ```
    Replace `.github/workflows/` with the actual path to your workflow directory.

## Example Output

```
Scanning workflows in .github/workflows/

--- Findings for .github/workflows/ci.yml ---
[WARNING] Workflow 'ci.yml' triggered by 'pull_request' or 'push' could benefit from 'concurrency'.
          Consider adding:
          concurrency:
            group: ${{ github.workflow }}-${{ github.ref }}
            cancel-in-progress: true

--- Findings for .github/workflows/deploy.yml ---
[WARNING] Workflow 'deploy.yml' uses 'actions/checkout@v2'. Consider updating to 'v3' or later for security.
[WARNING] Workflow 'deploy.yml' triggered by 'pull_request' lacks an explicit 'permissions' block.
          Consider adding:
          permissions:
            contents: read
            pull-requests: write # Or other minimal permissions required
```

## Development

The agent is written in Python and uses `pyyaml` for parsing workflow files. Tests are self-contained and use mocks to simulate file system interactions.
