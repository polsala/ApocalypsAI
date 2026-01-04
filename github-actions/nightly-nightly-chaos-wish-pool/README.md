# Nightly Chaos Wish Pool

A whimsical GitHub Action that randomly selects and executes community-approved chaos scenarios, adding delightful unpredictability to your repository.

## Features
- Randomly chooses from a curated list of chaos scenarios
- Executes approved actions like deleting temporary files, renaming branches, or creating funny commits
- Fully reversible with automatic cleanup
- Safe by design - only runs on non-production branches

## Usage
Add this action to your workflow:
```yaml
- uses: actions/checkout@v4
- name: Grant chaotic wish
  uses: ./utils/nightly-chaos-wish-pool
  with:
    scenario-file: ".github/chaos_scenarios.yml"
```

## Scenarios
Scenarios are defined in YAML format:
```yaml
scenarios:
  - name: "Rename to magic"
    description: "Rename main branch to something whimsical"
    type: branch-rename
    params:
      new_name: "enchanted-main"
      duration: 300
  - name: "File shuffle"
    description: "Temporarily move some files around"
    type: file-shuffle
    params:
      files:
        - ".github/workflows/"
        - "README.md"
      duration: 60
```

## Safety
- Only runs on branches matching `.*-test$`
- All changes are reverted within the specified duration
- No permanent damage is possible
- Requires explicit approval via `CHAOS_APPROVED=true` environment variable

## License
MIT
