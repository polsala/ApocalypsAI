# Nightly GitHub Actions Workflow Linter

This utility is a GitHub Action designed to lint and validate your `.github/workflows/*.yml` files. It helps catch common syntax errors, potential misconfigurations, and adherence to best practices for GitHub Actions.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/your_workflow.yml` file:

```yaml
- name: Run GitHub Actions Linter
  uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-lint-check@main
  with:
    # Optional: Specify a path to check if not the entire .github/workflows directory
    # workflow_path: '.github/workflows/my_specific_workflow.yml'
```

## Inputs

*   `workflow_path` (optional): A glob pattern or specific path to the GitHub Actions workflow file(s) to check. Defaults to `'.github/workflows/*.yml'`.

## Outputs

This action does not produce any explicit outputs, but it will fail the workflow if any linting errors are found.

## Development & Testing

This action is built using a simple shell script and relies on the `actionlint` tool. Tests are included to verify its functionality.
