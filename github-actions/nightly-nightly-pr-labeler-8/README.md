# Nightly PR Labeler

A whimsical GitHub Action that suggests appropriate labels for a pull request based on the list of changed files. It scans the file paths and outputs a comma‑separated list of labels that can be added to the PR.

## Features
- Detects documentation changes, Python code, Markdown, and generic changes.
- Runs in a lightweight Bash environment; no external dependencies.
- Easy to integrate into any workflow.

## Usage
```yaml
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Get changed files
        id: files
        run: |
          echo "files<<EOF" >> $GITHUB_OUTPUT
          git diff --name-only ${{{{ github.event.pull_request.base.sha }}}} ${{{{ github.event.pull_request.head.sha }}}} >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      - uses: ./github-actions/nightly-pr-labeler
        with:
          files: "${{{{ steps.files.outputs.files }}}}"
```

The action will print a line like:
```
Labels to add: documentation,python
```
You can then use `gh pr edit` or another step to actually apply the labels.
