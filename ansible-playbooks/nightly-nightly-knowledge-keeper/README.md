# Nightly Knowledge Keeper

This Ansible playbook helps maintain consistency in your markdown-based knowledge base or digital garden by auditing files for proper YAML front matter. It identifies files that are missing front matter or specific required keys within their front matter, providing a report of non-compliant files.

## Features

- Scans specified directories for markdown files (`.md`).
- Checks if each markdown file contains a valid YAML front matter block.
- Validates the presence of user-defined required keys within the front matter.
- Reports non-compliant files and missing keys.

## Prerequisites

- Ansible installed (version 2.10 or higher recommended).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file. For local execution, you can use `localhost`:
    ```ini
    [local]
    localhost ansible_connection=local
    ```

2.  **Configure variables**:
    Edit `src/vars/main.yml` to specify the paths to your knowledge base directories and the keys you require in the front matter.

    ```yaml
    # src/vars/main.yml
    knowledge_base_paths:
      - /path/to/your/notes
      - /another/path/to/guides
    required_front_matter_keys:
      - title
      - date
      - tags
    ```
    You can also pass these as extra vars: `-e "knowledge_base_paths=['/tmp/kb']"`.

3.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

    The playbook will output a summary of compliant and non-compliant files.

## Example Output

```
PLAY [Audit Knowledge Base Markdown Files] *************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Find markdown files] *****************************************************
ok: [localhost]

TASK [Initialize audit results] ************************************************
ok: [localhost]

TASK [Process each markdown file] **********************************************
ok: [localhost] => (item={'path': '/tmp/knowledge_base_audit/compliant_note.md', ...})
ok: [localhost] => (item={'path': '/tmp/knowledge_base_audit/missing_key_note.md', ...})
ok: [localhost] => (item={'path': '/tmp/knowledge_base_audit/no_front_matter_note.md', ...})
ok: [localhost] => (item={'path': '/tmp/knowledge_base_audit/malformed_front_matter.md', ...})

TASK [Report non-compliant files] **********************************************
ok: [localhost] => {
    "msg": "--- Knowledge Base Audit Report ---\n\nCompliant Files: 1\n  - /tmp/knowledge_base_audit/compliant_note.md\n\nNon-Compliant Files: 3\n  - /tmp/knowledge_base_audit/missing_key_note.md (Missing keys: ['date'])\n  - /tmp/knowledge_base_audit/no_front_matter_note.md (Missing front matter)\n  - /tmp/knowledge_base_audit/malformed_front_matter.md (Missing keys: ['date', 'tags'])\n"
}

PLAY RECAP *********************************************************************
localhost                  : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Testing

The `tests/test_playbook.yml` file creates temporary markdown files with various front matter conditions and then runs the main playbook against them, asserting the correctness of the generated audit report. This test is designed to be deterministic and run offline using `ansible_connection=local`.
