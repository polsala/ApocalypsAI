## Nightly GitHub Actions Validator

This utility is a GitHub Actions workflow designed to automatically validate other GitHub Actions workflows within the repository. It checks for common issues such as missing secrets, overly broad permissions, and adherence to best practices, aiming to improve the security and reliability of your CI/CD pipelines.

### How it Works

The workflow triggers on pull requests targeting the `main` branch. It uses a combination of shell scripting and static analysis to inspect `.github/workflows/*.yml` files.

### Usage

No direct usage is required. This workflow runs automatically on pull requests. It will comment on the PR with any detected issues.

### Configuration

Currently, the workflow is configured to run on all `.yml` files within the `.github/workflows/` directory. Future enhancements could include configurable paths or specific checks.

### Example Workflow Run

When a PR is opened, the workflow will execute. If issues are found, it will post a comment like:

```
@<user> :warning: **GitHub Actions Workflow Validation Failed** :warning:

Found the following potential issues in your workflow:

- **`path/to/your/workflow.yml`**: Uses `secrets.ANY_SECRET` which is too broad. Consider specifying a more granular secret.
- **`path/to/another/workflow.yml`**: Grants `write-all` permissions. Review if this is necessary.
```

If no issues are found, a success message will be posted.
