# Nightly PR Praise Action

This GitHub Action automatically posts a whimsical, encouraging comment to Pull Requests once they are successfully merged. It's designed to celebrate contributions and boost morale within the ApocalypsAI community, reminding everyone that even in the digital wasteland, good work is appreciated.

## Features

*   **Automated Praise**: Posts a random, pre-defined, or custom praise message upon PR merge.
*   **Whimsical & Themed**: Default messages are crafted with the ApocalypsAI universe in mind.
*   **Customizable**: Easily provide your own set of praise messages.

## Usage

To use this action, add a new step to your workflow that triggers on `pull_request` events with `types: [closed]`. Ensure the action runs only if the PR was merged.

```yaml
name: PR Praise

on:
  pull_request:
    types:
      - closed

jobs:
  praise_merged_pr:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == true
    steps:
      - name: Give Whimsical Praise
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-praise-action@main # Replace 'main' with your branch/tag if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Provide custom praise messages (each line is a separate message)
          # praise-messages: |
          #   'Your code is a beacon in the digital night!'
          #   'The circuits sing your praises, survivor!'
          #   'Another bug vanquished, another feature born. Magnificent!'
```

## Inputs

*   `github-token` (required):
    The GitHub token used to authenticate API calls. Typically `${{ secrets.GITHUB_TOKEN }}`.
*   `praise-messages` (optional):
    A multiline string where each line is a custom praise message. If provided, the action will randomly select one from these messages. If not provided, a set of default ApocalypsAI-themed messages will be used.

## Outputs

None.

## Development

To run tests locally:

```bash
npm install
npm test
```
