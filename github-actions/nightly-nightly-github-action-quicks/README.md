# Nightly GitHub Action Quickstart

A reusable GitHub Actions workflow template generator that creates a starter CI/CD pipeline with lint, test, and build steps for common project types.

## Features

- Generates a starter workflow for Python, Node.js, Rust, Go, and Java projects
- Includes lint, test, and build steps
- Configurable with environment variables
- Self-documenting with inline comments

## Usage

1. Add the workflow to your repository:

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-action-quickstart.yml@main
    with:
      project-type: "python" # or node, rust, go, java
      python-version: "3.11" # optional
      node-version: "20" # optional
      rust-version: "1.70" # optional
      go-version: "1.21" # optional
      java-version: "17" # optional
```

2. Customize the workflow as needed for your project.

## Project Types

- **python**: Lint with flake8, test with pytest, build with pip
- **node**: Lint with eslint, test with npm test, build with npm run build
- **rust**: Lint with clippy, test with cargo test, build with cargo build --release
- **go**: Lint with golangci-lint, test with go test, build with go build
- **java**: Lint with checkstyle, test with mvn test, build with mvn package

## License

MIT
