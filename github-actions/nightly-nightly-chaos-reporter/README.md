## Nightly Chaos Reporter

This GitHub Action simulates a chaotic event and generates a whimsical report about it. It's designed to add a touch of fun and unpredictability to your CI/CD pipelines, reminding you that even in the face of digital disarray, there's always room for a bit of absurdity.

### Usage

To use this action, add the following to your GitHub Actions workflow file:

```yaml
- name: Run Chaos Reporter
  uses: polsala/ApocalypsAI/utils/github-actions/nightly-chaos-reporter@main
  with:
    chaos_level: "moderate" # Optional: 'low', 'moderate', 'high'
    reporting_style: "poetic" # Optional: 'poetic', 'technical', 'humorous'
```

### Inputs

*   `chaos_level` (optional): The intensity of the simulated chaos. Defaults to `"moderate"`.
    *   `low`: Minor inconveniences, like a rogue semicolon.
    *   `moderate`: Moderate disruptions, such as a server hiccup or a misplaced comma.
    *   `high`: Full-blown digital pandemonium, think rogue AI, temporal anomalies, or a sudden influx of cat memes.
*   `reporting_style` (optional): The tone of the generated report. Defaults to `"poetic"`.
    *   `poetic`: Flowery language, metaphors, and dramatic flair.
    *   `technical`: Dry, factual, and filled with jargon.
    *   `humorous`: Puns, jokes, and lighthearted observations.

### Outputs

*   `chaos_report`: A string containing the generated chaos report.

### Example Workflow

```yaml
name: Chaos Report Example

on:
  workflow_dispatch:

jobs:
  report_chaos:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Chaos Report
        id: chaos_reporter
        uses: polsala/ApocalypsAI/utils/github-actions/nightly-chaos-reporter@main
        with:
          chaos_level: "high"
          reporting_style: "humorous"

      - name: Display Report
        run: | 
          echo "## The Chaos Report ##"
          echo "${{ steps.chaos_reporter.outputs.chaos_report }}"
```
