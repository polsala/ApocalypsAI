# Nightly Post-Merge Pep Talk

This GitHub Action provides a moment of whimsical encouragement to your contributors after a Pull Request is successfully merged. In the face of impending digital doom (or just a tough coding session), a little affirmation goes a long way. This action automatically posts a random, apocalypse-themed pep talk or piece of wisdom as a comment on the merged PR.

## Usage

To use this action, add a new workflow file (e.g., `.github/workflows/pep-talk.yml`) to your repository:

```yaml
name: Post-Merge Pep Talk

on:
  pull_request_target:
    types:
      - closed

jobs:
  pep_talk:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to post comments on PRs
    if: github.event.pull_request.merged == true
    steps:
      - name: Deliver Post-Merge Pep Talk
        uses: polsala/ApocalypsAI/github-actions/nightly-post-merge-pep-talk@main # Or your specific branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

- `github-token`: **Required**. Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`, with `pull-requests: write` permission to allow the action to post comments.

## Example Pep Talks

Here are a few examples of the kind of wisdom this action might impart:

* "Another merge, another step closer to digital salvation! Keep building, survivor."
* "The code is strong with this one. May your commits be ever green and your deployments swift."
* "Even in the byte-strewn ruins, your contributions shine like a beacon. Well done!"
* "Remember, every line of code is a shield against the void. You've forged a mighty one today."

## Development

See `src/main.js` for the action's logic and `tests/test_main.js` for unit tests.
