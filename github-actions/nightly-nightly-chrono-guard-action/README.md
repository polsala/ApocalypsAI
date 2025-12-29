# Nightly Chrono-Guard Action

A GitHub Action that scans Pull Request titles and commit messages for keywords related to temporal anomalies, time travel, or anachronisms. If detected, it adds a warning comment to the PR, reminding contributors to be mindful of the timeline.

## 🕰️ Purpose

In the chaotic aftermath of the apocalypse, maintaining a stable timeline is paramount. This action acts as a whimsical guardian, flagging any PRs that might inadvertently (or advertently!) introduce temporal paradoxes or distortions through their naming conventions. It's a light-hearted reminder to keep our code and our history consistent.

## 🚀 Usage

To use the Nightly Chrono-Guard Action in your workflow, add a step like this:

```yaml
name: Chrono-Guard Scan

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  chrono_scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Chrono-Guard
        id: check # Assign an ID to reference outputs
        uses: polsala/ApocalypsAI/nightly-chrono-guard-action@main # Adjust path if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          keywords: 'time travel,paradox,anachronism,future past,temporal rift,chronos,aevum,yester-tomorrow,pre-post-apocalypse,timey-wimey,temporal distortion'

      - name: Report if anomaly detected
        if: steps.check.outputs.temporal-anomaly-detected == 'true'
        run: echo "A temporal anomaly was detected! Check the PR comments for details."
```

### Inputs

*   `github-token`:
    *   **Description**: Your GitHub token for API access. Usually `secrets.GITHUB_TOKEN`.
    *   **Required**: `true`
*   `keywords`:
    *   **Description**: A comma-separated list of custom keywords to detect. Overrides the default list.
    *   **Required**: `false`
    *   **Default**: `'time travel,paradox,anachronism,future past,temporal rift,chronos,aevum,yester-tomorrow,pre-post-apocalypse,timey-wimey'`

### Outputs

*   `temporal-anomaly-detected`:
    *   **Description**: A boolean (`'true'` or `'false'`) indicating whether any temporal anomaly keywords were detected.

## 🧪 Development & Testing

The action's logic is implemented in `src/main.js`. Tests are written using Jest and located in `tests/test.js`.

To run tests locally:

1.  Navigate to the `nightly-chrono-guard-action` directory.
2.  Install dependencies: `npm install` (you'll need `jest`, `@actions/core`, `@actions/github`).
3.  Run tests: `npm test` (or `jest`).

The tests mock the GitHub Actions toolkit and API interactions to ensure deterministic and offline execution.

```javascript
// Example mock rationale from tests/test.js:
// Mock rationale: Simulate core functions for input/output/logging without actual side effects.
// Mock rationale: Simulate GitHub API calls and context for deterministic testing.
```
