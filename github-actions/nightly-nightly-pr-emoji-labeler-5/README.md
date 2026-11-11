# Nightly PR Emoji Labeler

A whimsical GitHub Action that automatically adds a random emoji label to every pull request and posts a friendly comment. Useful for adding a bit of fun to PR reviews while still being deterministic for testing.

## Usage

```yaml
name: PR Emoji Labeler
on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-pr-emoji-labeler
        with:
          github-token: ${{{{ secrets.GITHUB_TOKEN }}}}
```

## Inputs

- `github-token` (required): Token with repo scope.

## How it works

The action selects an emoji from a curated list, adds it as a label to the PR, and posts a comment like "🚀 PR labeled with 🚀! Happy coding!".

## Testing

Run the test script:

```sh
bash tests/test_labeler.sh
```
