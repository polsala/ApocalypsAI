# nightly-celestial-pr-blesser

A GitHub Action that bestows a "Celestial Blessing" upon Pull Requests based on configurable alignment criteria. This action helps maintain PR quality and encourages good practices with a touch of cosmic whimsy.

## ✨ Features

- **Configurable Criteria**: Set minimum PR body length, maximum lines changed, and required keywords in the PR title.
- **Whimsical Feedback**: Adds a comment to the PR with a "Celestial Blessing" or a "Cosmic Alignment" suggestion.
- **Status Output**: Sets an `is-blessed` output for conditional workflow steps.
- **Failure Enforcement**: Can optionally fail the workflow if the PR does not meet alignment criteria.

## 🚀 Usage

To use this action, add it as a step in your GitHub Actions workflow, typically on `pull_request` events.

### Example Workflow (`.github/workflows/celestial-blessing.yml`)

```yaml
name: Celestial PR Blessing

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  bless_pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Bestow Celestial Blessing
        id: celestial_blesser
        uses: polsala/ApocalypsAI/nightly-celestial-pr-blesser@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-title-keywords: 'feat,fix,docs,chore,refactor'
          pr-body-min-length: '50'
          max-lines-changed: '300'
          blessing-message: '✨ The cosmos aligns for this Pull Request! May its journey to merge be guided by starlight. ✨'
          failure-message: '🌌 The celestial currents are turbulent for this Pull Request. Seek better alignment with the stars (and review criteria). 🌌'

      - name: Conditional Step if Blessed
        if: steps.celestial_blesser.outputs.is-blessed == 'true'
        run: echo "The PR is blessed! Proceeding with further celestial tasks..."

      - name: Conditional Step if Not Blessed
        if: steps.celestial_blesser.outputs.is-blessed == 'false'
        run: echo "The PR is not blessed. Consider adding a manual review label."
```

## ⚙️ Inputs

| Name                  | Description                                                                 | Required | Default                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------------|
| `github-token`        | GitHub token for API calls (e.g., to add comments).                         | `true`   |                                                                                                         |
| `pr-title-keywords`   | Comma-separated keywords required in PR title (e.g., "feat,fix").           | `false`  | `feat,fix,docs,chore`                                                                                   |
| `pr-body-min-length`  | Minimum length for the PR body description.                                 | `false`  | `20`                                                                                                    |
| `max-lines-changed`   | Maximum total lines added/deleted for a blessing.                           | `false`  | `500`                                                                                                   |
| `blessing-message`    | Message to add if the PR receives a blessing.                               | `false`  | `✨ This Pull Request has achieved Celestial Alignment! May its merge be swift and its impact profound. ✨` |
| `failure-message`     | Message to add if the PR does not receive a blessing.                       | `false`  | `🌌 This Pull Request seeks further cosmic alignment. Review the stars (and criteria) for a blessing. 🌌` |

## 📤 Outputs

| Name         | Description                                        |
|--------------|----------------------------------------------------|
| `is-blessed` | `true` if the PR received a blessing, `false` otherwise. |

## 🧪 Testing

The action includes unit tests using `jest`. To run them:

1.  Navigate to the `nightly-celestial-pr-blesser` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`
