# Nightly Workflow Guard Dog

This GitHub Action acts as a vigilant guardian for your CI/CD workflows. It inspects workflow runs for potentially risky operations or deviations from predefined safety rules, helping to prevent accidental misconfigurations or malicious actions.

## Purpose

In the chaotic landscape of automated workflows, it's easy for things to go awry. The Workflow Guard Dog is designed to be a proactive safety net, sniffing out suspicious activities before they can cause damage.

## How it Works

The Guard Dog analyzes the steps within a GitHub Actions workflow run. It checks for a configurable set of "forbidden" commands, patterns, or actions. If any are detected, it can fail the workflow, add a warning comment, or simply log the suspicious activity.

## Usage

To use the Workflow Guard Dog, add the following to your GitHub Actions workflow file:

```yaml
name: My Workflow with Guard Dog

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Workflow Guard Dog
        uses: polsala/ApocalypsAI/nightly-workflow-guard-dog@main # Replace with actual repo/tag
        with:
          forbidden_patterns: |
            rm -rf /
            git push --force
            curl http://malicious.site
          fail_on_detection: true # Set to false to only warn

      - name: Your other build steps
        run: echo "Building..."
```

## Inputs

*   `forbidden_patterns` (optional): A multi-line string where each line is a regex pattern to search for within workflow commands. If any pattern matches, the Guard Dog will trigger.
*   `fail_on_detection` (optional, default: `true`): If `true`, the action will fail the workflow run upon detecting a forbidden pattern. If `false`, it will only add a warning comment to the run.

## Example Forbidden Patterns

*   `rm -rf /`: A classic dangerous command.
*   `git push --force`: Force pushing can overwrite history and cause issues.
*   `curl http://malicious.site`: Blocking access to known malicious sites.
*   `eval `: Potentially dangerous command execution.

## Contributing

Contributions are welcome! Please open an issue or a pull request.
