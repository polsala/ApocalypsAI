## Nightly GitHub Action Debugger

This workflow provides a comprehensive snapshot of the GitHub Actions environment, aiding in the debugging of other workflows.

### Purpose

When a GitHub Actions workflow behaves unexpectedly, it can be challenging to pinpoint the cause. This utility creates a dedicated workflow that runs with minimal setup and outputs a wealth of information about the runner environment, including:

*   Environment variables
*   File system structure and contents of key directories
*   Installed tools and their versions
*   Network configuration
*   GitHub context information

This information can then be used to compare against expected states or to identify discrepancies that might be causing issues in other workflows.

### Usage

To use this workflow, simply add it to your repository's `.github/workflows/` directory. You can trigger it manually or via a cron schedule.

```yaml
name: Debug GitHub Actions Environment

on:
  workflow_dispatch: # Allows manual triggering
  schedule:
    - cron: '0 3 * * *' # Runs daily at 3 AM UTC

jobs:
  debug_env:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-debugger.yml@main
```

### Output

The workflow will create a log file named `action_environment_debug.log` containing all the collected information. This log will be attached to the workflow run, making it easily accessible for analysis.

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
