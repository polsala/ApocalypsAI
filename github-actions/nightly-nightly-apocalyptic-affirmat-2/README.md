# Nightly Apocalyptic Affirmation GitHub Action

Injects a random, whimsically apocalyptic affirmation into your GitHub Actions workflow summary or as a step output. Because even when the world is ending, your code deserves a little encouragement.

## 🚀 Usage

Add this action to any of your GitHub Actions workflows.

```yaml
name: Daily Build with Affirmation

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Get Apocalyptic Affirmation
        id: affirmation_step
        uses: polsala/ApocalypsAI/github-actions/nightly-apocalyptic-affirmation@main # Replace 'main' with your branch/tag
        with:
          target: 'summary' # or 'output'

      - name: Use the affirmation (if target is 'output')
        if: steps.affirmation_step.outputs.affirmation != ''
        run: |
          echo "Today's wisdom: ${{ steps.affirmation_step.outputs.affirmation }}"

      - name: Your build steps here
        run: |
          echo "Building the future, one byte at a time..."
          # ... your actual build commands ...
```

### Inputs

*   `target` (Optional, default: `'summary'`):
    *   `'summary'`: The affirmation will be added to the workflow run summary.
    *   `'output'`: The affirmation will be available as a step output named `affirmation`. It will also be logged to `stdout` as an info message.

### Outputs

*   `affirmation`: The randomly selected apocalyptic affirmation (string).

## 🛠️ Development

### Local Testing

To test the `action.yml` and `src/main.js` locally, you can use `act` (a tool for running GitHub Actions locally).

1.  **Install `act`**: Follow instructions at [https://github.com/nektos/act](https://github.com/nektos/act)
2.  **Run a test workflow**: The `tests/test.yml` workflow is designed to be run as part of the repository's CI/CD. For local `act` testing, you would typically point `act` to a workflow file in `.github/workflows` that *uses* your action. For this specific setup, the `tests/test.yml` is a self-contained workflow that tests the action by referencing it locally.

    A more direct way to test the action's script (without full GitHub Actions environment):
    ```bash
    node src/main.js
    ```

### Contributing

Feel free to suggest new affirmations or improvements!

## License

This utility is released under the MIT License.
