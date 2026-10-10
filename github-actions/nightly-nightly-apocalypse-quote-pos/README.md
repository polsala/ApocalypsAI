# Nightly Apocalypse Quote Poster

A reusable GitHub Actions workflow that posts a random post‑apocalypse themed quote as a comment on a chosen issue each night. Perfect for keeping your repository morale high during the end times.

## Inputs
- `github_token` (required): A token with `repo` scope to authenticate the API request.
- `issue_number` (required): The issue number where the quote will be posted.
- `quotes` (optional): A multiline string of quotes; one per line. If omitted, a built‑in list is used.

## Usage
```yaml
name: Daily Quote
on:
  schedule:
    - cron: '0 9 * * *' # every day at 09:00 UTC

jobs:
  post-quote:
    uses: ./.github/actions/nightly-apocalypse-quote-poster
    with:
      github_token: ${{ secrets.GITHUB_TOKEN }}
      issue_number: 42
```

## How it works
The workflow selects a random line from the provided `quotes` input (or the internal list) and posts it as a comment on the specified issue using the GitHub REST API.

## License
MIT
