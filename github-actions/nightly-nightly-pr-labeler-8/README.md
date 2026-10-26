# nightly‑pr‑labeler

A tiny GitHub Action that inspects the title of a pull request and automatically adds appropriate labels:

* `bug` – if the title contains the word *bug*
* `enhancement` – if the title contains the word *feature*
* `documentation` – if the title contains *doc* or *documentation*
* a random emoji label (🚀, 🐛, ✨, 📚, ⚡) for a touch of whimsy

The action does **not** call the GitHub API directly; instead it emits the `labels` output which can be consumed by a subsequent step that actually applies the labels (e.g., using `gh` or the `actions/github-script` action).

## Usage
```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu‑latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run labeler
        id: labeler
        uses: ./github-actions/nightly-pr-labeler
        with:
          # No inputs needed; the action reads the PR event automatically

      - name: Apply labels
        uses: actions/github-script@v6
        with:
          script: |
            const labels = '${{ steps.labeler.outputs.labels }}'.split(',').map(l => l.trim()).filter(Boolean);
            if (labels.length) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }
```

## Files
* `action.yml` – Action metadata
* `src/index.js` – Core implementation (pure Node.js, no external deps)
* `tests/test.js` – Offline deterministic test suite using only the Node standard library

## License
MIT © ApocalypsAI
