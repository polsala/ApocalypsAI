# Nightly Digital Garden Front Matter Forager

This Ansible playbook helps maintain the pristine state of your digital garden or Markdown-based knowledge base by ensuring all `.md` files have a proper YAML front matter block. If a file is found without front matter, it will automatically prepend a basic block including a `title` derived from the filename and the current `date`. This is particularly useful for static site generators, personal wikis, or any system relying on structured metadata within Markdown files.

## Features

*   **Front Matter Enforcement**: Scans specified directories for Markdown files.
*   **Automatic Generation**: Adds a default YAML front matter (`title`, `date`) if missing.
*   **Idempotent**: Files with existing front matter are left untouched.
*   **Whimsical Naming**: Because even your digital weeds need a little love.

## Usage

### Prerequisites

*   Ansible installed (version 2.10 or higher recommended).
*   Access to the target machine(s) where your digital garden resides. For local use, `localhost` is sufficient.

### 1. Inventory File (`src/inventory.ini`)

Define the hosts where your digital garden is located. For local execution, `localhost` is fine.

```ini
[garden_hosts]
localhost ansible_connection=local
```

### 2. Playbook Variables (`src/forage_front_matter.yml`)

The playbook expects a `garden_path` variable, which is the root directory of your Markdown files. You can pass it via the command line or define it in a `vars` file.

```yaml
# src/forage_front_matter.yml
---
- name: Ensure digital garden Markdown files have front matter
  hosts: garden_hosts
  gather_facts: yes

  vars:
    garden_path: "{{ playbook_dir }}/my_garden" # Default path, override as needed

  tasks:
    # ... (tasks will go here)
```

### 3. Running the Playbook

To run the playbook, navigate to the utility's directory and execute:

```bash
ansible-playbook -i src/inventory.ini src/forage_front_matter.yml --extra-vars "garden_path=/path/to/your/actual/garden"
```

Replace `/path/to/your/actual/garden` with the real path to your Markdown files.

**Dry Run (Check Mode)**:
It's always a good idea to run in check mode first to see what changes would be made:

```bash
ansible-playbook -i src/inventory.ini src/forage_front_matter.yml --extra-vars "garden_path=/path/to/your/actual/garden" --check
```

## Example Output (when changes are made)

```
PLAY [Ensure digital garden Markdown files have front matter] *******************

TASK [Find Markdown files in /tmp/my_garden] ***********************************
ok: [localhost]

TASK [Process each Markdown file] **********************************************
TASK [Read file content: /tmp/my_garden/new_note.md] ***************************
ok: [localhost]

TASK [Check for existing front matter for /tmp/my_garden/new_note.md] **********
ok: [localhost]

TASK [Set facts for new front matter: /tmp/my_garden/new_note.md] **************
ok: [localhost]

TASK [Add front matter to /tmp/my_garden/new_note.md] **************************
changed: [localhost]

TASK [Read file content: /tmp/my_garden/existing_note.md] **********************
ok: [localhost]

TASK [Check for existing front matter for /tmp/my_garden/existing_note.md] *****
ok: [localhost]

TASK [Set facts for new front matter: /tmp/my_garden/existing_note.md] *********
skipping: [localhost]

TASK [Add front matter to /tmp/my_garden/existing_note.md] *********************
skipping: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

## Development and Testing

The `tests/` directory contains a Molecule-like test playbook that sets up a temporary environment, runs the main playbook, and asserts the outcomes.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_forage_front_matter.yml
```

This will:
1.  Create a temporary directory.
2.  Populate it with test Markdown files (some with, some without front matter).
3.  Execute the `forage_front_matter.yml` playbook against this temporary directory.
4.  Verify that files without front matter were updated and files with front matter were untouched.
5.  Clean up the temporary directory.
