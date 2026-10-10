# Nightly Apocalypse Reaction

## Overview

`nightly-apocalypse-reaction` is a tiny GitHub Actions workflow that brings a bit of post‑apocalyptic flair to your repository. Whenever a new issue is opened, the workflow:

1. Picks a random apocalypse‑themed emoji (☢️, 💥, 🔥, ⚡, 🌪️, ☄️, 🧟‍♂️, 🧟‍♀️, 🦖, 🦕) and adds it as a reaction to the issue.
2. Posts a short, whimsical comment such as "Brace yourself, the apocalypse is nigh!".

The action is completely self‑contained, requires no secrets, and runs on the default `ubuntu-latest` runner.

## Installation

Add the workflow file to your repository under `.github/workflows/`:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/apocalypse-reaction.yml \
  https://raw.githubusercontent.com/<your‑org>/<your‑repo>/main/github-actions/nightly-apocalypse-reaction/.github/workflows/apocalypse-reaction.yml
```

Commit and push the change. The workflow will automatically trigger on every new issue.

## Customisation

If you want to customise the emoji list or the comment pool, edit the `script` sections of the workflow. The lists are defined as JavaScript arrays named `emojis` and `messages`.

## License

MIT © ApocalypsAI
