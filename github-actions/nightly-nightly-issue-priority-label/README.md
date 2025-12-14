# Issue Priority Labeler

A GitHub Action that automatically determines a priority label for an issue based on keywords in its title.

## Inputs

- `title` – The issue title (required).
- `priority_keywords` – JSON string mapping priority levels to arrays of keywords. Example: `{\"critical\":[\"crash\",\"down\"],\"high\":[\"error\",\"fail\"],\"medium\":[\"slow\",\"lag\"],\"low\":[\"typo\",\"suggestion\"]}` (optional, defaults to a built‑in set).

## Outputs

- `label` – The priority label that was selected (`critical`, `high`, `medium`, `low`, or `untriaged`).

## Usage

```yaml
steps:
  - uses: actions/checkout@v3
  - name: Set priority label
    id: priority
    uses: ./nightly-issue-priority-labeler
    with:
      title: ${{{{ github.event.issue.title }}}}
  - name: Apply label
    uses: actions-ecosystem/action-add-labels@v1
    with:
      labels: ${{{{ steps.priority.outputs.label }}}}
```

## How it works

The action parses the `priority_keywords` mapping (or uses the default) and checks the issue title for any of the keywords, case‑insensitively. The first matching priority in the order `critical → high → medium → low` is returned. If no keywords match, the label `untriaged` is returned.
