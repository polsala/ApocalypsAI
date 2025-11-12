# Workflow Whisperer

## The ApocalypsAI's Guide to Harmonious GitHub Actions

This utility, the `Workflow Whisperer`, is designed to gently guide your GitHub Action workflows towards optimal performance and clarity. It scans your `.github/workflows/*.yml` files, identifying common pitfalls and suggesting improvements to make your automation more robust, efficient, and less prone to unexpected behaviors.

Think of it as a friendly spirit ensuring your CI/CD pipelines are always in tune with the rhythm of the apocalypse (or just good engineering practices).

## Features

The Workflow Whisperer currently checks for:

*   **Missing Workflow Name**: Ensures your top-level workflow has a descriptive `name`.
*   **Missing Job Names**: Recommends adding a `name` to each job for better readability in the GitHub UI.
*   **Missing `runs-on`**: Verifies that all jobs specify an execution environment.
*   **Outdated `actions/checkout`**: Suggests upgrading `actions/checkout` to `v3` or `v4` for improved security and features.
*   **Unfiltered `on: push` / `on: pull_request`**: Warns if `on: push` or `on: pull_request` triggers are used without specifying `branches` or `paths`, which can lead to excessive workflow runs.
*   **Missing `concurrency`**: Suggests adding `concurrency` to manage parallel workflow runs, especially in busy repositories.

## Usage

To use the Workflow Whisperer, simply run the `whisperer.py` script from your repository's root directory (or any directory containing a `.github/workflows` folder):

```bash
python3 src/whisperer.py
```

It will scan the current directory for `.github/workflows/*.yml` files and print any identified issues and suggestions to the console.

## Example Output

```
Scanning workflow: .github/workflows/my-ci.yml
  [WARNING] Workflow 'my-ci.yml' is missing a top-level 'name'. Consider adding one for clarity.
  [WARNING] Job 'build' is missing a 'name'. Consider adding one for better readability in the GitHub UI.
  [SUGGESTION] Job 'test' uses 'actions/checkout@v2'. Consider upgrading to 'actions/checkout@v3' or 'v4' for better security and features.
  [SUGGESTION] Workflow 'my-ci.yml' has multiple jobs but no 'concurrency' key. Consider adding 'concurrency' to manage parallel runs.

Scanning workflow: .github/workflows/another-workflow.yml
  [WARNING] Job 'deploy' is missing 'runs-on'. This job will not run.
  [SUGGESTION] Workflow 'another-workflow.yml' triggers on 'push' without 'branches' or 'paths'. This can lead to excessive runs. Consider filtering.

No issues found in .github/workflows/good-workflow.yml

All workflows appear to be in good shape according to the Workflow Whisperer!
```
