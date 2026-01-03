# Nightly Workflow Visualizer

An interactive web-based tool that analyzes GitHub Actions workflows and generates dependency graphs to visualize job relationships, parallel execution paths, and workflow bottlenecks.

## Features

- **Interactive Graph**: Drag, zoom, and explore workflow dependencies
- **Job Analysis**: See execution order, parallel jobs, and critical paths
- **Performance Insights**: Identify bottlenecks and optimization opportunities
- **Export Options**: Download as PNG, SVG, or JSON

## Usage

1. Run the CLI tool to analyze a repository's workflows
2. Open the generated `index.html` in any modern browser
3. Explore the interactive visualization

## CLI Options

```bash
# Analyze workflows in current directory
node src/analyze.js

# Specify custom workflow directory
node src/analyze.js --workflows-dir .github/workflows

# Output to custom location
node src/analyze.js --output ./visualization
```

## Technologies

- **Frontend**: React + D3.js for interactive visualizations
- **Backend**: Node.js CLI tool for workflow parsing
- **Data Format**: JSON workflow dependency graphs

## Installation

```bash
npm install
npm run build
```

## License

MIT - feel free to use and modify!
