# Nightly PR Affirmation Enforcer

This GitHub Action helps maintain the whimsical spirit and preparedness of the ApocalypsAI community by ensuring every Pull Request description includes a "Whimsical Affirmation" or a "Survival Tip". It promotes positive reinforcement and readiness, even in the face of impending doom.

## How it Works

The action scans the Pull Request description for specific keywords or phrases. If any of the required phrases are found, the action passes. If none are found, the action fails, prompting the PR author to add a suitable affirmation or tip.

## Usage

To use this action, add a step to your workflow YAML file, typically triggered on `pull_request` events. You can customize the phrases the action looks for.

```yaml
name: Enforce Whimsical PR Discipline

on:
  pull_request:
    types: [opened, edited, reopened, synchronize]

jobs:
  check_pr_affirmation:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR Description for Affirmation
        # Replace 'polsala/ApocalypsAI/github-actions/nightly-pr-affirmation-enforcer@main' with the actual path
        # to this action in your repository, or a specific release tag.
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-affirmation-enforcer@main
        with:
          pr-description: ${{ github.event.pull_request.body }}
          required-phrases: "Whimsical Affirmation:,Survival Tip:,Apocalyptic Insight:"

      - name: PR Affirmation Status
        if: always()
        run: |
          echo "Affirmation check completed. Status: ${{ steps.check_pr_affirmation.outputs.affirmation-found }}"
```

## Inputs

*   `pr-description` (Required):
    The full body of the pull request. This is typically retrieved using `${{ github.event.pull_request.body }}`.

*   `required-phrases` (Optional):
    A comma-separated string of phrases that the PR description must contain at least one of. If multiple phrases are provided, the action passes if *any* of them are found. Defaults to `"Whimsical Affirmation:,Survival Tip:"`.

## Outputs

*   `affirmation-found`:
    A boolean string (`'true'` or `'false'`) indicating whether any of the required phrases were found in the PR description.
