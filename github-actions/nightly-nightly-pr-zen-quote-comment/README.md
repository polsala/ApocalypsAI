# nightly-pr-zen-quote-commenter

A whimsical yet useful GitHub Action that leaves a random zen quote as a comment on every new pull request. Perfect for adding a touch of inspiration (or confusion) to your CI pipeline.

## Features

- Picks a quote from a curated list of zen sayings.
- Posts the quote as a comment on the PR using the provided `GITHUB_TOKEN`.
- Fully self‑contained – no external network calls, all quotes are baked in.
- Deterministic in tests by allowing the `RANDOM` seed to be set.

## Usage

Add the following step to any workflow that runs on `pull_request` events:

```yaml
jobs:
  zen-comment:
    runs-on: ubuntu-latest
    steps:
      - name: Add zen quote comment
        uses: ./path/to/nightly-pr-zen-quote-commenter
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | A token with `repo` scope to post comments. Usually `secrets.GITHUB_TOKEN`. | Yes |

### Environment Variables (advanced)

| Variable | Description |
|----------|-------------|
| `PR_NUMBER` | Pull request number to comment on. If omitted, the action will try to read it from the `GITHUB_EVENT_PATH` payload (standard GitHub event JSON). |
| `GITHUB_API_URL` | Base URL for the GitHub API. Defaults to `https://api.github.com`. |

## Testing

The `tests/test_action.sh` script runs the action in a sandbox with a mocked `curl` command to capture the request payload. It forces `RANDOM=0` to make the quote selection deterministic.

Run the test locally:

```bash
chmod +x tests/test_action.sh
./tests/test_action.sh
```

If the test passes, you will see `All tests passed!`.

## License

MIT © ApocalypsAI
