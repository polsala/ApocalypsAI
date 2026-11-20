# Nightly PR Whimsy Validator

This GitHub Action ensures your Pull Requests maintain a delightful and optimistic tone by checking for whimsical keywords and flagging grim ones. Keep your codebase cheerful and your team smiling!

## Usage

Add this action to your workflow, typically on `pull_request` events:

```yaml
name: Validate PR Whimsy

on:
  pull_request:
    types: [opened, reopened, edited, synchronize]

jobs:
  whimsy_check:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR for Whimsy
        uses: polsala/ApocalypsAI/nightly-pr-whimsy-validator@main # Replace with actual path/ref
        id: whimsy_validator
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          whimsy-keywords: 'sparkle, joy, delightful, cheerful, fantastic, wondrous, magical, whimsical, gleeful, radiant'
          grim-keywords: 'bug, error, failure, broken, grim, despair, apocalypse, doom, catastrophe'
          min-whimsy-count: 1
          fail-on-grim: true
      - name: Whimsy Report
        run: |
          echo "Whimsy Score: ${{ steps.whimsy_validator.outputs.whimsy-score }}"
          echo "Grim Found: ${{ steps.whimsy_validator.outputs.grim-found }}"
          echo "Validation Status: ${{ steps.whimsy_validator.outputs.validation-status }}"
```

## Inputs

| Name               | Description                                                                 | Required | Default                                                                                              |
|--------------------|-----------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------|
| `github-token`     | GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`).                 | Yes      |                                                                                                      |
| `whimsy-keywords`  | Comma-separated list of keywords considered whimsical. Case-insensitive.    | No       | `sparkle, joy, delightful, cheerful, fantastic, wondrous, magical, whimsical, gleeful, radiant`      |
| `grim-keywords`    | Comma-separated list of keywords considered grim. Case-insensitive.         | No       | `bug, error, failure, broken, grim, despair, apocalypse, doom, catastrophe`                         |
| `min-whimsy-count` | Minimum number of whimsical keywords required in the PR title or body.      | No       | `1`                                                                                                  |
| `fail-on-grim`     | If `true`, the action will fail if any grim keywords are found.             | No       | `true`                                                                                               |

## Outputs

| Name                | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `whimsy-score`      | The total count of whimsical keywords found.                                |
| `grim-found`        | `true` if any grim keywords were found, `false` otherwise.                  |
| `validation-status` | A string indicating the overall validation result: `success`, `warning`, `failure`. |

## Development

To run tests:
```bash
npm install
npm test
```
