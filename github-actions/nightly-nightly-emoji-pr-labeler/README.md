# Emoji PR Labeler

A whimsical yet practical GitHub Action that scans the pull‑request title for specific emojis and automatically adds corresponding labels.

## How it works

| Emoji | Label |
|-------|-------|
| 🐛    | `bug` |
| ✨    | `enhancement` |
| 📚    | `documentation` |
| 🚀    | `feature` |

The action reads the `pr_title` input, maps any recognised emojis to their labels, removes duplicates, and outputs a comma‑separated list via the `labels` output.

## Usage

```yaml
name: PR Emoji Labeller
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Apply emoji labels
        id: emoji_labeler
        uses: ./
        with:
          pr_title: "${{ github.event.pull_request.title }}"

      - name: Add labels to PR
        if: steps.emoji_labeler.outputs.labels != ''
        uses: actions-ecosystem/action-add-labels@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          labels: ${{ steps.emoji_labeler.outputs.labels }}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `pr_title` | The title of the pull request to scan for emojis. | Yes |

## Outputs

| Name | Description |
|------|-------------|
| `labels` | Comma‑separated list of labels derived from emojis. |

## Development

The core logic lives in `src/labeler.sh`. Tests can be run locally with:

```bash
bash tests/test_labeler.sh
```

## License

MIT © ApocalypsAI
