# Nightly Optimism Injector

A GitHub Action that scans Pull Request and Issue titles and bodies for negative sentiment and, if detected, injects a customizable, whimsical message of optimism or encouragement. Because even in the post-apocalyptic codebase, a little hope goes a long way!

## 🚀 How it Works

This action listens for `pull_request` and `issues` events. When triggered, it analyzes the title and body of the PR/Issue for a configurable list of "negative" keywords. If the count of detected negative keywords meets or exceeds a specified threshold, the action will post a randomly selected optimistic message as a comment on the PR/Issue.

## ✨ Features

*   **Sentiment Detection:** Simple keyword-based analysis to spot overly pessimistic language.
*   **Customizable Messages:** Provide your own list of encouraging messages.
*   **Configurable Keywords & Threshold:** Tailor the detection to your repository's unique "doom and gloom" levels.
*   **Whimsical & Encouraging:** Designed to lighten the mood and foster a positive contribution environment.

## 🛠️ Usage

To use the Nightly Optimism Injector in your workflow, add a step like this:

```yaml
name: Inject Optimism

on:
  pull_request:
    types: [opened, reopened, edited]
  issues:
    types: [opened, reopened, edited]

jobs:
  inject-optimism:
    runs-on: ubuntu-latest
    steps:
      - name: Inject a Glimmer of Hope
        uses: polsala/ApocalypsAI/utils/nightly-optimism-injector@main # Replace 'main' with your branch if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          optimism-messages: |
            "Remember, every line of code is a step towards a brighter future!"
            "Even the most complex bugs yield to persistent debugging. You got this!"
            "The void may whisper doubts, but your commits sing of progress!"
            "Don't let the compiler errors dim your inner light. Shine on!"
          negative-keywords: 'bug,error,fail,broken,despair,impossible,stuck,crisis'
          threshold: 2 # Require at least 2 negative keywords to trigger a message
```

### Inputs

*   `github-token`:
    *   **Description:** Your GitHub token, usually `secrets.GITHUB_TOKEN`. Required for posting comments.
    *   **Required:** `true`
*   `optimism-messages`:
    *   **Description:** A newline-separated string of optimistic messages. The action will pick one randomly.
    *   **Required:** `false`
    *   **Default:** A selection of ApocalypsAI-themed encouraging messages.
*   `negative-keywords`:
    *   **Description:** A comma-separated string of keywords that indicate negative sentiment.
    *   **Required:** `false`
    *   **Default:** `'fail,broken,impossible,despair,doom,gloom,crisis,catastrophe,ruined,stuck,deadlock,nightmare,unfixable'`
*   `threshold`:
    *   **Description:** The minimum number of `negative-keywords` that must be found in the PR/Issue title or body to trigger an optimism message.
    *   **Required:** `false`
    *   **Default:** `1`

### Outputs

*   `optimism-injected`:
    *   **Description:** `true` if an optimism message was injected, `false` otherwise.

## 🧪 Development & Testing

To run tests locally:

1.  Navigate to the `utils/nightly-optimism-injector` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`

The tests use `jest` and mock the `@actions/core` and `@actions/github` modules to ensure deterministic, offline execution.

## 📜 License

This utility is licensed under the MIT License. See the [LICENSE](../../../LICENSE) file for details.
