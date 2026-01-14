## Nightly GitHub Action Lint Runner

This GitHub Action provides a robust way to lint and validate YAML files within your repository, specifically targeting GitHub Actions workflows and other configuration files.

### Purpose

In the chaotic landscape of code repositories, misconfigured YAML files can lead to broken workflows and unexpected behavior. This action acts as a vigilant guardian, ensuring that your YAML files adhere to basic structural integrity and common best practices before they can cause trouble.

### Features

*   **YAML Linting**: Uses `yamllint` to check for syntax errors and style issues.
*   **Workflow Validation**: Leverages `action-validator` to check GitHub Actions workflow files for structural correctness and common pitfalls.
*   **Customizable Paths**: Allows specifying directories or files to include or exclude from the linting process.
*   **Fail Fast**: Fails the workflow immediately if any linting or validation errors are found.

### Inputs

*   `paths` (optional, default: `.`): A space-separated list of paths to lint. Can be files or directories.
*   `exclude_paths` (optional, default: ``): A space-separated list of paths to exclude from linting.
*   `fail_on_error` (optional, default: `true`): Whether to fail the workflow on any linting or validation error.

### Outputs

*   `lint_status`: The overall status of the linting process ('success' or 'failure').

### Usage

```yaml
name: YAML Lint and Validate

on: [push, pull_request]

jobs:
  lint_yaml:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run YAML Lint and Validate Action
        id: yaml_linter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main # Replace with actual repo/branch/tag
        with:
          paths: ".github/workflows/ .github/workflows/ .github/workflows/"
          exclude_paths: ".github/workflows/example.yml"

      - name: Report Status
        run: echo "Lint status: ${{ steps.yaml_linter.outputs.lint_status }}"
```

### Development & Testing

This action is built using a Docker container. Tests are included within the `tests/` directory and can be run locally using Docker Compose.

**To run tests locally:**

1.  Ensure you have Docker and Docker Compose installed.
2.  Navigate to the `utils/nightly-gh-action-lint-runner/` directory.
3.  Run `docker-compose up --build`.

Tests are designed to be deterministic and offline, using mocked file structures.
