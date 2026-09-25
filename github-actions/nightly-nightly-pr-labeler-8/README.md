# PR Title Labeler Action

A tiny composite GitHub Action that examines a pull request title and suggests appropriate labels such as `bug`, `enhancement`, `documentation`, or `tests`. It outputs a comma‑separated list of labels which can be used in subsequent steps (e.g., with `gh pr edit`).

## Inputs

- `title` (required): The title of the pull request.

## Outputs

- `labels`: Comma‑separated list of suggested labels. Empty if no keywords match.

## Example workflow

```yaml
name: PR Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./  # uses the action from this repository
        id: labeler
        with:
          title: ${{ github.event.pull_request.title }}

      - name: Apply labels
        if: steps.labeler.outputs.labels != ''
        run: |
          gh pr edit ${{ github.event.pull_request.number }} --add-label ${{ steps.labeler.outputs.labels }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action runs a small Bash script that looks for keyword matches (case‑insensitive) in the title and maps them to predefined labels.

## Testing

Run the provided test script locally:

```bash
bash tests/test_labeler.sh
```
