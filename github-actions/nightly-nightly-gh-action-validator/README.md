## Nightly GitHub Action Validator

This utility is a GitHub Action designed to validate the structure and syntax of other GitHub Actions workflow files (`.github/workflows/*.yml`). It aims to catch common errors and ensure workflows adhere to basic structural integrity before they are committed or merged.

### Usage

To use this action in your workflow, add the following steps:

```yaml
- name: Validate GitHub Actions Workflows
  uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-validator@main
  with:
    workflow_path: '.github/workflows/your_workflow.yml'
```

#### Inputs

*   `workflow_path` (required): The path to the GitHub Actions workflow file to validate.

#### Outputs

This action does not produce any explicit outputs, but it will fail the workflow if validation errors are found.

### Development & Testing

This utility is implemented as a GitHub Action workflow itself. The core logic is a simple shell script that uses `yamllint` and `grep` to perform checks.

Tests are included to ensure the validation logic works as expected. These tests are run using `pytest` and mock the file system interactions.
