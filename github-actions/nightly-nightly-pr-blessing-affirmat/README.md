# Nightly PR Blessing Affirmation

This GitHub Action bestows a whimsical, apocalypse-themed affirmation upon Pull Requests that have been successfully merged with all checks passing. It's a small token of appreciation for maintaining order and quality in the face of impending temporal distortions.

## Features

*   **Automated Affirmations**: Automatically posts a positive, themed comment to merged PRs.
*   **Quality Gated**: Only blesses PRs where all associated status checks have passed successfully.
*   **Whimsical**: Adds a touch of lightheartedness to your CI/CD pipeline.

## Usage

To use this action, add a step to your GitHub Actions workflow (e.g., in `.github/workflows/bless-pr.yml`). This action should typically run on `pull_request` events with `types: [closed]`.

```yaml
name: 'Bless Merged PRs'

on: 
  pull_request:
    types: [closed]

jobs:
  bless_pr:
    runs-on: ubuntu-latest
    # Only run if the PR was merged and not just closed
    if: github.event.pull_request.merged == true
    steps:
      - name: 'PR Blessing Affirmation'
        uses: polsala/ApocalypsAI/nightly-pr-blessing-affirmation@main # Replace 'main' with your branch if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

*   `github-token`: **Required**. A GitHub token with `pull_requests: write` permission to post comments. Usually `${{ secrets.GITHUB_TOKEN }}` is sufficient.

### Outputs

*   `affirmation-message`: The specific affirmation message that was posted to the PR.

## Whimsical Affirmations

Here are some examples of the affirmations this action might post:

*   "The void acknowledges your diligence. Well merged, survivor!"
*   "Even in the twilight, your code shines bright. A beacon of hope!"
*   "The temporal currents are stable. This merge is blessed by the Chrono-Weavers!"
*   "A successful integration! The data streams flow smoothly through the fractured reality."
*   "Your contribution ripples positively through the timelines. Excellent work!"

## Development

This action is written in JavaScript and uses the `@actions/core` and `@actions/github` libraries. Tests are written with Jest.
