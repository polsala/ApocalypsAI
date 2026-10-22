# Nightly PR Labeler

## Overview

`nightly-pr-labeler` is a whimsical yet practical reusable GitHub Action that scans the list of files changed in a pull request and automatically suggests labels such as `documentation`, `tests`, `ci`, and `python`.  It helps keep PRs tidy without manual label juggling.

## How it works

1. The workflow that uses this action must provide a JSON event payload containing a `files` array (the list of changed file paths).  The official GitHub `pull_request` event does not include this array, so a preceding step (e.g., `actions/github-script` or a custom script) should fetch the changed files via the GitHub API and write them to a temporary file, then set the `GITHUB_EVENT_PATH` environment variable.
2. The action reads `GITHUB_EVENT_PATH`, determines appropriate labels, and prints a JSON array of labels to `stdout`.  You can capture this output and feed it to `actions/github-script` or `peter-evans/create-or-update-labels` to actually apply the labels.

## Example usage

```yaml
name: PR Labeler
on:
  pull_request_target:
    types: [opened, synchronize]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Get changed files
        id: files
        uses: actions/github-script@v6
        with:
          script: |
            const pr = context.payload.pull_request;
            const { data: files } = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr.number
            });
            const paths = files.map(f => f.filename);
            const fs = require('fs');
            const tmp = require('os').tmpdir();
            const file = `${tmp}/pr-files-${pr.number}.json`;
            fs.writeFileSync(file, JSON.stringify({ files: paths }));
            core.exportVariable('GITHUB_EVENT_PATH', file);
      - name: Run labeler
        uses: ./nightly-pr-labeler
        id: labeler
      - name: Apply labels
        uses: actions/github-script@v6
        with:
          script: |
            const labels = JSON.parse(`${{ steps.labeler.outputs.labels }}`);
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              labels
            });
```

## Supported label heuristics

| Pattern | Label |
|---------|-------|
| Path starts with `docs/` or ends with `.md` | `documentation` |
| Path starts with `tests/` or ends with `.test.js` / `.spec.js` | `tests` |
| Path starts with `.github/` or contains `workflow` | `ci` |
| Path ends with `.py` | `python` |

Feel free to fork and extend the heuristics for your own project!
