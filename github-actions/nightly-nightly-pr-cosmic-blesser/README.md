# Nightly PR Cosmic Blesser

Bestow cosmic approval upon your Pull Requests! This GitHub Action adds a whimsical, randomly selected blessing as a comment to your PR and can optionally set a passing status check, ensuring your code is aligned with the celestial spheres before merging.

## ✨ Features

*   **Whimsical Blessings:** A collection of positive, slightly absurd messages to brighten your day.
*   **PR Commenting:** Automatically adds a comment to the Pull Request.
*   **Optional Status Check:** Can set a passing status check named "Cosmic Blessing" to indicate celestial alignment.
*   **Easy Integration:** Simple to add to any GitHub Actions workflow.

## 🚀 Usage

Add the following step to your PR workflow (e.g., on `pull_request` events):

```yaml
name: Cosmic PR Workflow

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  bless_pr:
    runs-on: ubuntu-latest
    steps:
      - name: Invoke Cosmic Blesser
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-cosmic-blesser@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          set-status-check: true # Optional: set to false to only comment
```

### Inputs

*   `github-token`: **Required.** Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`. Used to post comments and set status checks.
*   `set-status-check`: **Optional.** `true` or `false`. Defaults to `true`. If `true`, a passing status check named "Cosmic Blessing" will be added to the PR.

## 🌌 Examples of Blessings

*   "The cosmic dust motes align for this PR. Merge with stardust!"
*   "A celestial choir sings praises for your code. Proceed, brave developer!"
*   "The void whispers approval. Your changes are destined for greatness."
*   "Beware the space-time continuum, but your PR is safe. For now."
*   "May your merges be swift and your conflicts few, as decreed by the Great Architect of the Universe."

## 🛠️ Development

### Local Testing

To test this action locally, you can use `act`. Ensure you have `node` and `npm` installed.

1.  Install dependencies: `npm install`
2.  Run tests: `npm test`

### Action Structure

```
.
├── action.yml           # Action definition
├── README.md            # This file
├── src/
│   └── main.js          # Core logic
├── tests/
│   └── test.js          # Unit tests for main.js
└── package.json         # Node.js project definition
```
