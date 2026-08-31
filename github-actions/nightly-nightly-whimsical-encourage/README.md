# Nightly Whimsical Encouragement Action

This GitHub Action automatically posts a whimsical, encouraging comment on new pull requests or issues that have a specific label. It's designed to boost community morale and provide a friendly welcome or a little pick-me-up to contributors.

## Features

*   **Automated Encouragement**: Posts a random encouraging message from a configurable list.
*   **Label-Triggered**: Only activates when a specified label is present on the PR or issue.
*   **Customizable Messages**: Easily define your own set of whimsical messages.

## Usage

To use this action, add a step to your GitHub Actions workflow (e.g., `.github/workflows/morale.yml`):

```yaml
name: 'Community Morale Booster'

on:
  pull_request:
    types: [opened]
  issues:
    types: [opened]

jobs:
  encourage:
    runs-on: ubuntu-latest
    steps:
      - name: 'Whimsical Encouragement'
        uses: polsala/ApocalypsAI/nightly-whimsical-encourage@main # Or a specific release tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          label-to-trigger: 'needs-cheering'
          messages: |-
            [
              "Hark! A new beacon of brilliance has appeared! Your contribution shines brighter than a supernova!",
              "Behold, a masterpiece in the making! May your code be bug-free and your spirits high!",
              "The cosmos aligns for your magnificent effort! Keep up the stellar work!",
              "Even in the void, your creativity sparks like a thousand fireflies! Amazing!",
              "A wild contribution appeared! It's super effective at making our day!"
            ]
```

### Inputs

*   `github-token` (required):
    The GitHub token used to make API calls (e.g., `secrets.GITHUB_TOKEN`).
*   `label-to-trigger` (required):
    The name of the label that, when present on a new PR or issue, will trigger the action to post a comment. Example: `needs-cheering`.
*   `messages` (required):
    A JSON array of strings, where each string is a whimsical message. One will be randomly selected and posted as a comment.

## Development

### Setup

1.  Clone the repository.
2.  Navigate to `utils/nightly-whimsical-encourage`.
3.  Install dependencies: `npm install`

### Running Tests

`npm test`

## Contributing

Feel free to add more whimsical messages or suggest improvements!
