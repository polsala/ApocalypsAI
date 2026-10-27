# Nightly Cosmic PR Aligner

## 🌌 Align Your Pull Requests with the Cosmos! 🌠

This GitHub Action helps maintain a positive and consistent vibe across your pull requests by checking their titles and descriptions for 'cosmic alignment'. It can be configured to look for specific keywords, encourage positive language, or simply add a touch of whimsy to your development workflow.

If a PR is deemed 'misaligned' (e.g., contains negative or placeholder keywords), the action can post a helpful, whimsical suggestion. If it's 'aligned', it can celebrate the stellar contribution with a positive comment.

## ✨ Usage

To use the `nightly-cosmic-pr-aligner` in your workflow, add a step like this:

```yaml
name: Cosmic PR Alignment Check
on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  align_check:
    runs-on: ubuntu-latest
    steps:
      - name: Check Cosmic Alignment
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-pr-aligner@main # Or your specific branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          aligned-keywords: 'feat,fix,chore,docs,style,refactor,perf,test,build,ci,revert,✨,🚀,🎉,harmonious,stellar,radiant'
          misaligned-keywords: 'WIP,ugh,broken,temp,draft,bad,fixme,TODO'
          alignment-threshold: '1'
          misalignment-threshold: '1'
          comment-on-alignment: 'true'
          comment-on-misalignment: 'true'
```

## 🚀 Inputs

| Input Name              | Description                                                              | Required | Default Value                                                                                                 |
|-------------------------|--------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------|
| `github-token`          | GitHub token for API calls (e.g., `secrets.GITHUB_TOKEN`).               | Yes      |                                                                                                               |
| `aligned-keywords`      | Comma-separated list of keywords indicating cosmic alignment.            | No       | `feat,fix,chore,docs,style,refactor,perf,test,build,ci,revert,✨,🚀,🎉,harmonious,stellar,radiant` |
| `misaligned-keywords`   | Comma-separated list of keywords indicating cosmic misalignment.         | No       | `WIP,ugh,broken,temp,draft,bad,fixme,TODO`                                                                    |
| `alignment-threshold`   | Minimum number of aligned keywords to consider a PR 'aligned'.           | No       | `1`                                                                                                           |
| `misalignment-threshold`| Minimum number of misaligned keywords to consider a PR 'misaligned'.     | No       | `1`                                                                                                           |
| `comment-on-alignment`  | Whether to add a positive comment if the PR is aligned.                  | No       | `true`                                                                                                        |
| `comment-on-misalignment`| Whether to add a suggestion comment if the PR is misaligned.             | No       | `true`                                                                                                        |

## 🌟 Outputs

| Output Name   | Description                                     |
|---------------|-------------------------------------------------|
| `is-aligned`  | `true` if the PR is cosmically aligned, `false` otherwise. |

## 🛠️ Development

This action is written in JavaScript. To build and test locally:

1.  Install dependencies: `npm install`
2.  Run tests: `npm test`
3.  Build for distribution (if modifying `src/index.js`): `npm run build` (uses `@vercel/ncc`)

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
