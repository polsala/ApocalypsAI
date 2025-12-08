## nightly-automated-whimsy-comment

Adds a daily whimsical comment to a designated GitHub issue with a randomized quote and emoji. Configure `ISSUE_NUMBER` and `GITHUB_TOKEN` in workflow secrets.

**Workflow example:**
```yaml
- uses: polsala/ApocalypsAI@main
  with:
    classifier: github-actions
    util_name: nightly-automated-whimsy-comment
```
