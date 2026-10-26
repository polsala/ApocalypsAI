# Nightly ApocalypsAI Tone Checker

A GitHub Action that ensures your Pull Request titles and descriptions resonate with the unique "whimsical apocalypse" tone of the ApocalypsAI project. It checks for a balance of both whimsical and doom-related keywords, providing feedback to help maintain the project's distinct voice.

## 🌟 Why use this?

In the chaotic yet charming world of ApocalypsAI, maintaining a consistent tone is crucial. This action acts as a friendly guardian, ensuring that new contributions embrace both the lighthearted whimsy and the underlying sense of impending doom that defines our collective. It helps contributors craft messages that are both informative and on-brand.

## 🚀 Usage

To use this action, add it as a step in your GitHub workflow, typically on `pull_request` or `pull_request_target` events. The action will analyze the PR's title and body against a configurable list of keywords.

```yaml
name: PR Tone Check

on:
  pull_request:
    types: [opened, reopened, synchronize, edited]

jobs:
  check_tone:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: ApocalypsAI Tone Verification
        uses: polsala/ApocalypsAI/nightly-apocalypsai-tone-checker@main # Replace 'main' with your branch/tag if needed
        id: tone_check
        with:
          pr-title: ${{ github.event.pull_request.title }}
          pr-body: ${{ github.event.pull_request.body }}
          # Optional: Customize keywords and minimum counts
          # whimsy-keywords: 'sparkle,giggle,fluffy,serendipitous'
          # doom-keywords: 'apocalypse,wasteland,temporal,void'
          # min-whimsy-count: '1'
          # min-doom-count: '1'

      - name: Report Tone Status
        if: always()
        run: |
          echo "Tone Status: ${{ steps.tone_check.outputs.tone-status }}"
          echo "Tone Message: ${{ steps.tone_check.outputs.tone-message }}"
          # You can add further steps here, e.g., commenting on the PR or failing the build
          if [ "${{ steps.tone_check.outputs.tone-status }}" == "fail" ]; then
            echo "::error title=ApocalypsAI Tone Check::${{ steps.tone_check.outputs.tone-message }}"
            exit 1
          fi
```

## ⚙️ Inputs

| Input Name         | Description                                                               | Required | Default Value                                                                                             |
|--------------------|---------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------------|
| `pr-title`         | The title of the pull request.                                            | `true`   |                                                                                                           |
| `pr-body`          | The body of the pull request.                                             | `true`   |                                                                                                           |
| `whimsy-keywords`  | Comma-separated list of keywords indicating whimsy.                       | `false`  | `sparkle,giggle,fluffy,serendipitous,chuckle,delight,joyful,frolic,bubbly,gleeful`                        |
| `doom-keywords`    | Comma-separated list of keywords indicating doom.                         | `false`  | `apocalypse,wasteland,temporal,void,anomaly,rift,despair,ruin,cataclysm,oblivion`                         |
| `min-whimsy-count` | Minimum number of unique whimsical keywords required.                     | `false`  | `1`                                                                                                       |
| `min-doom-count`   | Minimum number of unique doom keywords required.                          | `false`  | `1`                                                                                                       |

## 📤 Outputs

| Output Name    | Description                                       |
|----------------|---------------------------------------------------|
| `tone-status`  | The result of the tone check (`pass` or `fail`).  |
| `tone-message` | A message detailing the tone check result.        |

## 🧪 Testing

The core logic of this action (`src/verify_tone.sh`) is tested using a self-contained bash script (`tests/test_verify_tone.sh`). These tests are deterministic and run offline, simulating various PR titles and bodies to ensure accurate tone detection.
