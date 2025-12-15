# Nightly GHA Workflow Visualizer

A GitHub Actions workflow that automatically generates visual graphs of your repository's workflows. This tool parses YAML workflow files and creates interactive SVG diagrams showing job dependencies and workflow structure.

## Features

- Automatically detects workflow files in `.github/workflows/`
- Generates visual dependency graphs
- Highlights job relationships and parallel execution paths
- Creates interactive SVG output with tooltips
- Runs nightly to keep diagrams up-to-date

## Usage

The workflow runs automatically every night at 2 AM UTC. You can also trigger it manually:

```yaml
name: Manual Workflow Visualization
on:
  workflow_dispatch:

jobs:
  visualize:
    uses: ./.github/workflows/visualize-workflows.yml
```

## Output

Visualizations are stored in the `workflow-diagrams/` directory as SVG files, with one diagram per workflow.

## Requirements

- Node.js 18+ (for the visualization script)
- mermaid-cli for rendering diagrams

## License

MIT
