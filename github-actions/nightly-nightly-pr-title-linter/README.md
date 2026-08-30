# nightly-pr-title-linter

A tiny, whimsical GitHub Action that enforces a naming convention on pull‑request titles.

## What it does

- Reads the PR title from the `GITHUB_EVENT_PATH` JSON payload provided by GitHub Actions.
- Checks the title against a user‑supplied regular expression (default: `.*`).
- Emits a success message when the title matches, otherwise fails the job with a clear error.

## Why?

Consistent PR titles make changelogs, release notes, and automated tooling much easier to generate. This action gives you a lightweight, language‑agnostic way to enforce that consistency without pulling in heavy linters.

## Usage

```yaml
name: PR Title Lint
on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  lint-title:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint PR title
        uses: ./nightly-pr-title-linter
        with:
          pattern: '^feat: .+'   # require titles to start with "feat: "
```

### Inputs

| Name    | Description                                 | Required | Default |
|---------|---------------------------------------------|----------|---------|
| `pattern` | Regular expression that the PR title must match (ECMAScript syntax). | No | `.*` |

### Outputs

The action does not produce explicit outputs; it simply succeeds or fails the step.

## Development

The action is implemented as a **composite action** that runs a small Bash script (`src/lint.sh`).

### Running tests locally

```bash
bash tests/test_lint.sh
```

The test suite creates mock `GITHUB_EVENT_PATH` JSON files and verifies both passing and failing scenarios.
