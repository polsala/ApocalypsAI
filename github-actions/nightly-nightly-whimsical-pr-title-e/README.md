# Nightly Whimsical PR Title Enforcer

A GitHub Action that enforces whimsical naming conventions for Pull Request titles, ensuring they meet specific patterns and length requirements. This helps maintain the ApocalypsAI community's unique and playful tone in all contributions.

## Usage

Add this action to your workflow, typically on `pull_request` events.

```yaml
name: Enforce Whimsical PR Title
on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  enforce_title:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR Title Whimsicality
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsical-pr-title-enforcer@main # Replace 'main' with your branch/tag
        id: check_title
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pattern: '^(Whisper of the Void|Temporal Tear|Cosmic Quirk|Apocalyptic Doodle): .+'
          min-length: '25'
          fail-on-mismatch: 'true'
      - name: Report Whimsicality Status
        run: |
          echo "Is Whimsical: ${{ steps.check_title.outputs.is-whimsical }}"
          echo "Message: ${{ steps.check_title.outputs.message }}"
```

## Inputs

| Name             | Description                                                                                             | Required | Default Value                                       |
|------------------|---------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| `github-token`   | GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`).                                             | `true`   |                                                     |
| `pattern`        | Regular expression pattern the PR title must match.                                                     | `true`   | `^(Whisper of the Void|Temporal Tear|Cosmic Quirk): .+$` |
| `min-length`     | Minimum required length for the PR title.                                                               | `true`   | `20`                                                |
| `fail-on-mismatch` | Whether the action should fail the workflow if the title does not meet the requirements.                | `true`   | `true`                                              |

## Outputs

| Name           | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| `is-whimsical` | `true` if the PR title matches the pattern and length, `false` otherwise. |
| `message`      | A message indicating the result of the check.                             |

## Development & Testing

This action is built with Node.js.

To run tests:
```bash
npm install
npm test
```
