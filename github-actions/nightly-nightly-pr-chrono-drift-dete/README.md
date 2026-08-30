# Nightly PR Chrono-Drift Detector

A GitHub Action that scans Pull Request titles and descriptions for "temporal anomalies" or "chrono-drift." This helps maintain the integrity of your project's timeline by flagging:

1.  **Future-Dated Claims**: Mentions of dates in the PR content that are significantly in the future, potentially indicating premature announcements or misaligned planning.
2.  **Stale Pull Requests**: PRs that have been open for an extended period without recent activity, suggesting they might be forgotten or "lost in time."

By integrating this action into your CI/CD, you can ensure that PRs reflect the current state of development and prevent temporal inconsistencies from creeping into your codebase.

## Usage

To use the Nightly PR Chrono-Drift Detector, add it as a step in your GitHub Actions workflow. It's typically run on `pull_request` or `pull_request_target` events.

```yaml
name: Chrono-Drift Check

on:
  pull_request:
    types: [opened, reopened, synchronize, edited]

jobs:
  chrono_drift_detection:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Chrono-Drift Detector
        id: detector
        uses: polsala/ApocalypsAI/nightly-pr-chrono-drift-detector@main # Replace with actual path if different
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          future-date-threshold-days: '14' # Flag dates more than 14 days in the future
          stale-pr-threshold-days: '45'    # Flag PRs open for more than 45 days without recent updates
          ignore-drafts: 'true'            # Do not check draft PRs for staleness

      - name: Report Chrono-Drift
        if: steps.detector.outputs.chrono-drift-detected == 'true'
        run: |
          echo "Chrono-Drift Detected! Details:"
          echo "${{ steps.detector.outputs.drift-details }}" | jq .
          exit 1 # Fail the workflow if drift is detected
```

### Inputs

| Name                           | Description                                                                                             | Type    | Default | Required |
| :----------------------------- | :------------------------------------------------------------------------------------------------------ | :------ | :------ | :------- |
| `github-token`                 | **Required**. GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`).                               | `string`|         | `true`   |
| `future-date-threshold-days`   | Number of days into the future a mentioned date can be before being flagged as a "future-dated claim."  | `integer`| `7`     | `false`  |
| `stale-pr-threshold-days`      | Number of days a PR can be open without significant activity before being considered "stale."           | `integer`| `30`    | `false`  |
| `ignore-drafts`                | Set to `true` to skip the "stale PR" check for draft pull requests.                                     | `boolean`| `true`  | `false`  |

### Outputs

| Name                      | Description                                                                 | Type      |
| :------------------------ | :-------------------------------------------------------------------------- | :-------- |
| `chrono-drift-detected`   | `true` if any chrono-drift was detected, `false` otherwise.                 | `boolean` |
| `drift-details`           | A JSON string containing an array of detected drift anomalies and their details. | `string`  |

## Development

### Setup

```bash
npm install
```

### Running Tests

```bash
npm test
```

### Local Testing (using `act`)

You can test this action locally using `act`.

1.  Install `act`: `brew install act` (macOS) or follow instructions [here](https://github.com/nektos/act#installation).
2.  Create a dummy workflow file (e.g., `.github/workflows/test-local.yml`):

    ```yaml
    name: Local Chrono-Drift Test

    on: [pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Run Chrono-Drift Detector
            id: detector
            uses: ./ # Refers to the current directory
            with:
              github-token: ${{ secrets.GITHUB_TOKEN }} # A dummy token is fine for local testing
              future-date-threshold-days: '7'
              stale-pr-threshold-days: '30'
              ignore-drafts: 'true'
          - name: Output results
            run: |
              echo "Chrono-Drift Detected: ${{ steps.detector.outputs.chrono-drift-detected }}"
              echo "Details: ${{ steps.detector.outputs.drift-details }}"
    ```
3.  Simulate a `pull_request` event:

    ```bash
    act pull_request --event-payload '{ "pull_request": { "number": 1, "title": "Test PR", "body": "This PR is for a feature launching on 2025-01-01.", "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z", "draft": false } }'
    ```
    Adjust the `event-payload` to test different scenarios (e.g., future dates, old dates, draft PRs).

## License

This project is licensed under the MIT License.
