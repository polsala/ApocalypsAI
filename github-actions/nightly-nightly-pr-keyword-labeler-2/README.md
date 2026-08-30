# Nightly PR Keyword Labeler

A tiny GitHub Action that adds a label to a pull request when its title contains a given keyword. Perfect for whimsical labeling like “🧟‍♂️-zombie” for zombie‑themed PRs.

## Usage

```yaml
name: PR Keyword Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./github-actions/nightly-pr-keyword-labeler
        with:
          keyword: "zombie"
          label: "🧟‍♂️-zombie"
```

## Inputs

- `keyword` – The word to search for in the PR title (case‑insensitive).
- `label` – The label to output when the keyword is found.

## Outputs

- `label` – The label name if the keyword was present, otherwise empty.

The action does not directly call the GitHub API; it simply outputs the label name, allowing downstream steps to apply it with `actions/github-script` or similar.

## Testing

Run the provided test script locally:

```sh
node tests/test_action.js
```
