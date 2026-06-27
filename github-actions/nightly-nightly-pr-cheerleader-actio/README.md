# Nightly PR Cheerleader Action

## 🌟 Celebrate Every Win! 🌟

This GitHub Action brings a dose of whimsy and encouragement to your pull requests and issues. It listens for specific positive emoji reactions on comments and, when detected, automatically posts a cheerful, pre-defined affirmation.

Foster a more positive and supportive development environment, one reaction at a time!

## How it Works

1.  **Trigger**: The action is triggered when a reaction is added to an `issue_comment` or `pull_request_review_comment`.
2.  **Emoji Check**: It checks if the added reaction is one of the configured 'cheer' emojis (e.g., `:+1:`, `:sparkles:`, `:tada:`).
3.  **Affirmation**: If a matching emoji is found, the action selects a random affirmation from its internal list (or a custom file).
4.  **Comment**: A new comment containing the affirmation is posted to the relevant issue or pull request.

## Inputs

| Input Name          | Description                                                                                             | Required | Default Value                               |
| :------------------ | :------------------------------------------------------------------------------------------------------ | :------- | :------------------------------------------ |
| `github-token`      | **Required**. GitHub token with permissions to add comments (e.g., `${{ secrets.GITHUB_TOKEN }}`).      | `true`   | None                                        |
| `reaction-emojis`   | Comma-separated list of emojis (without colons) to trigger the cheer.                                   | `false`  | `+1,sparkles,tada,rocket,eyes,heart,hooray` |
| `affirmations-file` | Path to a file containing custom affirmations, one per line. If not provided, uses an internal default list. | `false`  | None                                        |

## Example Usage

To use this action, add a workflow file (e.g., `.github/workflows/cheerleader.yml`) to your repository:

```yaml
name: PR Cheerleader

on:
  issue_comment:
    types: [reacted]
  pull_request_review_comment:
    types: [reacted]

jobs:
  cheer:
    runs-on: ubuntu-latest
    steps:
      - name: Nightly PR Cheerleader Action
        uses: polsala/ApocalypsAI/nightly-pr-cheerleader-action@main # Adjust 'main' to your branch if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          reaction-emojis: '+1,sparkles,tada,rocket'
          # affirmations-file: './.github/affirmations.txt' # Uncomment to use a custom file
```

### Custom Affirmations File Example (`.github/affirmations.txt`)

```
Your code is a masterpiece!
This is truly inspiring work!
Keep up the fantastic effort!
The void is pleased with your progress!
```

## Default Affirmations

If no `affirmations-file` is provided, the action will choose from these:

*   "You're a star! Keep shining!"
*   "Fantastic work! The void is proud!"
*   "Your brilliance illuminates the darkest corners!"
*   "A true beacon of progress!"
*   "This is truly apocalyptic-ally awesome!"
*   "Keep up the stellar work, survivor!"
*   "Your efforts are building a better tomorrow, today!"
*   "Magnificent! A triumph against the entropy!"
*   "The cosmos applauds your dedication!"
*   "Absolutely radiant! What a contribution!"

## Development

To run tests or develop locally:

```bash
npm install
npm test
```
