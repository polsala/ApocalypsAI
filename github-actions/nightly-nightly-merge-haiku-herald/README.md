# Nightly Merge Haiku Herald

A whimsical GitHub Action that celebrates successful PR merges to the `main` branch by posting a randomly selected, apocalypse-themed haiku to a specified GitHub Issue or Discussion. Bring a touch of poetic charm (and impending doom) to your repository's workflow!

## Usage

Create a workflow file (e.g., `.github/workflows/haiku-herald.yml`) in your repository:

```yaml
name: Haiku Herald on Merge

on:
  pull_request:
    types: [closed]
    branches:
      - main

jobs:
  post-haiku:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Post Merge Haiku
        uses: polsala/ApocalypsAI/utils/nightly-merge-haiku-herald@main # Replace 'main' with your branch if testing
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          target-type: 'issue' # or 'discussion'
          target-id: '123'     # The issue number or discussion ID where the haiku will be posted
```

### Inputs

*   `github-token`: **Required**. Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`. This token needs `issues:write` or `discussions:write` permissions.
*   `target-type`: **Optional**. The type of target to comment on. Can be `issue` or `discussion`. Defaults to `issue`.
*   `target-id`: **Required**. The ID of the issue or discussion to post the haiku to. For issues, this is the issue number. For discussions, this is the discussion ID (found in the URL, e.g., `https://github.com/.../discussions/123` -> `123`).

## Development

### Haiku Collection

Haikus are stored in `src/haikus.json`. Feel free to add more! Each entry should be a string with newlines for the haiku lines.

### Local Testing

To test the JavaScript logic locally, ensure you have Node.js installed.

```bash
npm install
npm test
```
