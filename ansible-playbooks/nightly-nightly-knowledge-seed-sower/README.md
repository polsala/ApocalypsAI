# Nightly Knowledge Seed Sower

This Ansible playbook ensures that your digital garden or knowledge base is always fertile, by verifying the existence of essential directories and files, setting correct permissions, and populating new files with predefined template content. It's perfect for maintaining daily notes, project templates, or any structured file system for your thoughts and data.

## Features

-   **Directory Creation**: Ensures specified directories exist.
-   **File Creation from Templates**: Creates new files based on Jinja2 templates if they don't exist.
-   **Permission Management**: Sets appropriate file and directory permissions.
-   **Idempotent**: Can be run multiple times without unintended side effects.

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) that targets the host(s) where you want to manage your knowledge base. For local execution, you can use `localhost`.

    ```ini
    [knowledge_hosts]
    localhost ansible_connection=local
    ```

2.  **Configure variables**:
    Edit `src/vars/main.yml` to specify your `knowledge_base_root`, `directories_to_ensure`, and `files_to_seed`.

    ```yaml
    # src/vars/main.yml
    knowledge_base_root: "/home/user/my_knowledge_garden" # IMPORTANT: Adjust this for production!
    default_dir_mode: "0755"
    default_file_mode: "0644"

    directories_to_ensure:
      - path: "{{ knowledge_base_root }}/daily_notes"
      - path: "{{ knowledge_base_root }}/project_templates"
      - path: "{{ knowledge_base_root }}/ideas"

    files_to_seed:
      - path: "{{ knowledge_base_root }}/daily_notes/{{ ansible_date_time.date | default('YYYY-MM-DD') }}.md"
        template: "daily_note.j2"
        mode: "0600" # More restrictive for daily notes
      - path: "{{ knowledge_base_root }}/project_templates/new_project_readme.md"
        content: "# New Project Readme\n\n## Overview\n\n## Setup\n"
      - path: "{{ knowledge_base_root }}/.garden_config"
        content: "garden_version: 1.0\n"
        mode: "0600"
      - path: "{{ knowledge_base_root }}/empty_seed.txt" # Example of an empty file
    ```

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i inventory.ini src/seed_sower.yml
    ```

    To see what changes *would* be made without actually making them (dry-run):

    ```bash
    ansible-playbook -i inventory.ini src/seed_sower.yml --check
    ```

## Directory Structure

```
.
├── README.md
├── src/
│   ├── seed_sower.yml
│   ├── inventory.ini
│   ├── vars/
│   │   └── main.yml
│   └── templates/
│       └── daily_note.j2
└── tests/
    ├── test_seed_sower.yml
    └── inventory_test.ini
```

## Automated Tests

The tests ensure the playbook's syntax is valid, it behaves idempotently in check mode, and correctly creates files with the expected content and permissions in an isolated temporary directory.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_seed_sower.yml
```
