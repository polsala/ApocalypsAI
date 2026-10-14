# Nightly PR Prophecy Checker

A GitHub Action that ensures your Pull Request descriptions contain a designated "Prophecy" section with actual content, guiding your project's destiny and ensuring proper documentation.

## 🌌 Purpose

In the chaotic dance of development, it's easy to lose sight of the grand vision. The `nightly-pr-prophecy-checker` acts as a cosmic guardian, ensuring every Pull Request comes with a clear "Prophecy" – a declaration of its intended impact, future implications, or simply a detailed explanation of its purpose. No more vague PRs; let the stars align with your code!

## ✨ Usage

To use this action, add it to your workflow, typically on `pull_request_target` or `pull_request` events.

```yaml
name: Validate PR Prophecy

on:
  pull_request:
    types: [opened, reopened, edited, synchronize]

jobs:
  check_prophecy:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR Prophecy
        uses: polsala/ApocalypsAI/nightly-pr-prophecy-checker@main # Replace 'main' with your branch/tag
        id: prophecy_check
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          prophecy-header: '## The Grand Prophecy' # Optional: customize the header

      - name: Fail if Prophecy is Missing or Empty
        if: ${{ steps.prophecy_check.outputs.prophecy-found == 'false' }}
        run: |
          echo "::error file=.github/workflows/pr-prophecy.yml::The Pull Request description must contain a non-empty '## The Grand Prophecy' section to align with our cosmic development path."
          exit 1
```

### Inputs

*   `github-token`: **Required**. Your GitHub token, usually `${{ github.token }}`. Used to access PR details (though this action primarily reads `GITHUB_EVENT_PATH`).
*   `prophecy-header`: **Optional**. The markdown header string to look for. Defaults to `## Prophecy`.

### Outputs

*   `prophecy-found`: `true` if the specified prophecy header was found and its section contains non-whitespace content, `false` otherwise.

## 🧪 Testing

The action includes a self-contained test workflow (`tests/test.yml`) that simulates different PR descriptions to verify its behavior.

To run tests locally (requires `act`):
```bash
act pull_request -e tests/event_pr_with_prophecy.json -W .github/workflows/test.yml
act pull_request -e tests/event_pr_empty_prophecy.json -W .github/workflows/test.yml
act pull_request -e tests/event_pr_no_prophecy.json -W .github/workflows/test.yml
```
*(Note: `act` might require adjustments for composite actions or specific environment variables.)*
