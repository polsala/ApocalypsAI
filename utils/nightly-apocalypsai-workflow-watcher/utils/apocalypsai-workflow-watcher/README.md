# ApocalypsAI Workflow Watcher

## Overview

The `apocalypsai-workflow-watcher` is a crucial utility for the ApocalypsAI collective, designed to keep a vigilant eye on the health of our GitHub Actions workflows. It queries the GitHub API to fetch the latest run status for all workflows in the `polsala/ApocalypsAI` repository.

But this isn't just a dry status report! The Watcher delivers its findings with a touch of dramatic flair, letting you know if the gears of fate are grinding smoothly or if a digital apocalypse is on the horizon.

## Features

-   **Workflow Status Monitoring**: Fetches the latest run status for each unique workflow.
-   **Whimsical Reporting**: Provides themed messages based on the overall workflow health.
-   **Self-Contained**: Requires only a `GITHUB_TOKEN` environment variable.

## How to Run

1.  **Prerequisites**: Ensure you have Python 3.11+ installed.
2.  **Authentication**: You need a GitHub Personal Access Token (PAT) with `repo` scope. Set it as an environment variable:
    ```bash
    export GITHUB_TOKEN="YOUR_GITHUB_PAT"
    ```
3.  **Execution**: Navigate to the utility's directory and run the script:
    ```bash
    cd utils/apocalypsai-workflow-watcher/src
    python workflow_watcher.py
    ```

## Expected Output

The script will print a summary message to the console, indicating the overall health of the workflows.

**Example (All Success):**
```
The gears of fate grind smoothly. ApocalypsAI operations are nominal. All systems green!
```

**Example (Some Failures):**
```
A tremor in the timeline! Critical systems are faltering. Immediate intervention required to avert digital doom!

Failing Workflows:
-   gen_openrouter.yml (Failure 2023-10-27 10:30:00)
-   test_and_eval.yml (Cancelled 2023-10-27 10:45:00)
```

**Example (No Runs Found):**
```
The void stares back. No workflow activity detected. Is this the calm before the storm, or have we already fallen?
```

## Development

To run tests, navigate to the `tests` directory and use `python -m unittest`:

```bash
cd utils/apocalypsai-workflow-watcher/tests
python -m unittest test_workflow_watcher.py
```
