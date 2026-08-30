# Nightly Workflow Schedule Harmonizer

This GitHub Action ensures temporal consistency across your repository's automated processes by verifying that all workflows triggered by a `schedule` event adhere to a single, predefined "harmonized" cron schedule.

In the chaotic post-apocalyptic landscape of continuous integration, maintaining a synchronized rhythm for your automated tasks is crucial. This utility acts as a temporal guardian, flagging any workflow that dares to drift from the collective chronal pulse.

## Usage

To use the `nightly-workflow-schedule-harmonizer` action, add it as a step in one of your repository's workflows. It's recommended to run this check periodically, perhaps as part of a nightly health check or on every push to `main`.

```yaml
name: Workflow Chrono-Sync Check
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 3 * * *' # Run daily at 03:00 UTC

jobs:
  harmonize_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Harmonize Workflow Schedules
        id: harmonizer
        uses: polsala/ApocalypsAI/.github/actions/nightly-workflow-schedule-harmonizer@main # Adjust path if moved
        with:
          expected-cron-schedule: '0 0 * * *' # All scheduled workflows must run at midnight UTC
      - name: Report Desynchronized Workflows
        if: failure() && steps.harmonizer.outputs.desynchronized-workflows != ''
        run: |
          echo "The following workflows are experiencing temporal desynchronization: ${{ steps.harmonizer.outputs.desynchronized-workflows }}"
          echo "Please adjust their 'on: schedule:' cron expressions to match the harmonized '0 0 * * *'."
```

## Inputs

-   `expected-cron-schedule` (required):
    The cron schedule string (e.g., `'0 0 * * *'`) that all scheduled workflows in `.github/workflows/` must adhere to. The action will fail if any scheduled workflow does not match this pattern.

## Outputs

-   `desynchronized-workflows`:
    A comma-separated string of workflow filenames (e.g., `workflow1.yml,workflow2.yml`) that do not match the `expected-cron-schedule`. This output is empty if all workflows are harmonized.

## How it Works

1.  Scans all `.yml` and `.yaml` files within the `.github/workflows/` directory.
2.  For each file, it uses `yq` to parse the `on.schedule` block and extract all defined `cron` expressions.
3.  Compares each extracted cron expression against the `expected-cron-schedule` input.
4.  If any workflow contains a `schedule` trigger with a cron expression that does not match, the workflow is marked as "desynchronized."
5.  If any desynchronized workflows are found, the action fails and outputs a list of the offending files. Otherwise, it succeeds.

## Development & Testing

Refer to `tests/test.yml` for examples of how to test this action locally or in a CI environment. The tests simulate various workflow configurations (harmonized, desynchronized, mixed) to ensure the action behaves as expected.
