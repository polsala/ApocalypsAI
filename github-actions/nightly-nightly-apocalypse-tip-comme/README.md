# Apocalypse Tip Commenter

A GitHub Action that provides a random post‑apocalyptic survival tip. It can be used in workflows to add flavor to CI runs or to post the tip as a comment.

## Usage

```yaml
uses: ./github-actions/nightly-apocalypse-tip-commenter
id: tip
```

Then you can use `${{ steps.tip.outputs.tip }}`.

## Inputs

None.

## Outputs

- `tip`: The selected tip.

## Example

```yaml
jobs:
  tip:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./github-actions/nightly-apocalypse-tip-commenter
        id: tip
      - run: echo "Today's tip: ${{ steps.tip.outputs.tip }}"
```

## License

MIT
