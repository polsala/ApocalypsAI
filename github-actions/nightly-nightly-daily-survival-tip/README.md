# Daily Survival Tip GitHub Action

Creates a whimsical daily survival tip as an issue in the repository. Useful for keeping contributors entertained and reminded of post‑apocalyptic best practices.

## Usage

```yaml
name: Daily Survival Tip
on:
  schedule:
    - cron: '0 9 * * *' # every day at 09:00 UTC
jobs:
  tip:
    runs-on: ubuntu-latest
    steps:
      - uses: ./  # assuming the action is checked out
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

The action selects a tip based on the day of the year and posts an issue titled **Daily Survival Tip**.

## Inputs

- `github_token` – Required. Token with `repo` scope to create issues.

## Implementation

The action runs a small Bash script (`src/tip.sh`) that:

1. Holds a static array of tips.
2. Picks one using the current day of year.
3. Calls the GitHub REST API to create an issue.

## Testing

Run the provided test script:

```sh
bash tests/test_tip.sh
```

It mocks `curl` and `date` to verify the correct tip is selected and the payload is formed.
