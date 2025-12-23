# PR Language Labeler

A GitHub Action that automatically adds language-based labels to a pull request based on the file extensions changed in the PR.

## How it works

1. The action reads the `changed_files` array from the event payload (provided via `GITHUB_EVENT_PATH`).
2. It maps each file extension to a programming language.
3. It creates a set of labels like `lang-python`, `lang-javascript`, etc.
4. The labels are returned as the `labels` output and can be used with the `actions/github-script` or `github` CLI to actually apply them.

## Inputs

| Name | Description | Default |
|------|-------------|---------|
| `label-prefix` | Prefix for generated labels | `lang-` |
| `github-token` | Token with `issues:write` permission (optional, not used in this minimal version) | `""` |

## Outputs

| Name | Description |
|------|-------------|
| `labels` | Comma‑separated list of generated labels |

## Example workflow

```yaml
name: Auto label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - id: labeler
        uses: ./utils/nightly-pr-language-labeler
        with:
          label-prefix: "lang-"
      - name: Apply labels
        uses: actions/github-script@v6
        with:
          script: |
            const labels = "${{ steps.labeler.outputs.labels }}".split(",");
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels
            });
```

## Testing

Run `npm test` inside the utility folder. The test suite uses a mocked event payload and verifies the correct label output.
