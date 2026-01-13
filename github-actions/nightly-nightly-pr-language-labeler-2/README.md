# PR Language Labeler

A GitHub Action that automatically adds labels to a pull request based on the programming languages of the files changed.

## Features
- Detects common programming languages from file extensions.
- Adds a label in the form `lang:<language>` (e.g., `lang:python`).
- Works outâofâtheâbox with the default `GITHUB_TOKEN`.
- Optional `files` input for testing or custom file lists.

## Usage
```yaml
name: PR Language Labeler
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Label PR by language
        uses: ./\.github/actions/pr-language-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs
| Name | Description | Required |
|------|-------------|----------|
| `github-token` | Token with repo scope (usually `GITHUB_TOKEN`). | Yes |
| `files` | Optional JSON array of filenames to analyze (useful for testing). | No |

## How it works
1. The action receives a list of changed files (either via the `files` input or by calling the GitHub API).
2. It maps file extensions to language names.
3. It creates labels like `lang:python` and adds them to the PR.

## Development
The action is written in JavaScript and uses the official `@actions/core` and `@actions/github` packages.

### Running tests
```bash
npm install
npm test
```

## License
MIT
