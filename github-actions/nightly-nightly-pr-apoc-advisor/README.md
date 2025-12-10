# Nightly PR Apoc Advisor

A GitHub Action that injects a dose of whimsical apocalyptic wisdom into your Pull Request workflow. This action checks if a PR description contains a "survival tip" or "apocalyptic wisdom" keyword. If not, it adds a comment to the PR with a random, helpful (or humorously unhelpful) piece of advice for navigating the end times.

## 🚀 Usage

To use the `nightly-pr-apoc-advisor` action, add it to your workflow, typically on `pull_request_target` or `pull_request` events.

```yaml
name: PR Apoc Advisor

on:
  pull_request_target:
    types: [opened, reopened, edited]

jobs:
  advise:
    runs-on: ubuntu-latest
    steps:
      - name: Check for Apocalyptic Wisdom
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-apoc-advisor@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: keyword to look for in the PR description
          # If found, no advice will be given.
          # default: "survival tip"
          # wisdom-keyword: "apocalyptic wisdom"
```

### Inputs

- `github-token`: **Required**. Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`.
- `wisdom-keyword`: **Optional**. A keyword or phrase to look for in the PR description. If this keyword is found, the action assumes wisdom has already been provided and will not post a new comment. Defaults to `"survival tip"`.

## 🛠️ Development

### Setup

```bash
npm install
```

### Running Tests

```bash
npm test
```

### Building the Action

This action uses `ncc` to bundle the JavaScript into a single file for distribution. Run the build command before committing changes if you intend to update the `dist/index.js` file.

```bash
npm run build
```

## 📜 Apocalyptic Wisdoms

A selection of the profound insights this action might share:

- "Always know where your towel is. It's not just for hitchhikers anymore."
- "Remember, duct tape fixes everything, even existential dread."
- "A well-maintained zombie apocalypse plan is a happy apocalypse plan."
- "Hydration is key, especially when fleeing mutant squirrels."
- "Never trust a robot offering free hugs."
- "The best defense against a rogue AI is a good offense... or a really bad Wi-Fi signal."
- "Keep your emergency snacks close, and your emergency memes closer."
- "When in doubt, blame the temporal anomaly."
- "If you hear banjo music, run. If you don't hear banjo music, still run, just in case."
- "Always carry a spare pair of socks. You never know when you'll need to cross a radioactive puddle."
- "A good pair of boots will outlast any apocalypse."
- "Learn to identify edible fungi. Or, more importantly, inedible fungi."
- "Solar power is your friend. Unless it's a cloudy apocalypse."
- "Barter skills are more valuable than gold. Unless you're bartering for gold."
- "Don't forget to laugh. Even if it's a maniacal, end-of-the-world laugh."
