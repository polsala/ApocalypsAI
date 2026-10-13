# Nightly PR Ponderer

A whimsical GitHub Action that adds a random, thought-provoking philosophical quote to newly opened pull requests. Encourage contemplation and a moment of reflection amidst the hustle of code reviews!

## ✨ Features

- **Philosophical Insight**: Automatically comments on new PRs with a curated philosophical quote.
- **Whimsical Touch**: Adds a unique, reflective element to your development workflow.
- **Easy Integration**: Simple to add to any repository's `.github/workflows`.

## 🚀 Usage

To use the Nightly PR Ponderer in your repository, create a new workflow file (e.g., `.github/workflows/ponder.yml`) and add the following content:

```yaml
name: PR Ponderer

on:
  pull_request:
    types: [opened, reopened] # Trigger when a PR is opened or reopened

jobs:
  ponder:
    runs-on: ubuntu-latest
    steps:
      - name: Ponder the Pull Request
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-ponderer@main # Use the main branch of this repo
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name           | Description                                   | Required |
| :------------- | :-------------------------------------------- | :------- |
| `github-token` | GitHub token for API calls (e.g., `secrets.GITHUB_TOKEN`). | `true`   |

### Outputs

| Name    | Description                               |
| :------ | :---------------------------------------- |
| `quote` | The philosophical quote added to the PR. |

## 📜 Quotes

The action selects from a predefined list of quotes, including wisdom from:
- Socrates
- René Descartes
- Jean-Paul Sartre
- Ralph Waldo Emerson
- Buddha
- Aristotle
- Charles Darwin
- Nelson Mandela
- John Lennon
... and more!

## 🤝 Contributing

Feel free to suggest new philosophical quotes or improvements to the action!
