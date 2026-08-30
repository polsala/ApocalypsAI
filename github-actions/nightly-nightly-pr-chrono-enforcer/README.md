# Nightly PR Chrono-Consistency Enforcer

A GitHub Action that helps maintain the "temporal flow" and consistency of your project's Pull Requests. This utility ensures that PR titles and descriptions adhere to predefined length constraints and keyword patterns, preventing "temporal anomalies" in your commit history.

## ⏱️ The Problem

In the chaotic dance of development, PRs can sometimes drift out of sync. Titles might be too cryptic or excessively verbose, descriptions might lack crucial context, or contain forbidden phrases. The `Nightly PR Chrono-Consistency Enforcer` acts as a temporal guardian, ensuring each PR aligns with the project's established rhythm and quality standards.

## ✨ How it Works

This action runs on `pull_request` events. It inspects the PR's title and body against configurable rules:
-   **Length Constraints**: Define minimum and maximum lengths for both title and description.
-   **Required Keywords**: Specify keywords that *must* be present (e.g., `feat`, `fix`, `docs`, `refactor`).
-   **Disallowed Keywords**: Identify keywords that *must not* be present (e.g., `WIP`, `draft`, `TODO`).

If any inconsistencies are detected, the action will:
1.  Add a whimsical comment to the PR, detailing the "temporal anomalies."
2.  Optionally fail the GitHub Action check, preventing merge until the PR is brought back into "chrono-consistency."

## 🚀 Usage

To use the `Nightly PR Chrono-Consistency Enforcer` in your repository, add a new step to your workflow file (e.g., `.github/workflows/pr-checks.yml`):

```yaml
name: PR Chrono-Consistency Check

on:
  pull_request:
    types: [opened, reopened, synchronize, edited]

jobs:
  chrono_check:
    runs-on: ubuntu-latest
    steps:
      - name: Chrono-Consistency Enforcer
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-chrono-enforcer@main # Adjust 'main' to your default branch if different
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          min_title_length: '15'
          max_title_length: '80'
          min_body_length: '50'
          max_body_length: '1000'
          required_keywords: 'feat,fix,docs,refactor'
          disallowed_keywords: 'WIP,TODO,draft'
          fail_on_inconsistency: 'true'
```

### Inputs

| Input Name             | Description                                                                 | Required | Default |
| :--------------------- | :-------------------------------------------------------------------------- | :------- | :------ |
| `github_token`         | **Required.** GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`).   | `true`   |         |
| `min_title_length`     | Minimum allowed length for the PR title.                                    | `false`  | `10`    |
| `max_title_length`     | Maximum allowed length for the PR title.                                    | `false`  | `100`   |
| `min_body_length`      | Minimum allowed length for the PR description.                              | `false`  | `20`    |
| `max_body_length`      | Maximum allowed length for the PR description.                              | `false`  | `500`   |
| `required_keywords`    | Comma-separated list of keywords that *must* appear in the PR title or body. | `false`  |         |
| `disallowed_keywords`  | Comma-separated list of keywords that *must not* appear in the PR title or body. | `false`  |         |
| `fail_on_inconsistency`| Whether the action should fail if inconsistencies are found. If `false`, it will only post a warning and a comment. | `false`  | `true`  |

### Outputs

| Output Name            | Description                                                                 |
| :--------------------- | :-------------------------------------------------------------------------- |
| `is_chrono_consistent` | `true` if the PR is chrono-consistent, `false` otherwise.                   |

## 🧪 Development & Testing

The action's logic is implemented in `src/main.js`. Tests are written using Jest and located in `tests/test.js`.

To run tests locally:
1.  Navigate to the `github-actions/nightly-pr-chrono-enforcer` directory.
2.  Install dependencies: `npm install` (or `yarn install`).
3.  Run tests: `npm test` (or `yarn test`).

The tests mock the `@actions/core` and `@actions/github` modules to ensure deterministic and offline execution, simulating various PR scenarios and input configurations.
