# Nightly Workflow Chrono-Sentry

A GitHub Action that detects anomalous step durations in workflows, reporting "temporal distortions" to keep your CI/CD speedy.

## 🌌 The Chrono-Sentry's Mission

In the vast, ever-flowing river of CI/CD, sometimes a step takes an unexpected detour, a "temporal distortion" that slows down your precious build time. The Nightly Workflow Chrono-Sentry stands guard, meticulously observing the flow of time within your workflow steps. If a step dares to linger too long, or perhaps finishes with an unnatural haste (though we mostly care about the lingering!), the Sentry will sound the alarm, helping you pinpoint and rectify these chronal anomalies.

## ✨ Features

*   **Temporal Anomaly Detection**: Flags workflow steps whose duration significantly exceeds the average duration of other steps within the same job.
*   **Configurable Sensitivity**: Adjust the `threshold_multiplier` to fine-tune how sensitive the Sentry is to distortions.
*   **Minimum Duration Filter**: Ignore fleeting steps with `min_duration_seconds` to focus on substantial time-consumers.
*   **Detailed Anomaly Report**: Provides a JSON output with all detected distortions, including job name, step name, actual duration, and average job duration.
*   **Whimsical Warnings**: Emits warnings and a failure message with a touch of temporal flair when distortions are found.

## 🚀 Usage

Add the `nightly-workflow-chrono-sentry` action to your workflow, ideally as a final step after all other jobs have completed, or within a specific job you want to monitor.

```yaml
name: CI/CD with Chrono-Sentry

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate a quick task
        run: sleep 2

      - name: Simulate a normal task
        run: sleep 10

      - name: Simulate a *potentially* slow task
        run: sleep 25 # This might be flagged if other steps are much faster

      - name: Run Chrono-Sentry
        id: chrono-sentry
        uses: polsala/ApocalypsAI/nightly-workflow-chrono-sentry@main # Replace with actual path
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          threshold_multiplier: '2.0' # Flag if step is > 2x average
          min_duration_seconds: '5'   # Only consider steps longer than 5 seconds

      - name: Report Anomalies
        if: steps.chrono-sentry.outputs.anomalies_detected == 'true'
        run: |
          echo "🚨 Temporal Distortions Detected! 🚨"
          echo "${{ steps.chrono-sentry.outputs.anomaly_report }}"
          exit 1 # Fail the workflow if anomalies are critical
```

### Inputs

| Name                   | Description                                                                                                                            | Required | Default |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------ |
| `github_token`         | **GitHub Token for API access.** Use `${{ secrets.GITHUB_TOKEN }}`.                                                                    | `true`   |         |
| `threshold_multiplier` | A step is flagged if its duration is more than this multiplier times the average step duration in its job.                             | `false`  | `2.0`   |
| `min_duration_seconds` | Minimum duration (in seconds) for a step to be considered for anomaly detection. Shorter steps are ignored to focus on significant tasks. | `false`  | `5`     |

### Outputs

| Name                 | Description                                                              |
| :------------------- | :----------------------------------------------------------------------- |
| `anomalies_detected` | `true` if any temporal distortions (anomalies) were detected, `false` otherwise. |
| `anomaly_report`     | A JSON string containing details of detected temporal distortions.       |

## 🧪 Testing

To run tests locally:

1.  Navigate to the `nightly-workflow-chrono-sentry` directory.
2.  Run `npm install` in the `src/` directory to install dependencies.
3.  Run `npm test` in the `src/` directory.

```bash
cd nightly-workflow-chrono-sentry/src
npm install
npm test
```
