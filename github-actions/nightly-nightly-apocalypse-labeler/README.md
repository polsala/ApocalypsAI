# Apocalypse Labeler Action

A tiny GitHub Action that scans the title of a pull request for end‑of‑world keywords and, if any match, emits an `apocalypse_label` output with a configurable label (default: `apocalypse-ready`). This can be used in subsequent workflow steps to automatically add labels, post comments, or trigger other “doomsday” processes.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `keywords` | Comma‑separated list of keywords to look for in the PR title. | Yes | – |
| `label` | The label to output when a keyword matches. | No | `apocalypse-ready` |

## Outputs

| Name | Description |
|------|-------------|
| `apocalypse_label` | The label to apply, or an empty string if no keywords matched. |

## Usage

```yaml
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - id: labeler
        uses: ./  # path to this action
        with:
          keywords: "world, end, apocalypse"
          label: "doomsday"
      - if: steps.labeler.outputs.apocalypse_label != ''
        run: |
          gh pr edit ${{ github.event.pull_request.number }} --add-label "${{ steps.labeler.outputs.apocalypse_label }}"
```

The action reads the pull request event from `GITHUB_EVENT_PATH`, which is automatically provided by GitHub Actions.

## Testing

Run the tests locally with:

```sh
npm test
```

The test suite creates mock events and verifies the output logic without contacting the GitHub API.
