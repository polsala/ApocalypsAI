# Nightly Header Harmonizer

Ensures cosmic consistency across your repository by enforcing a standardized, ApocalypsAI-themed header in specified files.

## Purpose

In the chaotic aftermath, maintaining order is paramount. This GitHub Action helps you enforce a consistent header across your codebase, ensuring every file proudly bears the mark of the ApocalypsAI collective. It supports various comment styles and can optionally fix non-compliant files.

## Usage

To use this action, add a step to your GitHub Actions workflow (e.g., on `push` or `pull_request`):

```yaml
name: Enforce ApocalypsAI Headers
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  header_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Nightly Header Harmonizer
        uses: polsala/ApocalypsAI/utils/nightly-header-harmonizer@main # Adjust 'main' to your branch/tag
        with:
          header-content: |
            ApocalypsAI Header Harmonizer
            Forged in the fires of the Nightly Integrator.
            Ensuring cosmic consistency, one file at a time.
            (c) 2024 ApocalypsAI. All rights reserved.
          file-patterns: '*.py,*.sh,*.js,*.ts,*.go,*.java,*.html,*.css,*.md'
          fix-mode: 'true' # Set to 'true' to automatically add missing headers

      - name: Commit changes if headers were fixed
        if: steps.header_check.outputs.non_compliant_files != '' && github.event_name == 'push' && inputs.fix-mode == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "docs: Harmonize file headers [ApocalypsAI]"
          git push
```

### Inputs

-   `header-content` (required):
    The multi-line content of the header to enforce. **Do not include comment markers**; the action will add them based on the file type.
    Example:
    ```yaml
    header-content: |
      ApocalypsAI Header Harmonizer
      Forged in the fires of the Nightly Integrator.
      Ensuring cosmic consistency, one file at a time.
      (c) 2024 ApocalypsAI. All rights reserved.
    ```

-   `file-patterns` (required):
    A comma-separated list of glob patterns for files to check. The action will iterate through files matching these patterns.
    Example: `'*.py,*.sh,src/**/*.js,docs/*.md'`

-   `fix-mode` (optional, default: `'false'`):
    If set to `'true'`, the action will attempt to prepend missing or incorrect headers to the files. If set to `'false'`, it will only report non-compliant files and fail the workflow.

### Outputs

-   `non_compliant_files`:
    A multi-line string containing the paths of all files that were found to be non-compliant. This output can be used in subsequent steps (e.g., to commit changes if `fix-mode` was enabled).

## Supported Comment Styles

The action automatically detects and applies appropriate comment styles based on file extensions:

-   `#` for: `.py`, `.sh`, `.yml`, `.yaml`, `.md`, `.txt`
-   `//` for: `.js`, `.ts`, `.jsx`, `.tsx`, `.go`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`
-   `<!-- -->` for: `.html`, `.xml`
-   `/* */` for: `.css`

Files with unsupported extensions will be skipped with a warning.
