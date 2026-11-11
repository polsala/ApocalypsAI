# Nightly Release Blessing

A GitHub Action that bestows a whimsical, post-apocalyptic blessing and a survival tip upon successful releases or merges to `main`. Ensure your deployments are not just functional, but also spiritually fortified for the trials ahead!

## Usage

Add this action to your workflow, typically after a successful build, test, or deployment step.

```yaml
name: Release Blessing Workflow

on:
  release:
    types: [published]
  push:
    branches:
      - main

jobs:
  bless_release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Bestow Release Blessing
        uses: polsala/ApocalypsAI/github-actions/nightly-release-blessing@main # Replace 'main' with a specific tag/SHA in production
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          blessing-type: 'random' # Optional: 'ominous', 'hopeful', 'random'

      - name: Use the Blessing Message (Example)
        run: |
          echo "The blessing for this release is:"
          echo "${{ steps.bless.outputs.blessing-message }}"
        id: bless
```

## Inputs

| Name          | Description                                                                 | Required | Default   |
|---------------|-----------------------------------------------------------------------------|----------|-----------|
| `github-token`| GitHub token for API interaction (e.g., `secrets.GITHUB_TOKEN`).            | `true`   |           |
| `blessing-type`| Type of blessing to generate.                                               | `false`  | `random`  |

## Outputs

| Name          | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `blessing-message`| The full generated blessing message, including the survival tip.            |

## How it works

The action runs a bash script that selects a random blessing and a relevant survival tip from internal lists. It then combines these into a single message, which is outputted. In a real workflow, you would typically use this output to create a release comment, a new issue, or a discussion post.
