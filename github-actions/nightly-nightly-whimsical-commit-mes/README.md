# Nightly Whimsical Commit Message Action

A tiny GitHub Action that prints a whimsical commit message suggestion based on the repository name. Perfect for adding a splash of fun to your CI runs.

## Usage

```yaml
name: Whimsical Commit Message

on:
  push:
    branches: [ main ]

jobs:
  suggest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate whimsical commit message
        uses: ./github-actions/nightly-whimsical-commit-message-action
```

The action reads the `GITHUB_REPOSITORY` environment variable and outputs a message like:

```
Whimsical commit suggestion: Galactic polsala/ApocalypsAI
```

## How it works

The action runs a small Node.js script that selects an adjective from a predefined list and combines it with the repository name.

## Testing

Run the tests locally with:

```sh
node tests/test_main.js
```
