# Nightly GHA Workflow Linter

A GitHub Actions workflow linter that validates YAML syntax, checks for security anti-patterns, and enforces best practices across the repository.

## Features

- **YAML Syntax Validation**: Ensures all workflow files are valid YAML
- **Security Checks**: Detects common security anti-patterns
- **Best Practices**: Enforces repository-specific workflow standards
- **CI Integration**: Can be used as a GitHub Action or standalone script

## Usage

### As a GitHub Action

```yaml
name: Lint Workflows
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint Workflows
        uses: polsala/ApocalypsAI/nightly-gha-workflow-linter@main
```
