## Nightly GitHub Actions Workflow Linter

This utility is a GitHub Action designed to lint and validate your `.github/workflows/*.yml` files. It helps ensure your automation is well-formed and adheres to common best practices, preventing unexpected workflow failures.

### Usage

To use this action in your workflow, add the following to your `.github/workflows/your-workflow.yml`:

```yaml
name: Validate Workflows

on: [push, pull_request]

jobs:
  lint-workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Workflow Linter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main
        with:
          workflow_path: '.github/workflows/'
```

### Inputs

*   `workflow_path` (optional): The directory containing your GitHub Actions workflow files. Defaults to `.github/workflows/`.

### Outputs

This action does not produce any explicit outputs, but it will fail the job if any linting errors are found.

### Development & Testing

This action is built using a simple shell script and relies on `yamllint` for validation. Tests are included to ensure the linter functions correctly.
