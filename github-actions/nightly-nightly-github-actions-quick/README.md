# Nightly GitHub Actions Quickstart

A reusable GitHub Actions workflow that scaffolds a new project with a single workflow file, README, and a basic test suite.

## Features
- Scaffolds a new project with a single workflow file
- Generates a README with usage instructions
- Includes a basic test suite
- Supports multiple languages and frameworks

## Usage

Add the following to your repository's `.github/workflows/` directory:

```yaml
name: Nightly GitHub Actions Quickstart

on:
  workflow_dispatch:
    inputs:
      language:
        description: 'Language/Framework'
        required: true
        default: 'python'
        type: choice
        options:
          - python
          - node
          - rust
          - go
          - java
          - cpp

jobs:
  scaffold:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-quickstart.yml@main
    with:
      language: ${{ github.event.inputs.language }}
```

## License

MIT
