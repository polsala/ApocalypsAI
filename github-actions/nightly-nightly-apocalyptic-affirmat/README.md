# Apocalyptic Affirmation Bot

A GitHub Action that comments cryptic motivational messages on PRs/Issues using apocalyptic metaphors. Configure it to trigger on `pull_request` or `issues` events.

## Configuration
Add to your workflow:
```yaml
- uses: polsala/ApocalypsAI@main
  with:
    classifier: github-actions
    util_name: nightly-apocalyptic-affirmation-bot
```
