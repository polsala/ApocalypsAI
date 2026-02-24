# Nightly GitHub Action Debugger

This utility provides a reusable GitHub Actions workflow designed to help debug other workflows. It spins up a container with a variety of common debugging tools, allowing you to interactively explore the environment where your action is running or to execute specific commands.

## Purpose

When a GitHub Actions workflow fails unexpectedly, it can be challenging to diagnose the root cause, especially in complex or ephemeral environments. This workflow acts as a "debug console" for your CI/CD pipelines. You can trigger it manually or as part of a failing workflow to get a shell with tools like `curl`, `jq`, `git`, `docker`, `kubectl`, `awscli`, `gcloud`, and more pre-installed.

## Usage

To use this workflow, you can either:

1.  **Trigger it manually** from the Actions tab of your repository.
2.  **Call it from another workflow** using the `workflow_call` mechanism.

### Manual Trigger

Navigate to the "Actions" tab in your GitHub repository, select "Nightly GitHub Action Debugger" from the sidebar, and click "Run workflow". You can specify inputs to customize the environment.

### Calling from Another Workflow

Add the following to your existing workflow file:

```yaml
jobs:
  debug_my_action:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-debugger.yml@main
    with:
      # Optional: Specify a branch or tag if not using main
      # ref: main
      # Optional: Pass specific commands to run on startup
      # startup_commands: |
      #   echo "Starting custom commands..."
      #   ls -la
      #   curl -s https://api.github.com/users/octocat
      # Optional: Specify a different Docker image
      # docker_image: ubuntu:latest
```

## Inputs

*   `startup_commands` (optional): A multi-line string of shell commands to execute immediately after the container starts. This is useful for running specific diagnostic steps or setting up the environment before you connect.
*   `docker_image` (optional): The Docker image to use for the debugging environment. Defaults to a comprehensive image with many tools pre-installed. You can specify any valid Docker image.

## Outputs

This workflow primarily provides an interactive shell experience. Any output from `startup_commands` will be visible in the workflow run logs.

## Development & Testing

This workflow is designed to be self-contained. The `tests` directory contains a simple test that verifies the workflow can be triggered and execute basic commands.

To run tests locally:

1.  Ensure you have `act` installed (`pip install act`).
2.  Run `act --job debug_my_action --secret GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}` in the root of the repository.

(Note: For actual testing, you'd typically run this within a GitHub Actions environment or a simulated one like `act`.)
