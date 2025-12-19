# PR Title Labeler Action

A tiny GitHub Action that automatically adds a label to a pull request based on keywords found in the PR title.

## Inputs
- `title` (required): The pull request title.

## Outputs
- `labels` (string): Comma‑separated list of labels the action suggests.

## How it works
The action looks for the following keywords (case‑insensitive):
- `bug` → `bug`
- `feature` or `feat` → `enhancement`
- `doc` or `documentation` → `documentation`
If none match, it returns `question`.

## Usage

```yaml
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./utils/nightly-pr-labeler-action
        id: labeler
        with:
          title: ${{ github.event.pull_request.title }}
      - name: Apply label
        uses: actions-ecosystem/action-add-labels@v1
        with:
          labels: ${{ steps.labeler.outputs.labels }}
```
