# Apocalypse Forecast Action

A whimsical GitHub Action that generates an apocalypse‑themed forecast based on the number of open issues and pull requests in your repository. Use it in CI to add a fun comment or log.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `issue_count` | Number of open issues in the repository | Yes |
| `pr_count` | Number of open pull requests in the repository | Yes |
| `github_token` | (Optional) GitHub token to post a comment on the PR. If omitted the forecast is only printed to the log. | No |

## Outputs

| Name | Description |
|------|-------------|
| `forecast` | The generated apocalypse forecast string |

## Example workflow

```yaml
name: Apocalypse Forecast

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  forecast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate forecast
        id: forecast
        uses: ./
        with:
          issue_count: ${{ github.event.repository.open_issues_count }}
          pr_count: ${{ github.event.pull_request.comments }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
      - name: Show forecast
        run: echo "Forecast: ${{ steps.forecast.outputs.forecast }}"
```

## License

MIT © ApocalypsAI
