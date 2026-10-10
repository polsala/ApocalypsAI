# Nightly Cosmic Commit Aligner

## 🌌 Align Your Commits with Celestial Harmony 🌌

This GitHub Action ensures your commit messages resonate with the positive vibrations of the cosmos! It checks for "cosmic alignment" by analyzing the commit message for positive keywords, avoiding negative ones, and adhering to a sensible length. Keep your repository's commit history a beacon of clarity and good vibes!

### ✨ How it Works

The action performs the following checks on the latest commit message:
1.  **Positive Vibe Check**: Ensures the message contains at least one "positive" keyword (e.g., `feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`, `build`, `ci`, `perf`, `revert`, `improve`, `add`). This check is skipped if no positive keywords are configured.
2.  **Negative Energy Shield**: Detects and flags "negative" keywords (e.g., `broken`, `fail`, `buggy`, `mess`, `oops`, `ugh`, `bad`). This check is skipped if no negative keywords are configured.
3.  **Length Resonance**: Checks if the message is within a "harmonious" length (e.g., between 10 and 100 characters).

If all checks pass, the commit is deemed "Cosmically Aligned" and the status check passes. Otherwise, it fails, guiding you towards a more harmonious commit message.

### 🚀 Usage

Add this action to your workflow file (e.g., `.github/workflows/cosmic_align.yml`):

```yaml
name: Cosmic Commit Alignment Check

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    types: [opened, synchronize, reopened, edited]

jobs:
  align_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 1 # Only fetch the latest commit

      - name: Run Cosmic Commit Aligner
        id: cosmic_align
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-commit-aligner@main # Adjust 'main' to your branch or tag
        with:
          commit-message: "${{ github.event.head_commit.message }}" # Pass the commit message
          # Optional: Customize keywords and length
          # positive-keywords: "feat,fix,chore,docs,refactor,style,test,build,ci,perf,revert,improve,add,update"
          # negative-keywords: "broken,fail,buggy,mess,oops,ugh,bad,error"
          # min-length: 10
          # max-length: 100

      - name: Report Alignment Status
        if: failure()
        run: echo "::error::Commit message failed cosmic alignment: ${{ steps.cosmic_align.outputs.reason }}"
```

### ⚙️ Inputs

*   `commit-message` (Required): The commit message string to check.
*   `positive-keywords` (Optional): Comma-separated list of keywords that should be present. Default: `feat,fix,chore,docs,refactor,style,test,build,ci,perf,revert,improve,add,update`. If empty, this check is skipped.
*   `negative-keywords` (Optional): Comma-separated list of keywords that should NOT be present. Default: `broken,fail,buggy,mess,oops,ugh,bad,error`. If empty, this check is skipped.
*   `min-length` (Optional): Minimum allowed length for the commit message. Default: `10`
*   `max-length` (Optional): Maximum allowed length for the commit message. Default: `100`

### 📤 Outputs

*   `aligned` (boolean): `true` if the commit message is aligned, `false` otherwise.
*   `reason` (string): A message explaining why the alignment failed (if `aligned` is `false`).

### 💺 Development

To test locally, ensure you have `bash` available.
The `src/check_commit.sh` script can be run directly:

```bash
# Example of a good commit
./src/check_commit.sh "feat: Add new cosmic alignment sensor" "feat,fix" "broken" "10" "100"

# Example of a bad commit (too short)
./src/check_commit.sh "fix" "feat,fix" "broken" "10" "100"

# Example of a bad commit (negative keyword)
./src/check_commit.sh "fix: Ugh, this was broken" "feat,fix" "broken,ugh" "10" "100"
```
