# Nightly Lore Ledger

An Ansible playbook to audit and standardize markdown files in a digital lore ledger, ensuring consistent metadata and structure.

## Overview

The `nightly-lore-ledger` utility helps maintain consistency across your collection of markdown-based "lore" or knowledge base entries. It scans a specified directory for `.md` files, extracts their YAML front matter, and checks if all `required_front_matter` fields (e.g., `title`, `tags`, `category`, `status`) are present. It then generates a comprehensive audit report.

This ensures your digital archives are always ready for quick retrieval, even when the world outside is in chaos.

## Usage

### Prerequisites

-   Ansible installed (version 2.10 or higher recommended).
-   Markdown files with optional YAML front matter (delimited by `---`).

### Running the Playbook

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-lore-ledger
    ```

2.  **Define your lore ledger path and required fields:**
    Edit `src/vars/main.yml` to specify the `lore_ledger_path` (the directory containing your markdown files) and `required_front_matter` list.

    Example `src/vars/main.yml`:
    ```yaml
    lore_ledger_path: "/path/to/your/lore/collection" # Change this to your actual path
    required_front_matter:
      - title
      - tags
      - category
      - status
    ```

3.  **Execute the playbook:**
    ```bash
    ansible-playbook -i src/inventory.ini src/lore_ledger.yml
    ```

    This will scan the specified directory and generate an audit report named `lore_ledger_audit_report.txt` in the `lore_ledger_path`.

### Example Output (`lore_ledger_audit_report.txt`)

```
Lore Ledger Audit Report - 2023-10-27T10:30:00

Total files scanned: 3

File: /path/to/your/lore/collection/perfect_lore.md
  Status: OK
File: /path/to/your/lore/collection/incomplete_lore.md
  Status: MISSING_FIELDS
  Missing Fields: category, status
File: /path/to/your/lore/collection/untagged_note.md
  Status: MISSING_FIELDS
  Missing Fields: title, tags, category, status
```

## Development and Testing

### Running Tests

The tests use Ansible's `local` connection to create temporary markdown files, run the playbook against them, and then assert the content of the generated report.

```bash
ansible-playbook -i src/inventory.ini tests/test_lore_ledger.yml
```

**Mock rationale:** All tests are executed locally using `delegate_to: localhost` and `connection: local`. File operations (creation, reading, deletion) are performed on a temporary directory within the test environment. This ensures tests are deterministic, isolated, and do not require any external services or network access. The `slurp` and `template` modules operate on local files, and `assert` modules check the content of these local files.
