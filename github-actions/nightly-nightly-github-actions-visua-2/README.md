# Nightly GitHub Actions Visualizer

A GitHub Actions workflow that automatically generates interactive dependency graphs for your CI/CD pipelines. Perfect for understanding complex workflow relationships and identifying optimization opportunities.

## Features

- 🕸️ **Interactive Graphs**: Generate beautiful, interactive dependency graphs
- 📊 **Workflow Analysis**: Identify bottlenecks and optimization opportunities
- 🔄 **Auto-Update**: Automatically updates visualization on workflow changes
- 🎨 **Customizable**: Theme support and multiple output formats
- 📈 **Metrics**: Performance insights and dependency analysis

## Usage

### Basic Setup

Add this workflow to your `.github/workflows/` directory:

```yaml
name: Generate Workflow Visualization

on:
  workflow_dispatch:
  push:
    paths:
      - '.github/workflows/**'
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM

jobs:
  visualize-workflows:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-visualizer.yml@main
    with:
      output-format: 'svg'
      theme: 'dark'
      include-metrics: true
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `output-format` | Output format (svg, png, html) | svg |
| `theme` | Color theme (light, dark, colorful) | dark |
| `include-metrics` | Include performance metrics | true |
| `max-depth` | Maximum dependency depth to show | 5 |
| `exclude-workflows` | Comma-separated workflow names to exclude | '' |

### Output

The workflow generates:

- `workflow-graph.svg` - Interactive dependency graph
- `workflow-metrics.json` - Performance and dependency data
- `workflow-analysis.md` - Human-readable analysis report

## Examples

### Simple Workflow

```yaml
name: Simple CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Building..."
```

### Complex Multi-Stage Pipeline

```yaml
name: Complex Pipeline

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build

  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run deploy
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please:
- Check the [Issues](https://github.com/polsala/ApocalypsAI/issues) page
- Create a new issue with detailed reproduction steps
