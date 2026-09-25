# Nightly Cosmic Alignment Checker

This GitHub Action ensures your Pull Request titles and commit messages are in cosmic harmony with the universe (or at least, with our repository's whimsical theme).

If a PR title or any of its commit messages lack keywords associated with the cosmos, this action will gently suggest a more 'aligned' phrasing, encouraging a touch of celestial wonder in our codebase.

## Usage

To use the Nightly Cosmic Alignment Checker, add the following step to your workflow:

```yaml
name: Cosmic PR Check
on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  check_alignment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Cosmic Alignment Check
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-align-check@main # Replace 'main' with your branch/tag if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          alignment-keywords: 'star,galaxy,nebula,cosmos,celestial,void,astral,comet,meteor,supernova,quasar,pulsar,orbit,lunar,solar,stardust,constellation'
```

### Inputs

*   `github-token`: (Required) Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`, to allow the action to comment on PRs.
*   `alignment-keywords`: (Optional) A comma-separated string of keywords to check for cosmic alignment. Defaults to a comprehensive list of celestial terms.

### Outputs

*   `is-aligned`: A boolean indicating whether cosmic alignment was detected in the PR title or commit messages.

## How it Works

Upon a `pull_request` event (opened, reopened, or synchronized), the action will:

1.  Fetch the PR title and all associated commit messages.
2.  Scan these texts for any of the specified `alignment-keywords` (case-insensitive).
3.  If no cosmic keywords are found, it will post a whimsical comment on the PR, suggesting a more celestial touch.
4.  The `is-aligned` output will be set to `true` or `false` accordingly.

Embrace the cosmic flow in your code!
