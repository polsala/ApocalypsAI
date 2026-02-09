# Nightly Wasteland Pep Talker

A GitHub Action designed to inject a dose of post-apocalyptic optimism into your development workflow. Upon a successful pull request merge or a new release, this action will post a randomly selected "Wasteland Wisdom" message as a comment, reminding your team that even in the most desolate of codebases, there's always a glimmer of hope (and maybe a few spare parts).

## Features

- **Morale Boost**: Delivers whimsical, encouraging messages.
- **Automated Comments**: Integrates seamlessly with GitHub PRs and Releases.
- **Customizable**: Easily extendable with your own wisdoms.

## Usage

To use this action, add it to your workflow. It typically runs after a successful merge to your main branch or upon a release event.

### Example Workflow for Pull Request Merges

```yaml
name: Post-Merge Pep Talk

on:
  pull_request:
    types: [closed]
    branches: [main] # Or your primary branch

jobs:
  pep-talk:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Generate Wasteland Pep Talk
        uses: polsala/ApocalypsAI/github-actions/nightly-wasteland-pep-talker@main # Adjust path if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          event-type: pull_request
          event-id: ${{ github.event.pull_request.number }}
```

### Example Workflow for Releases

```yaml
name: Post-Release Wisdom

on:
  release:
    types: [published]

jobs:
  wisdom:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Wasteland Wisdom
        uses: polsala/ApocalypsAI/github-actions/nightly-wasteland-pep-talker@main # Adjust path if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          event-type: release
          event-id: ${{ github.event.release.id }}
```

## Inputs

| Name           | Description                                                                                             | Required |
|----------------|---------------------------------------------------------------------------------------------------------|----------|
| `github-token` | Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`. Used to authenticate API calls for commenting. | Yes      |
| `event-type`   | The type of GitHub event that triggered the action. Can be `pull_request` or `release`.                 | Yes      |
| `event-id`     | The ID of the event (PR number for `pull_request`, release ID for `release`).                           | Yes      |

## Development

### Adding New Wisdoms

You can easily add more whimsical wisdoms by editing the `src/generate_pep_talk.sh` file. Just add new lines to the `WISDOMS` array.

### Testing

Tests are located in `tests/`. The `test_action.yml` workflow demonstrates how to run the action in a mocked environment, verifying that the `gh` CLI command is called correctly without making actual API requests.
