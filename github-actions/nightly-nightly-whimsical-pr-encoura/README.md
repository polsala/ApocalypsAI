# Nightly Whimsical PR Encourager

This GitHub Action adds a touch of post-apocalyptic whimsy and encouragement to every newly opened Pull Request in your repository. It's designed to foster a friendly and engaging community by greeting contributors with a random, light-hearted message.

## ✨ Features

-   **Automatic Encouragement**: Posts a random, pre-defined whimsical message to new PRs.
-   **Customizable Messages**: Allows you to provide your own JSON array of messages.
-   **Community Building**: Adds a unique, fun element to your development workflow.

## 🚀 Usage

Create a workflow file (e.g., `.github/workflows/whimsical-pr.yml`) in your repository:

```yaml
name: Whimsical PR Encouragement

on: pull_request_target

jobs:
  encourage:
    runs-on: ubuntu-latest
    steps:
      - name: Add Whimsical Encouragement
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsical-pr-encourager@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Provide custom messages as a JSON array
          # messages: |-
          #   [
          #     "May your code be as resilient as a cockroach after the blast!",
          #     "A new PR emerges from the digital dust! We salute your bravery!"
          #   ]
```

**Note on `pull_request_target`**: This trigger is used to allow the action to post comments with `GITHUB_TOKEN` even from forks. Be cautious when using `pull_request_target` with actions that execute untrusted code from the PR. This action only reads context and posts a pre-defined message, making it relatively safe.

## ⚙️ Inputs

| Name           | Description                                    | Required | Default |
| :------------- | :--------------------------------------------- | :------- | :------ |
| `github-token` | GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`). | `true`   |         |
| `messages`     | JSON array of custom whimsical messages. If empty or invalid, default messages are used. | `false`  | `[]`    |

## 📤 Outputs

| Name         | Description             |
| :----------- | :---------------------- |
| `comment-id` | The ID of the created comment. |

## 💬 Example Whimsical Messages

-   "Behold, a new PR sprouts! May your code be as robust as a mutant cactus in the wasteland."
-   "A wild PR appeared! It's super effective! Go forth and conquer, brave coder!"
-   "The stars align, the void whispers... and a Pull Request is born! May its path be bug-free and its merges swift."
-   "Greetings, traveler! Your PR has arrived, bearing gifts of code. May the ancient algorithms bless its journey."
-   "The ApocalypsAI Integrator smiles upon this Pull Request. May your merge be legendary!"
