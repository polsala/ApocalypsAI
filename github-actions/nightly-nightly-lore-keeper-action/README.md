# Nightly Lore Keeper Action

Ensures your Pull Request titles and descriptions resonate with the established lore of the ApocalypsAI universe. This action helps maintain narrative consistency across contributions, gently nudging contributors to infuse their messages with the appropriate thematic elements.

## 🌌 Purpose

In the ever-shifting sands of the post-apocalyptic digital wasteland, maintaining a coherent narrative is paramount. The Nightly Lore Keeper acts as a sentinel, ensuring that all new contributions (via Pull Requests) speak the language of our shared reality. It checks for the presence of specified 'lore keywords' in PR titles and descriptions, offering guidance when the narrative drifts.

## 🚀 Usage

To integrate the Nightly Lore Keeper into your workflow, add a step to your `.github/workflows/your-workflow.yml` file. This action typically runs on `pull_request` events.

```yaml
name: Lore Compliance Check

on: pull_request

jobs:
  check_lore:
    runs-on: ubuntu-latest
    steps:
      - name: Nightly Lore Keeper
        uses: polsala/ApocalypsAI/nightly-lore-keeper-action@main # Or your specific branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          lore-keywords: "Temporal Anomaly,Void Whisper,Wasteland Scavenger,Chronal Drift"
          check-pr-title: true
          check-pr-body: true
          fail-on-mismatch: false # Set to true to make the check fail
```

## ⚙️ Inputs

| Input             | Description                                                                                             | Required | Default |
|-------------------|---------------------------------------------------------------------------------------------------------|----------|---------|
| `github-token`    | **Required.** A GitHub token with `pull_requests: write` permission to comment on PRs.                  | `true`   |         |
| `lore-keywords`   | **Required.** A comma-separated string of keywords or regex patterns that must be present in the PR content. | `true`   |         |
| `check-pr-title`  | Whether to check the Pull Request title for lore keywords.                                              | `false`  | `true`  |
| `check-pr-body`   | Whether to check the Pull Request body for lore keywords.                                               | `false`  | `true`  |
| `fail-on-mismatch`| If `true`, the action will fail if lore keywords are not found. Otherwise, it will only comment.        | `false`  | `false` |

## 📤 Outputs

| Output          | Description                                                                    |
|-----------------|--------------------------------------------------------------------------------|
| `lore-compliant`| `true` if the PR title/body contains all specified lore keywords, `false` otherwise. |

## 📜 Example Workflow

```yaml
name: Lore Compliance Check

on:
  pull_request:
    types: [opened, reopened, edited, synchronize]

jobs:
  lore_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Nightly Lore Keeper
        id: lore_keeper
        uses: polsala/ApocalypsAI/nightly-lore-keeper-action@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          lore-keywords: "ApocalypsAI,Integrator,Wasteland,Temporal,Whisper"
          fail-on-mismatch: false

      - name: Report Lore Compliance
        if: steps.lore_keeper.outputs.lore-compliant == 'false'
        run: echo "Lore compliance check failed. Please update your PR to include relevant lore terms."
      - name: Lore Compliant Message
        if: steps.lore_keeper.outputs.lore-compliant == 'true'
        run: echo "Excellent! Your contribution resonates with the echoes of the void."
```
