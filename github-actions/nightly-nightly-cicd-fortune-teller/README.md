# Nightly CI/CD Fortune Teller

A whimsical GitHub Action that brings a touch of cosmic guidance to your CI/CD pipelines! This action posts a randomly generated "CI/CD fortune" or "deployment blessing" as a comment on your Pull Requests, adding a moment of reflection (or amusement) before your code goes live.

## ✨ Features

*   **Whimsical Fortunes:** Get a unique, randomly generated message for each PR.
*   **Blessings & Warnings:** Choose between encouraging blessings for smooth deployments or light-hearted warnings about potential pitfalls.
*   **PR Commenting:** Automatically posts the fortune directly to your Pull Request.
*   **Self-contained:** Uses a simple bash script for fortune generation.

## 🚀 Usage

To use the `nightly-cicd-fortune-teller` action, add it as a step in your GitHub Actions workflow. It's typically run on `pull_request` events.

### Example Workflow (`.github/workflows/fortune.yml`)

```yaml
name: CI/CD Fortune Teller

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch: # Allows manual triggering

jobs:
  tell_fortune:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Tell a Blessing Fortune
        uses: polsala/ApocalypsAI/utils/nightly-cicd-fortune-teller@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          fortune-type: 'blessing' # Optional, defaults to 'blessing'

      - name: Tell a Warning Fortune (Optional)
        # You could run this conditionally, e.g., if tests fail, or just for fun
        # uses: polsala/ApocalypsAI/utils/nightly-cicd-fortune-teller@main
        # with:
        #   github-token: ${{ secrets.GITHUB_TOKEN }}
        #   fortune-type: 'warning'
```

### Inputs

| Input          | Description                                                                                             | Type     | Required | Default     |
| :------------- | :------------------------------------------------------------------------------------------------------ | :------- | :------- | :---------- |
| `github-token` | **Required.** GitHub token for posting comments. Usually `secrets.GITHUB_TOKEN`.                        | `string` | `true`   |             |
| `fortune-type` | Type of fortune to generate: `"blessing"` for encouraging messages or `"warning"` for humorous cautions. | `string` | `false`  | `"blessing"` |
| `pr-number`    | The pull request number to comment on. If not provided, the action attempts to infer it from `github.event` or `github.ref`. | `string` | `false`  |             |

### Outputs

| Output    | Description                   |
| :-------- | :---------------------------- |
| `fortune` | The generated fortune message. |

## 🧪 Testing

The action includes a self-contained test script for the fortune generation logic, and an example workflow to test the action's integration.

To run the unit tests for the fortune script locally:

```bash
cd utils/nightly-cicd-fortune-teller
bash tests/test_fortune.sh
```

This will execute the `test_fortune.sh` script, which verifies that the `fortune.sh` script produces non-empty output and correctly handles different `fortune-type` inputs.

To test the GitHub Action's workflow integration, you can manually trigger the `tests/test_action.yml` workflow from the GitHub UI or push changes to the `main` branch (or your development branch).

## 🤝 Contributing

Feel free to suggest new fortunes, improve the script, or add new features!
