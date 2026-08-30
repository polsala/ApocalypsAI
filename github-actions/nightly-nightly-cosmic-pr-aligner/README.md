# Nightly Cosmic PR Aligner

This GitHub Action ensures your Pull Requests are in "cosmic alignment" with your project's whimsical (or strict) naming conventions and content guidelines. It checks PR titles and descriptions against configurable regular expressions, promoting consistency and project harmony.

## Usage

Add this action to your workflow:

```yaml
name: Cosmic PR Alignment Check

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  align_check:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR Cosmic Alignment
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-pr-aligner@main # Replace 'main' with your branch/tag
        with:
          pr-title: ${{ github.event.pull_request.title }}
          pr-description: ${{ github.event.pull_request.body }}
          title-regex: '^(feat|fix|docs|chore|refactor|style|test|build|ci|perf|revert)(\(.+\))?: (✨|🐛|📝|🧹|♻️|🎨|✅|📦|🚀|⏪) .*' # Conventional Commits with Emojis
          description-regex: '.*(Aligns with the stars|Cosmic harmony achieved).*'
          fail-on-mismatch: true
```

### Inputs

- `pr-title`: (Optional) The pull request title to check. Defaults to `github.event.pull_request.title`. Useful for testing or custom scenarios.
- `pr-description`: (Optional) The pull request description (body) to check. Defaults to `github.event.pull_request.body`. Useful for testing or custom scenarios.
- `title-regex`: (Required) A regular expression pattern that the PR title must match.
- `description-regex`: (Required) A regular expression pattern that the PR description must match.
- `fail-on-mismatch`: (Optional) Boolean. If `true` (default), the action will fail if any pattern does not match. If `false`, it will only output warnings.

## Examples

### Enforcing Conventional Commits with Emojis

```yaml
          title-regex: '^(feat|fix|docs|chore|refactor|style|test|build|ci|perf|revert)(\(.+\))?: (✨|🐛|📝|🧹|♻️|🎨|✅|📦|🚀|⏪) .*'
          description-regex: '.*' # Any description is fine
```

### Requiring a specific phrase in the description

```yaml
          title-regex: '.*' # Any title is fine
          description-regex: '.*This PR brings cosmic balance to the force.*'
```

## Development & Testing

To test this action locally or in a workflow, you can provide explicit `pr-title` and `pr-description` inputs. See `tests/test_action.yml` for examples.
