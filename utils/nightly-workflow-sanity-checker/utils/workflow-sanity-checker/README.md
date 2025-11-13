# Workflow Sanity Checker

## Purpose

The Workflow Sanity Checker is a standalone utility designed to scan GitHub Actions workflow files (`.github/workflows/*.yml`) for common misconfigurations, missing essential blocks, and adherence to best practices. It helps ensure your automation remains robust and secure, even when the digital apocalypse looms.

## Features

*   **YAML Validity Check**: Ensures workflow files are syntactically correct YAML.
*   **Essential Block Verification**: Confirms the presence of `on:` triggers and `jobs:` sections.
*   **Job Structure Validation**: Checks that each job defines `runs-on` and `steps`.
*   **Action Versioning Enforcement**: Recommends specifying versions for `uses:` actions (e.g., `actions/checkout@v3` instead of `actions/checkout`).
*   **Permissions Block Recommendation**: Encourages the use of explicit `permissions` for enhanced security.

## Usage

Run the utility from your repository's root directory:

```bash
python src/checker.py
```

The script will scan all `.github/workflows/*.yml` files and print a report of any issues found.

## Example Output

```
Scanning workflows in .github/workflows/...

[ERROR] .github/workflows/broken.yml: Missing 'on:' trigger.
[WARNING] .github/workflows/unversioned.yml: Job 'build': Step 'Checkout': Action 'actions/checkout' should specify a version (e.g., 'actions/checkout@v3').
[INFO] .github/workflows/secure.yml: Job 'deploy': Consider adding an explicit 'permissions' block for better security.
[SUCCESS] All other workflows appear sane.
```
