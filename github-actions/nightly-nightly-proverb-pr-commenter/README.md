# Nightly Post-Apocalyptic Proverb PR Commenter

A GitHub Action that automatically adds a whimsical, post-apocalyptic proverb or survival tip as a comment to new Pull Requests. Inject a bit of morale and quirky wisdom into your team's development workflow!

## Usage

To use this action, add it to your workflow file (e.g., `.github/workflows/proverb-pr.yml`):

```yaml
name: Proverb PR Commenter

on:
  pull_request:
    types: [opened, reopened]

jobs:
  add-proverb:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Add Post-Apocalyptic Proverb
        uses: polsala/ApocalypsAI/github-actions/nightly-proverb-pr-commenter@main # Adjust path if moved
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: proverbs-file: './my-custom-proverbs.txt' # Path relative to repo root
```

### Inputs

*   `github-token` (required): Your GitHub Token, usually `secrets.GITHUB_TOKEN`. This is used to authenticate API calls for commenting on the Pull Request.
*   `proverbs-file` (optional): The path to a custom text file containing proverbs, one per line. If not provided, the action will use its default `proverbs.txt` file. The path should be relative to the repository root.

## How it works

1.  The action is triggered on `pull_request` events (specifically `opened` or `reopened`).
2.  It uses the provided `github-token` to authenticate with the GitHub API.
3.  It reads proverbs from the `proverbs.txt` file (either the default or a custom one).
4.  A random proverb is selected.
5.  The selected proverb is posted as a comment on the Pull Request using the `gh` CLI.

## Development & Testing

The core logic resides in `src/entrypoint.sh`. Tests are implemented in `tests/test_entrypoint.sh` and simulate the GitHub Actions environment by mocking the `gh` CLI and environment variables.

To run tests locally:

```bash
bash tests/test_entrypoint.sh
```
