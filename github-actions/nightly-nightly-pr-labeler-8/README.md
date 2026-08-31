# Nightly PR Labeler

Automatically adds descriptive labels to pull requests based on the files changed. This whimsical yet practical GitHub Action helps keep your PR board tidy without manual effort.

## Features

- Detects changed files in a PR.
- Matches file paths against glob patterns.
- Adds the corresponding labels via the GitHub API.
- Fully configurable via an input JSON mapping.

## Usage

Create a workflow that runs on `pull_request_target` (or `pull_request` if you trust the action).

```yaml
name: PR Labeler
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Nightly PR Labeler
        uses: ./nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional custom mapping (JSON string). Keys are glob patterns, values are label names.
          # label-mapping: '{"docs/**":"documentation","src/**":"code","tests/**":"tests"}'
```

### Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with `repo` scope to call the GitHub API. | Yes | – |
| `label-mapping` | JSON object mapping glob patterns to label names. | No | `{\"docs/**\":\"documentation\",\"tests/**\":\"tests\",\"src/**\":\"code\"}` |

### How it works

1. The action determines the PR number from the event context.
2. It fetches the list of changed files via `gh api`.
3. For each file, it checks the provided glob patterns.
4. All matching labels are collected and added to the PR.

### Testing

Run the provided test script locally:

```bash
cd nightly-pr-labeler/tests
bash test_action.sh
```

The test mocks the `gh` CLI, feeds a fake PR with three changed files, and verifies that the correct labels are reported.

---

*Enjoy a more organized PR workflow, courtesy of the ApocalypsAI night crew!*
