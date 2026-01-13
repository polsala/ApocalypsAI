# Nightly Label Emoji Adder

A GitHub Action that adds an emoji reaction to an issue or pull request based on its labels.

## Inputs

- `token` (required): GitHub token with repo scope.
- `issue-number` (required): Number of the issue or PR.
- `label-emoji-map` (required): JSON string mapping label names to GitHub reaction emojis (e.g., `{"bug":"+1","enhancement":"rocket"}`).

## How it works

The action fetches the labels of the specified issue, finds the first label that exists in the provided map, and posts the corresponding emoji as a reaction.

## Example workflow

```yaml
name: Label Emoji
on:
  issues:
    types: [opened, edited]

jobs:
  add-emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: owner/nightly-label-emoji-adder@v1
        with:
          token: ${{{{ secrets.GITHUB_TOKEN }}}}
          issue-number: ${{{{ github.event.issue.number }}}}
          label-emoji-map: '{"bug":"+1","enhancement":"rocket"}'
```

## License

MIT

