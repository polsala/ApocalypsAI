# Nightly Digital Garden Weeder

This Ansible playbook helps you maintain a tidy digital garden or personal knowledge base by identifying notes that are either 'stale' (not modified recently) or 'unlinked' (not referenced by other notes).

It generates a report and can optionally move identified files to a 'quarantine' directory, allowing you to review them for deletion, archiving, or integration.

## Features

*   **Staleness Detection**: Identifies markdown files that haven't been modified within a configurable threshold.
*   **Unlinked Note Detection**: Scans other markdown files to see if a note's filename (without extension) is referenced, helping find orphaned content.
*   **Comprehensive Report**: Generates a detailed report listing stale files, unlinked files, and those that are both (quarantine candidates).
*   **Optional Quarantine**: Safely moves identified 'quarantine candidates' to a designated directory for review, rather than immediate deletion.

## Prerequisites

*   Ansible (version 2.9 or newer recommended)
*   A local or remote system with markdown files to manage.

## Usage

1.  **Clone the repository** (or copy this utility's folder).
2.  **Configure your inventory**: The `src/inventory.ini` file is set up for `localhost` by default. If you want to run this on a remote machine, update the inventory accordingly.
3.  **Adjust variables**: Modify `src/vars/main.yml` to define your `garden_path`, `quarantine_path`, `stale_threshold_days`, and whether to `perform_quarantine`.
4.  **Run the playbook (check mode first)**:

    It's highly recommended to run in check mode first to see what actions would be taken without actually modifying your files:

    ```bash
    ansible-playbook -i src/inventory.ini src/weeder.yml --check
    ```

5.  **Review the report**: A report will be generated in your `quarantine_path` (e.g., `/tmp/digital_garden_quarantine/weeder_report_YYYYMMDDTHHMMSSZ.txt`). Examine its contents to understand which files are identified.

6.  **Run the playbook (with quarantine, if desired)**:

    If you are satisfied with the report and want to move the identified files to quarantine, set `perform_quarantine: true` in `src/vars/main.yml` and run:

    ```bash
    ansible-playbook -i src/inventory.ini src/weeder.yml
    ```

## Configuration (`src/vars/main.yml`)

*   `garden_path`: The absolute path to your digital garden or knowledge base directory. (e.g., `"/home/user/notes"`)
*   `quarantine_path`: The absolute path where identified files will be moved if `perform_quarantine` is `true`. (e.g., `"/home/user/notes_quarantine"`)
*   `stale_threshold_days`: The number of days after which a file is considered 'stale' if not modified. (e.g., `90`)
*   `perform_quarantine`: Set to `true` to enable moving files to the `quarantine_path`. Set to `false` (default) to only generate a report. (e.g., `true`)

## How "Unlinked" is Determined

A note is considered "unlinked" if its filename (without the `.md` extension) does not appear as a whole word within the content of any other markdown file in the garden. This is a heuristic and might not cover all linking conventions (e.g., complex graph databases or specific wiki-link syntaxes), but it's effective for simple markdown-based gardens.

## Example Report Output

```text
Digital Garden Weeder Report - 2023-10-27T10:30:00Z

Garden Path: /tmp/digital_garden
Quarantine Path: /tmp/digital_garden_quarantine
Stale Threshold: 30 days
Perform Quarantine: false

---
Total Markdown Files Found: 5

---
Stale Files (Modified over 30 days ago):
- /tmp/digital_garden/stale_linked_note.md (Last Modified: 2023-09-01 10:00:00)
- /tmp/digital_garden/stale_unlinked_note.md (Last Modified: 2023-09-05 14:30:00)

---
Unlinked Files (Not referenced by other notes):
- /tmp/digital_garden/stale_unlinked_note.md
- /tmp/digital_garden/fresh_unlinked_note.md

---
Quarantine Candidates (Stale AND Unlinked):
- /tmp/digital_garden/stale_unlinked_note.md

---
Action Taken:
Quarantine is disabled. No files were moved.
```
