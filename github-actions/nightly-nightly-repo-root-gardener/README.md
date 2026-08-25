# Nightly Repository Root Gardener

A GitHub Action to cultivate a healthy repository root by ensuring essential files are present, forbidden files are absent, and optionally checking for basic content patterns like license headers. Keep your project's foundational structure pristine!

## 🌸 Features

*   **Required File Check:** Verifies the existence of critical files (e.g., `LICENSE`, `README.md`, `CONTRIBUTING.md`).
*   **Forbidden File Check:** Ensures certain files (e.g., old config backups, temporary files) are *not* present.
*   **License Header Cultivation (Optional):** Scans common source code files (`.py`, `.js`, `.go`, `.rs`, `.ts`, `.java`, `.cpp`) for a basic license header pattern.
*   **Detailed Report:** Provides a JSON output detailing all findings.
*   **Issue Creation (Optional):** Can create a GitHub Issue or comment on a PR if discrepancies are found, guiding contributors to "tend their garden."

## 🌿 Usage

Create a workflow file (e.g., `.github/workflows/root-gardener.yml`):

```yaml
name: Root Gardener Check

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  schedule:
    - cron: '0 0 * * *' # Daily at midnight UTC

jobs:
  garden_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Root Gardener
        id: gardener
        uses: polsala/ApocalypsAI/nightly-repo-root-gardener@main # Replace 'main' with your branch/tag
        with:
          required_files: 'README.md,LICENSE,CONTRIBUTING.md'
          forbidden_files: '.DS_Store,temp_config.bak'
          check_license_header: true
          github_token: ${{ secrets.GITHUB_TOKEN }} # Optional, for creating issues/comments

      - name: Report Findings
        run: |
          echo "Gardener Status: ${{ steps.gardener.outputs.status }}"
          echo "Gardener Report:"
          echo "${{ steps.gardener.outputs.report }}" | jq .
        shell: bash
```

### Inputs

*   `required_files`: (Optional) A comma-separated string of file paths that *must* exist in the repository root. Default: `''`.
*   `forbidden_files`: (Optional) A comma-separated string of file paths that *must not* exist in the repository root. Default: `''`.
*   `check_license_header`: (Optional) Boolean. If `true`, checks common source files for a basic license header. Default: `false`.
*   `license_header_pattern`: (Optional) A regex pattern to match for license headers. Only used if `check_license_header` is `true`. Default: `'(Copyright|License)'`.
*   `github_token`: (Optional) `GITHUB_TOKEN` or a PAT. If provided and issues are found, the action will create a new issue or comment on the current PR. Default: `''`.

### Outputs

*   `status`: `success` if no issues found, `failure` otherwise.
*   `report`: A JSON string containing a detailed report of all checks and findings.

## 🐛 Development & Testing

To test this action locally or in a CI environment, you can use the provided `tests/test_action.yml` workflow. This workflow sets up various repository states and runs the action against them, asserting the outputs.

```bash
# Example of running tests (requires act or similar local runner, or push to a test branch)
# act -W .github/workflows/test_action.yml
```

The tests simulate different repository conditions (missing files, forbidden files, files without headers) and verify that the action correctly identifies them and reports the findings.
