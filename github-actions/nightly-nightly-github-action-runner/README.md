# Nightly GitHub Action Runner Validator

A reusable GitHub Actions workflow that validates other workflows for syntax, security, and performance best practices.

## Features

- ✅ YAML syntax validation
- ✅ Required fields check (name, on, jobs)
- ✅ Security best practices (no hardcoded secrets, proper permissions)
- ✅ Performance optimization checks (caching, matrix strategy)
- ✅ Action marketplace validation (pinned versions, trusted publishers)
- ✅ Conditional logic validation (if statements, environment variables)

## Usage

### As a reusable workflow

```yaml
name: Validate Workflows
on:
  pull_request:
    paths:
      - '.github/workflows/**'

jobs:
  validate:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-action-runner-validator.yml@main
    with:
      workflow-paths: '.github/workflows'
      strict-mode: true
```

### As a composite action

```yaml
name: CI
on: [push, pull_request]

jobs:
  validate-workflows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate GitHub Actions
        uses: polsala/ApocalypsAI/.github/actions/nightly-github-action-runner-validator/action.yml@main
        with:
          workflow-paths: '.github/workflows'
          strict-mode: true
```

## Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `workflow-paths` | Comma-separated list of paths to check for workflow files | `.github/workflows` |
| `strict-mode` | Enable strict validation (fails on warnings) | `false` |
| `ignore-patterns` | Comma-separated list of file patterns to ignore | `''` |

## Outputs

| Output | Description |
|--------|-------------|
| `validation-result` | JSON result with passed/failed counts and details |
| `has-errors` | Boolean indicating if any validation errors were found |

## Example Output

```
✅ Validating workflow: deploy.yml
  ✓ YAML syntax valid
  ✓ Required fields present
  ✓ No hardcoded secrets
  ✓ Actions use pinned versions
  ✓ Permissions properly scoped

⚠️  Warnings for workflow: ci.yml
  • Consider adding caching for npm dependencies
  • Matrix strategy could be optimized

❌ Errors in workflow: test.yml
  • Missing required 'name' field
  • Uses deprecated action 'actions/checkout@v1'

Summary: 1 passed, 1 warning, 1 failed
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Submit a pull request

## License

MIT
