# Nightly Temporal Phrase Detector

This GitHub Action scans Pull Request titles or commit messages for whimsical phrases that suggest temporal paradoxes or time-traveling shenanigans. It's designed to add a touch of playful vigilance to your repository's timeline, ensuring no rogue commits from the future (or past) slip by unnoticed.

## Usage

To use this action, add a step to your workflow that provides the message you want to scan. This is typically the `github.event.pull_request.title` for PRs or `github.event.head_commit.message` for pushes.

```yaml
name: 'Temporal Scan on PR'
on: pull_request
jobs:
  scan_pr_title:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Temporal Phrase Detector
        id: detect_phrases
        uses: polsala/ApocalypsAI/github-actions/nightly-temporal-phrase-detector@main
        with:
          message: ${{ github.event.pull_request.title }}
          fail-on-paradox: 'true'

      - name: Report Paradox
        if: steps.detect_phrases.outputs.paradox-detected == 'true'
        run: |
          echo "🚨 Temporal Paradox Detected!"
          echo "Detected phrases: ${{ steps.detect_phrases.outputs.detected-phrases }}"
          exit 1 # Or just warn, depending on fail-on-paradox
```

## Inputs

| Name            | Description                                                               | Required | Default |
|-----------------|---------------------------------------------------------------------------|----------|---------|
| `message`       | The string message to scan for temporal phrases (e.g., PR title, commit message). | `true`   |         |
| `fail-on-paradox` | If `true`, the action will fail if any temporal paradox phrase is detected. | `false`  | `false` |

## Outputs

| Name                | Description                                                               |
|---------------------|---------------------------------------------------------------------------|
| `paradox-detected`  | A boolean (`'true'` or `'false'`) indicating if any temporal phrase was found. |
| `detected-phrases`  | A comma-separated string of all detected temporal phrases.                 |

## Temporal Phrases Detected

The action looks for the following (case-insensitive) phrases:

*   `fixed a bug from next week`
*   `reverted a future change`
*   `applied a patch from 2077`
*   `this commit is from another timeline`
*   `pre-emptively fixed`
*   `retroactively applied`
*   `from the future`
*   `from the past that hasn't happened`
*   `temporal anomaly`
*   `time warp`
*   `chronal distortion`

Feel free to contribute more whimsical temporal phrases!
