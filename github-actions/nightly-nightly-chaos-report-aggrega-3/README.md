# nightly-chaos-report-aggregator

A GitHub Action to collect and summarize chaos engineering experiment results across multiple workflow runs into a single markdown dashboard.

## Features

- Scans specified directories or artifacts for chaos reports
- Aggregates success/failure metrics
- Generates a human-readable markdown summary
- Outputs structured data for downstream use

## Usage

In your workflow YAML:

```yaml
- name: Aggregate Chaos Reports
  uses: polsala/ApocalypsAI/utils/nightly-chaos-report-aggregator@main
  with:
    input-dir: 'chaos-reports'
    output-file: 'chaos-summary.md'
```

### Inputs

| Input       | Description                      | Default           |
|-------------|----------------------------------|-------------------|
| `input-dir` | Directory containing report files | `chaos-reports`   |
| `output-file` | Path to write summary markdown     | `chaos-summary.md` |

### Outputs

- `summary-path`: Path to the generated markdown summary
- `total-runs`: Total number of chaos runs processed
- `failed-runs`: Number of failed chaos runs

## Example Output

```
# Chaos Engineering Summary

- Total Runs: 12
- Failed Runs: 2
- Success Rate: 83.33%

## Failures

- Run ID: `network-failure-2025-04-05`
- Run ID: `disk-stress-2025-04-05`
```
