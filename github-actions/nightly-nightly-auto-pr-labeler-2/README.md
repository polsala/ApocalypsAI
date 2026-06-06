# Auto PR Labeler

Utility that automatically adds a label to a pull request based on its title prefix. It ships as a reusable GitHub Actions workflow together with a tiny Node.js helper.

## Features
- Detects common semantic prefixes: `feat`, `fix`, `docs`, `chore`, `refactor`.
- Maps them to corresponding labels (`feature`, `bug`, `documentation`, `chore`, `refactor`).
- Works on PR events: opened, edited, reopened.
- No external dependencies beyond the built‑in `node` runtime.

## Installation
Add the workflow file to your repository:
```bash
mkdir -p .github/workflows
curl -o .github/workflows/auto-label-pr.yml https://raw.githubusercontent.com/your-org/your-repo/main/.github/workflows/auto-label-pr.yml
```
Commit the file and push. The workflow will run automatically on PR events.

## How it works
1. GitHub triggers the workflow on PR events.
2. The workflow checks out the repo and sets up Node.js.
3. `src/labeler.js` reads the PR title from the event payload (`GITHUB_EVENT_PATH`).
4. It determines the appropriate label and emits it as an output (`::set-output`).
5. In a real‑world scenario you would extend the script to call the GitHub REST API (using `GITHUB_TOKEN`) to apply the label. For safety in this sandbox we only output the label.

## Customization
- Edit `src/labeler.js` to add more prefix‑to‑label mappings.
- Replace the placeholder `console.log` with an actual API call if you need the label to be applied automatically.

## Testing
Run the bundled tests locally with Node:
```bash
node tests/test_labeler.js
```
All tests should pass, confirming the prefix detection logic works as expected.
