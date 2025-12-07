# Nightly Repo Mood Ring

The `nightly-repo-mood-ring` GitHub Action is a whimsical utility designed to gauge the emotional "mood" of your repository based on recent commit messages. It scans for keywords indicating positive, negative, or neutral sentiment and provides a summary of the repository's current vibe. Keep an eye on your repo's emotional well-being!

## Features

*   **Sentiment Analysis**: Scans recent commit messages for predefined positive, negative, and neutral keywords.
*   **Mood Reporting**: Outputs a concise "mood" (e.g., "Joyful", "Stressed", "Optimistic", "Concerned", "Neutral").
*   **Summary**: Provides a brief summary of the analysis.
*   **Configurable**: Adjust the number of commits to analyze.

## Usage

To use this action, add it as a step in your GitHub Actions workflow.

```yaml
name: Repo Mood Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  check_mood:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Analyze Repo Mood
        id: mood_ring
        uses: polsala/ApocalypsAI/github-actions/nightly-repo-mood-ring@main # Replace 'main' with your branch/tag
        with:
          commit-count: 20 # Optional: Number of recent commits to analyze (default: 10)

      - name: Report Mood
        run: |
          echo "The current repository mood is: ${{ steps.mood_ring.outputs.repo-mood }}"
          echo "Summary: ${{ steps.mood_ring.outputs.mood-summary }}"
          # You can use this output to trigger further actions, like posting to Slack,
          # creating an issue if the mood is 'Stressed', etc.
```

## Inputs

*   `commit-count` (optional): The number of recent commit messages to analyze. Defaults to `10`.

## Outputs

*   `repo-mood`: The determined mood of the repository (e.g., `Joyful`, `Stressed`, `Optimistic`, `Concerned`, `Neutral`).
*   `mood-summary`: A brief textual summary of the analysis.

## How it Works

The action uses a simple keyword-based sentiment analysis. It counts occurrences of positive, negative, and neutral words within the commit messages. The overall mood is then determined by comparing these counts using a set of heuristic rules.

### Mood Heuristics

*   **Joyful**: Significantly more positive than negative keywords.
*   **Stressed**: Significantly more negative than positive keywords.
*   **Optimistic**: More positive than negative keywords.
*   **Concerned**: More negative than positive keywords.
*   **Neutral**: Roughly equal positive/negative or predominantly neutral keywords.

## Development

### Testing

Tests are located in `tests/test_mood_analyzer.sh`. They use a mocked `git` command to provide deterministic commit message inputs.
