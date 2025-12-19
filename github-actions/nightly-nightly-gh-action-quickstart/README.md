# Nightly GH Action Quickstart

This GitHub Action automatically creates a minimal, runnable workflow file for a new repository on the first push.

## Features

* Detects if a workflow file already exists.
* Creates a new workflow file with a customizable name.
* Allows you to specify the trigger event and branch.
* Generates a job with customizable steps.
* Uses a composite action for easy integration.

## Usage

Add the following step to any workflow:

```yaml
- name: Quickstart Workflow
  uses: polsala/ApocalypsAI/nightly-gh-action-quickstart@main
  with:
    workflow-name: "my-workflow.yml"
    run-on: "push"
    run-on-branch: "main"
    job-name: "my-job"
    steps: |
      [{"name": "Checkout", "uses": "actions/checkout@v4"}, {"name": "Hello World", "run": "echo \"Hello, world!\""}]
```

## Inputs

| Name | Description | Default |
| --- | --- | --- |
| `workflow-name` | The name of the generated workflow file. | `nightly-quickstart.yml` |
| `run-on` | The event that triggers the workflow. | `push` |
| `run-on-branch` | The branch that triggers the workflow. | `main` |
| `job-name` | The name of the generated job. | `quickstart` |
| `steps` | A JSON array of steps to add to the job. | Checkout + Hello World |

## Outputs

None.

## License

MIT
