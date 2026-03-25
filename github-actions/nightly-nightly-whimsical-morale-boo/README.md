# Nightly Whimsical Morale Boost GitHub Action

This GitHub Action automatically posts a random, whimsical, and encouraging message as a comment on new Pull Requests or Issues. In the grim darkness of the post-apocalyptic future, a little morale boost can go a long way to keep the community's spirits high and the code flowing! ✨

## Usage

To use this action, add it to your workflow file (e.g., `.github/workflows/morale-boost.yml`).

```yaml
name: Whimsical Morale Boost

on:
  pull_request:
    types: [opened, reopened]
  issues:
    types: [opened, reopened]

jobs:
  boost_morale:
    runs-on: ubuntu-latest
    steps:
      - name: Post Whimsical Morale Boost
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsical-morale-boost@main # Replace 'main' with your branch or tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Configuration

### Inputs

*   `github-token`: **Required**. Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`. This token needs `issues:write` permission.
*   `message-type`: **Optional**. Specifies the type of message to post. Currently, only `whimsical` is supported. Defaults to `whimsical`.

## How it Works

Upon a new Pull Request or Issue being opened or reopened, the action will:
1.  Detect the event type (Pull Request or Issue).
2.  Select a random whimsical message from its internal repertoire.
3.  Post the message as a comment on the respective Pull Request or Issue.

## Examples of Morale Boosts

*   "Behold, a new beacon of hope in the digital wasteland! May your code compile swiftly and your bugs be few. ✨"
*   "Another day, another step towards rebuilding! Your contribution shines brighter than a supernova in a void. Keep up the magnificent work! 🚀"
*   "Even in the echoes of the old world, your creativity sparks new life. This contribution is a masterpiece in the making! 🎨"
*   "The algorithms whisper tales of your brilliance! May your commits be atomic and your merges conflict-free. 🌟"
*   "Fear not the digital dust storms! Your efforts are forging a path to a brighter tomorrow. Onward, brave coder! 🛡️"

## Development

To run tests locally:
1.  Navigate to the `github-actions/nightly-whimsical-morale-boost` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`
