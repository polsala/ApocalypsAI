# PR Fun Fact Commenter

A GitHub Action that posts a random fun fact as a comment on a pull request. Perfect for adding a splash of whimsy to code reviews.

## Usage

```yaml
name: Add Fun Fact
on:
  pull_request:
    types: [opened, reopened]

jobs:
  fun-fact:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Post Fun Fact
        uses: ./github-actions/nightly-pr-fun-fact-commenter
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The action will post a comment containing a random fun fact and also set the output `fun_fact` which can be used by subsequent steps.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with permission to comment on PRs | true | N/A |

## Outputs

| Name | Description |
|------|-------------|
| `fun_fact` | The fun fact that was posted |

## License

MIT
