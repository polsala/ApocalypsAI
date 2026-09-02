# Nightly Digital Garden Weeder

## Summary
The `nightly-garden-weeder` is an Ansible playbook designed to help you maintain a tidy and consistent digital garden (a collection of Markdown notes, articles, or documentation). It audits your Markdown files to ensure they adhere to a specified YAML front matter structure, reporting on any files that are missing front matter or required fields.

## Whimsical Purpose
Even digital gardens need a little tending! This utility acts as your diligent garden gnome, ensuring every precious note has its proper label and metadata, preventing your knowledge base from becoming an overgrown, unsearchable jungle.

## How it Works
The playbook performs the following steps:
1.  **Scans**: It searches a specified directory for all `.md` files.
2.  **Parses Front Matter**: For each file, it attempts to identify and parse the YAML front matter (the block between `---` at the top of the file).
3.  **Validates Fields**: It checks if the parsed front matter contains all `required_front_matter_keys` defined in `vars/garden_config.yml`.
4.  **Reports**: It generates a summary report, indicating which files are well-tended and which need some "weeding" (i.e., are missing front matter or required fields).

## Usage

### Prerequisites
-   Ansible installed (version 2.9 or higher recommended).
-   Python `pyyaml` library installed on the control node (`pip install pyyaml`).
-   Ansible `community.general` collection installed (`ansible-galaxy collection install community.general`).

### 1. Configure your Garden
Edit `vars/garden_config.yml` to define the `garden_path` (the directory containing your Markdown files) and the `required_front_matter_keys`.

```yaml
# vars/garden_config.yml
garden_path: "/path/to/your/digital/garden" # e.g., "{{ playbook_dir }}/my_notes"
required_front_matter_keys:
  - title
  - date
  - tags
```

### 2. Prepare your Inventory
A simple `inventory.ini` is provided. This playbook is designed to run locally on your control machine.

```ini
# src/inventory.ini
[localhost]
localhost ansible_connection=local
```

### 3. Run the Weeder
Execute the playbook from the `src` directory:

```bash
ansible-playbook -i inventory.ini garden_weeder.yml
```

The playbook will output a summary of its findings to the console.

## Automated Tests

Tests are implemented using a separate Ansible playbook that sets up a temporary environment, runs the main playbook, and asserts its output.

### How to Run Tests
1.  Navigate to the `tests` directory.
2.  Ensure `pyyaml` is installed (`pip install pyyaml`).
3.  Ensure `community.general` collection is installed (`ansible-galaxy collection install community.general`).
4.  Run the test playbook:

    ```bash
    ansible-playbook -i test_inventory.ini test_garden_weeder.yml
    ```

The tests will:
-   Create a temporary directory.
-   Populate it with valid and invalid Markdown files.
-   Run `garden_weeder.yml` against this temporary garden.
-   Verify that the output correctly identifies the status of each file.
-   Clean up the temporary directory.

## Example Output (partial)

```
...
TASK [Report: Files needing weeding] *******************************************
ok: [localhost] => {
    "msg": "--- Digital Garden Weeding Report ---\n\nWell-tended files (1):\n  - /tmp/ansible_test_garden_XXXXXX/valid_note.md\n\nFiles needing weeding (2):\n  - /tmp/ansible_test_garden_XXXXXX/invalid_note_no_frontmatter.md (Missing front matter)\n  - /tmp/ansible_test_garden_XXXXXX/invalid_note_missing_tag.md (Missing keys: ['tags'])\n\nTotal files scanned: 3"
}
...
```
