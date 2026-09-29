# Nightly Broken Link Scavenger

This GitHub Action acts as a digital scavenger, diligently sifting through your repository's markdown files (`.md`) to unearth and report any broken external links. In the post-apocalyptic digital landscape, dead links are like irradiated zones – best identified and avoided. This utility helps maintain the integrity of your documentation and ensures your community isn't led astray by 'wasteland' URLs.

## Features

*   Scans all `.md` files in a specified path.
*   Extracts external `http://` and `https://` links.
*   Performs HTTP HEAD/GET requests to check link validity.
*   Reports broken links (non-2xx status codes) in the job summary and as an action output.
*   Allows ignoring specific URL patterns.

## Usage

To use the Nightly Broken Link Scavenger, add it as a step in your GitHub Actions workflow. It's recommended to run this on `pull_request` or `push` events, or as a scheduled `cron` job.

```yaml
name: Link Scavenger

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  scavenge_for_broken_links:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Nightly Broken Link Scavenger
        id: link_scavenger
        uses: polsala/ApocalypsAI/github-actions/nightly-broken-link-scavenger@main # Replace 'main' with your branch/tag
        with:
          path: '.' # Optional: directory to scan, defaults to '.'
          ignore_patterns: | # Optional: newline-separated regex patterns to ignore URLs
            ^https://example.com/internal-docs
            ^https://localhost:

      - name: Report Broken Links
        if: steps.link_scavenger.outputs.broken_links_found == 'true'
        run: |
          echo "## ⚠️ Broken Links Detected! ⚠️"
          echo "The Nightly Broken Link Scavenger has found the following 'wasteland' URLs:\n"
          echo "${{ steps.link_scavenger.outputs.broken_links_report }}"
          exit 1 # Fail the job if broken links are found
      
      - name: No Broken Links
        if: steps.link_scavenger.outputs.broken_links_found == 'false'
        run: echo "✅ All links are sound! The digital wasteland is clear."
```

## Inputs

*   `path` (optional): The directory to start scanning for markdown files. Defaults to `.` (the repository root).
*   `ignore_patterns` (optional): A newline-separated string of regular expressions. Any URL matching one of these patterns will be skipped during the check. Useful for internal links or known flaky external services.

## Outputs

*   `broken_links_found`: A boolean string (`'true'` or `'false'`) indicating if any broken links were detected.
*   `broken_links_report`: A multiline string containing the list of broken links, formatted as `[HTTP_CODE] <URL> (found in <FILE_PATH>)`.

## Development & Testing

The core logic resides in `src/check_links.sh`. Tests are in `tests/test_check_links.sh` and use a mocked `curl` command to ensure deterministic and offline execution. To run tests locally:

```bash
cd github-actions/nightly-broken-link-scavenger
bash tests/test_check_links.sh
```
