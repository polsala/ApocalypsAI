# nightly-pr-quote-commenter

## Overview

`nightly-pr-quote-commenter` is a **GitHub Action** that automatically leaves a light‑hearted, randomly chosen quote as a comment on every newly opened pull request.  It adds a splash of personality to the PR review process while keeping the implementation simple and dependency‑free.

## Why a Quote?

* **Encourage contributors** – A friendly line can make a reviewer smile.
* **Break the ice** – Great for open‑source projects where contributors may be strangers.
* **Whimsical flair** – Fits the ApocalypsAI spirit of “anarchy with discipline”.

## How it works

The action is a **composite action** that runs two steps:
1. **Select a quote** – a small Bash script picks a random entry from a built‑in list.
2. **Post the comment** – using `curl` and the `GITHUB_TOKEN` secret, it creates a comment on the PR via the GitHub REST API.

Because it uses only Bash and `curl`, there are no extra runtime dependencies.

## Usage

Add the following to your workflow (e.g. `.github/workflows/pr-quote.yml`):

```yaml
name: PR Quote Commenter
on:
  pull_request:
    types: [opened]

jobs:
  add-quote:
    runs-on: ubuntu-latest
    steps:
      - name: Run PR Quote Commenter
        uses: ./github-actions/nightly-pr-quote-commenter
        with: {}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> **Note**: The action expects the `GITHUB_TOKEN` secret (automatically provided by GitHub Actions) to be passed as an environment variable.

## Customising the Quote List

If you want to tailor the quotes, edit `src/quotes.txt`.  Each line is treated as a separate quote.

## Testing

A deterministic test script is provided under `tests/`.  It runs the quote‑selection script and verifies that the output follows the `quote=` format.

```bash
bash tests/test_select_quote.sh
```

## License

MIT – see the root `LICENSE` file.
