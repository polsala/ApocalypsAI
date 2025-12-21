# Nightly GitHub Actions Visualizer

A GitHub Actions workflow that automatically generates visual diagrams of your repository's GitHub Actions workflows.

## Features

- Automatically detects all workflow files in `.github/workflows/`
- Generates interactive SVG diagrams showing job dependencies
- Highlights job relationships and parallel execution paths
- Creates a visual overview of your CI/CD pipeline
- Updates automatically on workflow changes

## Usage

1. Add this workflow to your repository's `.github/workflows/` directory
2. The workflow will automatically run when workflow files are modified
3. Generated diagrams will be uploaded as workflow artifacts
4. Optionally, diagrams can be committed back to the repository

## Configuration

The workflow can be configured by modifying the environment variables in the workflow file:

- `WORKFLOW_DIR`: Directory containing workflow files (default: `.github/workflows`)
- `OUTPUT_DIR`: Directory for generated diagrams (default: `workflow-diagrams`)
- `COMMIT_DIAGRAMS`: Whether to commit diagrams back to repo (default: `false`)

## Example Output

The workflow generates SVG files that visualize:
- Job dependencies and execution order
- Parallel job execution
- Conditional job execution
- Workflow triggers and events

## Dependencies

- Uses only GitHub Actions built-in features
- No external dependencies required
- Compatible with all GitHub repositories

## License

MIT
