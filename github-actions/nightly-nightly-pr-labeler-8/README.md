# Nightly PR Labeler

A tiny GitHub Action that inspects the list of files changed in a pull request and automatically suggests whimsical labels.

## What it does

- **📚 docs-only** – all changed files are documentation (`*.md`, `*.txt`).
- **🧪 test-only** – all changed files are test files (`*_test.*`, `*_spec.*`).
- **⚙️ config-change** – any change to workflow or action configuration (`.github/workflows/*.yml`, `.github/actions/*`).
- **🚀 code-change** – any other source code change.

If multiple categories apply, the action returns a comma‑separated list of labels.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `changed_files` | Comma‑separated list of file paths that were changed in the PR. Usually supplied via `github.event.pull_request.changed_files` or a custom script. | Yes |

## Outputs

| Name | Description |
|------|-------------|
| `labels` | Comma‑separated list of labels that should be applied to the PR. |

## Example workflow

```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Get changed files
        id: files
        uses: jitterbit/get-changed-files@v1
        with:
          format: csv

      - name: Run PR labeler
        uses: ./
        id: labeler
        with:
          changed_files: ${{ steps.files.outputs.all }}

      - name: Apply labels
        uses: actions-ecosystem/action-add-labels@v1
        with:
          labels: ${{ steps.labeler.outputs.labels }}
```

## Testing

Run the bundled shell tests locally:

```bash
bash tests/test_label_pr.sh
```

The tests are deterministic and use only mocked inputs.
