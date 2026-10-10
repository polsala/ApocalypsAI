# Nightly Prophetic PR Omen

A whimsical GitHub Action that adds a prophetic omen to your Pull Requests, hinting at the potential future impact of the code changes. Embrace the mystery and let the ApocalypsAI guide your merges!

## ✨ How it works

When a Pull Request is opened or updated, this action calculates a unique "omen" based on the PR's title and body. This omen is then added as a comment to the PR, providing a fun, cryptic, and sometimes eerily accurate prediction about the code's journey.

## 🚀 Usage

To use the `nightly-prophetic-pr-omen` action, add a step to your GitHub Actions workflow (e.g., in `.github/workflows/omen.yml`):

```yaml
name: Prophetic PR Omen

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  omen:
    runs-on: ubuntu-latest
    steps:
      - name: Generate and Post Prophetic Omen
        uses: polsala/ApocalypsAI/utils/nightly-prophetic-pr-omen@main # Replace 'main' with your branch if needed
        with:
          pr-title: ${{ github.event.pull_request.title }}
          pr-body: ${{ github.event.pull_request.body }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name           | Description                                    | Required |
| :------------- | :--------------------------------------------- | :------- |
| `pr-title`     | The title of the pull request.                 | `true`   |
| `pr-body`      | The body of the pull request.                  | `false`  |
| `github-token` | GitHub token for commenting on the PR.         | `true`   |

### Outputs

| Name           | Description                     |
| :------------- | :------------------------------ |
| `omen-message` | The generated prophetic omen.   |

## 🧪 Development & Testing

The omen generation logic is deterministic, ensuring consistent results for the same PR title and body. Tests are written using Jest and mock the GitHub Actions toolkit to run offline.

To run tests:

1.  Navigate to the `utils/nightly-prophetic-pr-omen` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`

```bash
# Example of running tests
cd utils/nightly-prophetic-pr-omen
npm install
npm test
```
