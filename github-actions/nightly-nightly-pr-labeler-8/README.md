# Nightly PR Labeler

Utility GitHub Action that reads a comma‑separated list of labels from the `labels` input and prints the labels it would apply to the current pull request. Useful for debugging label logic without needing a token.

## Usage

```yaml
steps:
  - uses: actions/checkout@v3
  - name: PR Labeler
    uses: ./utils/nightly-pr-labeler
    with:
      labels: bug, documentation
```

The action will output `applied-labels` containing the list of labels.

## Inputs

- `labels` – Comma‑separated list of labels to apply.

## Outputs

- `applied-labels` – The processed list of labels.

## Testing

Run `node tests/test_index.js` (uses Node's built‑in assert).
