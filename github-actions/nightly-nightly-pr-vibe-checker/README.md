# Nightly PR Vibe Checker

This GitHub Action helps maintain a positive and constructive atmosphere in your pull requests by analyzing the sentiment of PR titles and descriptions. If the "vibe score" falls below a configurable threshold, it will provide a friendly suggestion to uplift the mood!

## Features

*   Analyzes PR title and body for positive and negative keywords.
*   Calculates a "vibe score".
*   Sets a status (High, Medium, Low) based on the score.
*   Adds a comment to the PR with a whimsical suggestion if the vibes are low.

## Usage

Add this action to your workflow, typically on `pull_request` events:

```yaml
name: PR Vibe Check

on:
  pull_request:
    types: [opened, reopened, synchronize, edited]

jobs:
  vibe_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run PR Vibe Checker
        uses: polsala/ApocalypsAI/nightly-pr-vibe-checker@main # Replace 'main' with your branch/tag
        id: vibe
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          threshold: 0 # Default is 0, adjust as needed. Higher means more positive required.
          positive-keywords: 'awesome,great,fantastic,delightful,joy,happy,success,celebrate,win,progress,exciting,superb,excellent,brilliant,hooray'
          negative-keywords: 'bug,error,issue,problem,fix,fail,broken,struggle,difficult,challenge,bad,sad,frustrate,annoy,regret'
          check-title: true
          check-body: true

      - name: Report Vibe Status
        run: |
          echo "Vibe Score: ${{ steps.vibe.outputs.vibe-score }}"
          echo "Vibe Status: ${{ steps.vibe.outputs.vibe-status }}"
          echo "Suggestion: ${{ steps.vibe.outputs.suggestion }}"
          if [ "${{ steps.vibe.outputs.vibe-status }}" == "Low" ]; then
            echo "::warning::The PR vibes are a bit low. Consider adding some sparkle!"
          fi
```

## Inputs

*   `github-token`: **Required**. Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`. Used to post comments.
*   `threshold`: **Optional**. The minimum vibe score required for a "High" status. Default: `0`.
*   `positive-keywords`: **Optional**. Comma-separated list of words that increase the vibe score. Default: `awesome,great,fantastic,delightful,joy,happy,success,celebrate,win,progress,exciting,superb,excellent,brilliant,hooray`.
*   `negative-keywords`: **Optional**. Comma-separated list of words that decrease the vibe score. Default: `bug,error,issue,problem,fix,fail,broken,struggle,difficult,challenge,bad,sad,frustrate,annoy,regret`.
*   `check-title`: **Optional**. Boolean. Whether to include the PR title in the vibe check. Default: `true`.
*   `check-body`: **Optional**. Boolean. Whether to include the PR body in the vibe check. Default: `true`.

## Outputs

*   `vibe-score`: The calculated numerical vibe score.
*   `vibe-status`: The categorized status: `High`, `Medium`, or `Low`.
*   `suggestion`: A whimsical suggestion message if the vibe status is `Low`.

## Development

This action is written in JavaScript.

To run tests:
```bash
npm install
npm test
```
