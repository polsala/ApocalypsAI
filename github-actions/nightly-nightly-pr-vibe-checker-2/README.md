# Nightly PR Vibe Checker

Ensures Pull Request titles align with the ApocalypsAI's whimsical-apocalyptic theme by checking for required and forbidden keywords.

## Usage

Add this action to your workflow (e.g., `.github/workflows/pr-checks.yml`):

```yaml
name: PR Vibe Check
on:
  pull_request:
    types: [opened, reopened, synchronize, edited]

jobs:
  vibe_check:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR Title Vibe
        uses: polsala/ApocalypsAI/nightly-pr-vibe-checker@main # Adjust 'main' to your default branch or a specific tag
        id: vibe_status
        with:
          required-keywords: "temporal,void,wasteland,whisper,anomaly,apocalypse"
          forbidden-keywords: "fix,feat,chore,refactor,docs,style,perf,test,build,ci,revert"
          fail-on-no-match-required: true
          fail-on-match-forbidden: true
      - name: Report Vibe Status
        run: echo "PR Vibe Status: ${{ steps.vibe_status.outputs.vibe-status }}"
```

## Inputs

*   `required-keywords` (optional): A comma-separated string of keywords. The PR title must contain at least one of these keywords to pass the check. Case-insensitive.
*   `forbidden-keywords` (optional): A comma-separated string of keywords. The PR title must *not* contain any of these keywords to pass the check. Case-insensitive.
*   `fail-on-no-match-required` (optional): Boolean (`true` or `false`). If `true` (default), the action will fail if no `required-keywords` are found. If `false`, it will only warn.
*   `fail-on-match-forbidden` (optional): Boolean (`true` or `false`). If `true` (default), the action will fail if any `forbidden-keywords` are found. If `false`, it will only warn.

## Outputs

*   `vibe-status`: `pass` if the PR title meets the criteria, `fail` otherwise.

## Development

This action uses a composite run action with a bash script. Ensure `jq` is available in your environment for local testing.
