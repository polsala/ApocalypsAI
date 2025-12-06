# Workflow Wellness Oracle

## Overview
The Workflow Wellness Oracle is a whimsical-yet-useful utility designed to scan your GitHub Action workflow files (`.github/workflows/*.yml`) for common configuration issues, deprecated syntax, and potential best practice deviations. It provides a 'wellness report' to help maintain the health and robustness of your repository's automation.

## Features
- **Trigger Check**: Ensures workflows have an `on` trigger defined.
- **Deprecated Syntax**: Flags usage of `::set-output`.
- **Job Runner Check**: Verifies that jobs specify a `runs-on` environment.
- **Step Action/Run Check**: Confirms that each step has either a `uses` or `run` command.
- **Basic Secret Detection**: Whimsically warns about potential hardcoded secrets in `env` blocks (very basic pattern matching).

## Usage
To run the Oracle, navigate to your repository's root and execute the script, providing the path to your `.github/workflows` directory:

```bash
python utils/workflow-wellness-oracle/src/oracle.py .github/workflows
```

The Oracle will print a report to the console, detailing any issues found.

## Example Output
```
Scanning workflows in .github/workflows...

--- Workflow Wellness Report ---

File: .github/workflows/my-broken-workflow.yml
  - WARNING: Workflow is missing an 'on' trigger.
  - WARNING: Job 'build' is missing 'runs-on'.
  - WARNING: Step 'setup' in job 'build' is missing 'uses' or 'run'.

File: .github/workflows/my-deprecated-workflow.yml
  - DEPRECATION: Found '::set-output' in step 'set-var' in job 'test'. Consider using job outputs or environment files.

File: .github/workflows/my-secret-workflow.yml
  - WHIMSICAL WARNING: Potential hardcoded secret 'MY_API_KEY' found in step 'Deploy App' in job 'deploy' env. Consider using GitHub Secrets.

All workflows scanned. May your automation be ever well!
```

## Dependencies
- `PyYAML` (install with `pip install PyYAML`)
