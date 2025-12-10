# Wasteland Issue Guardian

A GitHub Action that adds a random survival tip and `wasteland-guardian` label to every new issue. Keeps your team hydrated with wisdom in the digital desert.

## Workflow Example
```yaml
name: Wasteland Guardian
on: [issues]

jobs:
  guard:
    runs-on: ubuntu-latest
    steps:
      - name: Add survival wisdom
        uses: polsala/ApocalypsAI@main/nightly-wasteland-issue-guardian/
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          tips-file: 'survival_tips.yaml'
```

## Customization
Add your own tips in `survival_tips.yaml` format:
```yaml
- "Remember to hydrate your code with comments"
- "No commit without a test - it's radioactive out there!"
- "Merge only when the moon is waxing crescent"
```
