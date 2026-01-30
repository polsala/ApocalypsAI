# nightly-action-commit-emoji-annotator

A tiny GitHub Action that reads the latest commit message of a push event and adds an emoji reaction to the commit. The emoji is chosen whimsically based on the content of the message:

- **"fix"** → 👍 (`+1`)
- **"feat"** → 🚀 (`rocket`)
- **"docs"** → 📖 (`book`)
- Anything else → 👀 (`eyes`)

## Usage

Add the action to a workflow that runs on `push` events:

```yaml
name: Emoji Annotator
on: push
jobs:
  annotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Add emoji reaction
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The action expects the `GITHUB_TOKEN` (or a PAT with `repo` scope) to be provided via the `github-token` input.

## How it works

1. The action loads the event payload from `GITHUB_EVENT_PATH` (provided by GitHub).
2. It extracts the commit SHA and the commit message.
3. A simple keyword‑based selector chooses an emoji.
4. Using the Octokit REST client, the action creates a reaction on the commit.

## Testing

Run the bundled test script locally:

```bash
npm install
node tests/test_selectEmoji.js
```

The test verifies the emoji‑selection logic without contacting the GitHub API.

## License

MIT © ApocalypsAI
