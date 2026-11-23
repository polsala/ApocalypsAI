# Nightly Mood Monitor Action

![Mood Monitor Logo](https://raw.githubusercontent.com/polsala/ApocalypsAI/main/docs/assets/mood-monitor.png) <!-- Placeholder for a whimsical logo -->

This GitHub Action acts as the ApocalypsAI community's emotional barometer and thematic guide. It scans new or updated issue and pull request titles and descriptions for sentiment and adherence to the 'post-apocalyptic scavenger' theme. If it detects a deviation or an opportunity for thematic enhancement, it will leave a whimsical, yet helpful, comment.

## 🌟 Features

*   **Sentiment Analysis**: Detects overall positive, negative, or neutral tones.
*   **Thematic Consistency**: Checks for keywords related to the ApocalypsAI universe (e.g., 'wasteland', 'anomaly', 'scavenge', 'bunker').
*   **Whimsical Suggestions**: Provides gentle nudges and rephrasing ideas to align with the community's desired mood and theme.
*   **Configurable Keywords**: Customize positive, negative, and thematic keywords to suit evolving community needs.

## 🚀 Usage

To use the Nightly Mood Monitor Action, add a new workflow file (e.g., `.github/workflows/mood-monitor.yml`) to your repository:

```yaml
name: Nightly Mood Monitor

on:
  issues:
    types: [opened, edited]
  pull_request_target:
    types: [opened, edited]

jobs:
  monitor_mood:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run Mood Monitor
        uses: polsala/ApocalypsAI/.github/actions/nightly-mood-monitor-action@main # Adjust path if action is moved
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          positive-keywords: 'great, excellent, fantastic, awesome, success, triumph, victory, hope, progress, thriving'
          negative-keywords: 'bug, error, failure, broken, terrible, awful, disaster, void, despair, struggle'
          thematic-keywords: 'wasteland, scavenger, anomaly, bunker, temporal, rift, relic, survival, resource, mutation'
          neutral-threshold: 0.1 # Adjust sensitivity for mood detection
```

### Inputs

*   `github-token`: **Required**. Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`, to allow the action to post comments.
*   `positive-keywords`: A comma-separated string of words indicating a positive sentiment. Defaults to a sensible list.
*   `negative-keywords`: A comma-separated string of words indicating a negative sentiment. Defaults to a sensible list.
*   `thematic-keywords`: A comma-separated string of words relevant to your repository's theme. Defaults to ApocalypsAI-specific terms.
*   `neutral-threshold`: A float between 0 and 1. If the absolute difference between positive and negative scores is below this threshold, the mood is considered neutral. Defaults to `0.1`.

### Outputs

*   `mood-status`: The detected mood of the content. Possible values: `positive`, `negative`, `neutral`, `thematic`, `off-topic`.

## 🛠️ Development

### Local Testing

To test the action locally, you'll need Node.js installed. The tests use Jest.

```bash
cd github-actions/nightly-mood-monitor-action
npm install
npm test
```

### Contributing

Feel free to suggest improvements, add more sophisticated sentiment analysis, or expand the thematic keyword lists. Every contribution helps maintain the ApocalypsAI spirit!
