# GitHub Action: YAML Linter & Validator

This GitHub Action provides a robust way to lint and validate all YAML files within your repository. It helps catch syntax errors, structural issues, and potential misconfigurations before they cause problems.

## Features

*   **YAML Linting**: Uses `yamllint` to enforce style and detect common errors.
*   **Schema Validation (Optional)**: Can optionally validate YAML files against a provided JSON schema.
*   **Customizable Rules**: Supports `.yamllint` configuration files for tailored linting rules.

## Usage

Add this to your `.github/workflows/yaml-lint.yml` file:

```yaml
name: YAML Lint and Validate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint_yaml:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run YAML Linter and Validator
        uses: polsala/ApocalypsAI/github-actions/nightly-gh-action-lint-check@main
        with:
          # Optional: Path to a JSON schema file for validation
          # schema_path: .github/workflows/schemas/my_schema.json
          # Optional: Specify a custom .yamllint config file
          # yamllint_config: .github/workflows/.yamllint_custom
          # Optional: Glob pattern to include specific files
          # include_globs: "**/*.yml"
          # Optional: Glob pattern to exclude specific files
          # exclude_globs: "**/vendor/**"
