# Nightly Digital Garden Keeper

This Ansible playbook helps maintain a collection of markdown files, often referred to as a "digital garden" or knowledge base. It automates several common maintenance tasks:

- **Tag Validation**: Identifies markdown files that are missing required YAML front matter tags or have empty tag fields.
- **Broken Link Detection**: Scans for internal markdown links (`[text](link.md)`) that point to non-existent local files.
- **Content Archiving**: Moves old markdown files (based on their modification time) into a designated archive directory.
- **Report Generation**: Creates a summary report of all findings.

## Usage

1.  **Define your inventory**: Ensure you have a `localhost` entry in your `inventory.ini` file, as this playbook runs locally.

    ```ini
    [localhost]
    localhost ansible_connection=local
    ```

2.  **Configure variables**: Adjust the `garden_path`, `archive_path`, `archive_after_days`, `required_tags_field`, and `required_date_field` in `src/vars/main.yml` or pass them as extra variables (`-e`).

    - `garden_path`: The root directory of your digital garden markdown files.
    - `archive_path`: The directory where old files will be moved.
    - `archive_after_days`: Files older than this many days will be archived.
    - `required_tags_field`: The YAML front matter field name expected for tags (e.g., `tags`).
    - `required_date_field`: The YAML front matter field name expected for the date (e.g., `date`).

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_keeper.yml
    ```

    After execution, a `digital_garden_report.md` will be generated in your `garden_path` detailing any issues found and actions taken.

## Example Front Matter

Your markdown files should ideally have YAML front matter like this:

```markdown
---
title: My Awesome Note
tags: [ansible, automation, garden]
date: 2023-10-27
---

This is the content of my note.

[Link to another note](another-note.md)
```

## Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
ansible-playbook -i tests/inventory.ini tests/test_garden_keeper.yml
```

This will set up a temporary test environment, run the `garden_keeper.yml` playbook against it, and assert the expected outcomes.
