# Nightly Chronicle Entry Reminder

## 📜 About This Utility

In the grand tapestry of our repository's history, every Pull Request weaves a new thread. The `nightly-chronicle-entry-reminder` is a whimsical-yet-wise GitHub Action designed to ensure that no significant event goes unrecorded. It gently nudges contributors to include a 'Chronicle Entry' (a changelog or release note) in their PR description, ensuring our historical archives are always complete and sparkling with clarity.

Think of it as your friendly, automated librarian, making sure every new chapter has its proper summary!

## ✨ Features

*   **Automated Nudge:** Automatically checks PR descriptions for predefined keywords (e.g., "Chronicle Entry:", "Changelog:", "Release Notes:").
*   **Customizable Phrases:** Easily configure the phrases the action looks for.
*   **Friendly Reminders:** Posts a customizable, whimsical comment on the PR if an entry is missing.
*   **Status Check Integration:** Can fail the PR status check, preventing merges until the chronicle is updated.

## 🚀 How to Use

To integrate the `nightly-chronicle-entry-reminder` into your workflow, add the following step to your `.github/workflows/your-pr-workflow.yml` file. This action typically runs on `pull_request_target` or `pull_request` events.

```yaml
name: PR Chronicle Check
on:
  pull_request:
    types:
      - opened
      - reopened
      - synchronize

jobs:
  check_chronicle_entry:
    runs-on: ubuntu-latest
    steps:
      - name: Chronicle Entry Reminder
        uses: polsala/ApocalypsAI/.github/actions/nightly-chronicle-entry-reminder@main # Adjust path if this action is moved
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Customize the required phrase (regex supported)
          # required_phrase: 'My Custom Changelog:|Release Note:'
          # Optional: Customize the comment message
          # comment_message: 'Hark! A new tale unfolds, but its summary is missing!'
```

### Inputs

*   `github_token` (Required): Your GitHub token, usually `secrets.GITHUB_TOKEN`, used to post comments on the PR.
*   `required_phrase` (Optional): A regex pattern to search for in the PR description. Defaults to `'Chronicle Entry:|Changelog:|Release Notes:'`.
*   `comment_message` (Optional): The message posted as a comment on the PR if the required phrase is not found. Defaults to a friendly reminder.

### Outputs

*   `chronicle_entry_found`: A boolean (`true` or `false`) indicating whether the required phrase was found in the PR description.

## 🛠️ Development & Testing

This action's core logic resides in `src/check_chronicle_entry.sh`. Tests are implemented as a shell script in `tests/test_check_chronicle_entry.sh` that directly invokes the core script with mock inputs.

To run tests locally:

```bash
bash tests/test_check_chronicle_entry.sh
```

## 💖 Contributing

Got an idea for a new chapter in our chronicle? Or perhaps a more eloquent reminder? Contributions are welcome! Feel free to open an issue or submit a Pull Request.
