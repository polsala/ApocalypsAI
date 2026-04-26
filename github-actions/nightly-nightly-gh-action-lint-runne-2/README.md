## Nightly GitHub Actions Lint Runner

This GitHub Action provides a robust way to lint and validate your `.github/workflows/*.yml` files. It helps catch common syntax errors, potential misconfigurations, and adherence to best practices before they cause issues in your CI/CD pipelines.

### Usage

To use this action in your workflow, add the following to your `.github/workflows/your-workflow.yml` file:

```yaml
name: Lint GitHub Actions Workflows

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Actions Lint Runner
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main
        with:
          # Optional: Specify a glob pattern to include/exclude specific workflow files.
          # Defaults to '**/.github/workflows/*.yml'
          workflow_path: '**/.github/workflows/*.yml'
```

### Inputs

*   `workflow_path` (Optional): A glob pattern to specify which workflow files to lint. Defaults to `**/.github/workflows/*.yml`.

### Outputs

This action does not produce any explicit outputs, but it will fail the job if any linting errors are found.

### Development & Testing

This action is built using a simple shell script and relies on the `actionlint` tool. Tests are included to ensure the core functionality works as expected.

To run tests locally:

1.  Ensure you have Docker installed.
2.  Navigate to the `nightly-gh-action-lint-runner` directory.
3.  Run `docker-compose up --build`.
