# Nightly AI Reviewer GitHub Action

Automatically review pull requests using AI to provide code quality feedback and suggestions.

## Features

- Analyzes code changes in pull requests
- Provides AI-powered code review suggestions
- Checks for common code quality issues
- Generates actionable feedback

## Usage

Add this action to your repository's workflow:

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: AI Reviewer
        uses: polsala/ApocalypsAI/.github/actions/nightly-ai-reviewer-github-action@main
        with:
          openrouter-api-key: ${{ secrets.OPENROUTER_API_KEY }}
          model: "anthropic/claude-3-5-sonnet"
          max-tokens: 2000
          temperature: 0.3
```

## Inputs

- `openrouter-api-key`: Your OpenRouter API key (required)
- `model`: The AI model to use (default: "anthropic/claude-3-5-sonnet")
- `max-tokens`: Maximum tokens for the response (default: 2000)
- `temperature`: Creativity parameter (default: 0.3)

## Outputs

- `review-comment`: The AI-generated review comment

## License

MIT
