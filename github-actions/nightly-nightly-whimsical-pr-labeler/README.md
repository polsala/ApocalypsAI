## Whimsical PR Labeler

Automatically applies whimsical labels to PRs based on file count:
- 🌱 Solo Survivor (1 file)
- 🧑‍🤝‍🧑 Duo Duo (2-5 files)
- 🤝 Tribe Triage (6-10 files)
- 🌪️ Wasteland Wave (11+ files)

Add to your workflow with:
```yaml
- uses: actions/labeler@v1
  with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    labels: '🌱,🧑‍🤝‍🧑,部落,🌪️'
```
