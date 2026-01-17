# Nightly First Blossom Celebrator

This GitHub Action celebrates new contributors by automatically posting a whimsical comment on their very first merged pull request. It's a small gesture to welcome and appreciate fresh talent joining the community.

## How it Works

1.  **Trigger**: The action runs whenever a pull request is closed and merged into the default branch.
2.  **Contributor Check**: It queries the GitHub API to determine if the author of the merged PR has any other merged pull requests in the repository.
3.  **Celebration**: If no other merged PRs are found, it's identified as their 'first blossom' (first contribution), and a celebratory comment is posted to the PR.

## Usage

To use this action, add a new workflow file (e.g., `.github/workflows/first-blossom.yml`) to your repository:

```yaml
name: First Blossom Celebration

on: pull_request_target

jobs:
  celebrate-first-contribution:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Celebrate First Blossom
        # Use the full path to the action within the repository
        # Example: polsala/ApocalypsAI/github-actions/nightly-first-blossom-celebrator@main
        uses: <owner>/<repo>/github-actions/nightly-first-blossom-celebrator@main # Replace with your actual repo path and branch/tag
        id: celebrate
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - name: Output if first contribution
        run: echo "Is first contribution: ${{ steps.celebrate.outputs.is-first-contribution }}"
```

### Inputs

*   `github-token`: **Required**. A GitHub token with `pull_requests: write` and `issues: write` permissions. `secrets.GITHUB_TOKEN` usually suffices for `pull_request_target` events.

### Outputs

*   `is-first-contribution`: A boolean string (`'true'` or `'false'`) indicating whether the merged PR was the author's first contribution to the repository.

## Development

This action is built with Node.js and uses the `@actions/github` and `@actions/core` libraries.

To run tests locally:

1.  Install dependencies:
    ```bash
    npm install @actions/core @actions/github jest jest-when
    ```
2.  Run tests:
    ```bash
    npm test
    ```
