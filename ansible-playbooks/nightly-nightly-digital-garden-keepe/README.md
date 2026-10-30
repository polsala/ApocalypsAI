# Nightly Digital Garden Keeper

This Ansible playbook helps maintain the health and organization of your "digital garden" – a collection of markdown notes, thoughts, and knowledge base entries. It performs regular backups, audits notes for specific tags, identifies stale content, and generates a comprehensive report.

## Features

*   **Automated Backups**: Creates timestamped archives of your digital garden.
*   **Tag Auditing**: Checks for the presence of user-defined tags (e.g., `#todo`, `#review`) within your markdown files.
*   **Stale Content Detection**: Identifies notes that haven't been modified in a configurable number of days, helping you prune or refresh forgotten knowledge.
*   **Health Report**: Generates a detailed markdown report summarizing backup status, tagged files, and stale notes.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Access to the target host(s) where your digital garden resides.

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) that lists the hosts where your digital garden is located.

    ```ini
    [garden_hosts]
    your_server_ip ansible_user=your_user
    ```

2.  **Configure variables**:
    Edit `src/vars/main.yml` to set the `garden_path`, `backup_path`, `stale_days_threshold`, and `required_tags`.

    ```yaml
    # src/vars/main.yml
    garden_path: "/home/your_user/digital_garden"
    backup_path: "/home/your_user/digital_garden_backups"
    stale_days_threshold: 90 # Mark notes as stale if not modified in 90 days
    required_tags:
      - "#todo"
      - "#review"
    ```

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_keeper.yml
    ```

    After execution, a report will be generated at `{{ backup_path }}/garden_report_YYYYMMDD_HHMMSS.md` on the target host.

## Testing

This utility includes a self-contained test playbook that simulates a digital garden environment and verifies the playbook's functionality.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_garden_keeper.yml
```

The tests will:
1.  Create a temporary digital garden structure.
2.  Execute `garden_keeper.yml` against this temporary structure.
3.  Verify that backups are created and the report contains expected content regarding stale and tagged files.
4.  Clean up the temporary test environment.

## Example Report Output

```markdown
# Digital Garden Health Report (Generated: YYYY-MM-DD HH:MM:SS)

## Backup Status
*   **Last Backup**: /path/to/digital_garden_backups/digital_garden_YYYYMMDD_HHMMSS.tar.gz
*   **Status**: Backup successful.

## Stale Notes (Not modified in 90 days)
*   /home/your_user/digital_garden/old_idea.md (Last Modified: YYYY-MM-DD)
*   /home/your_user/digital_garden/forgotten_draft.md (Last Modified: YYYY-MM-DD)

## Notes with Required Tags
### Tag: #todo
*   /home/your_user/digital_garden/project_plan.md
*   /home/your_user/digital_garden/next_steps.md

### Tag: #review
*   /home/your_user/digital_garden/draft_article.md
```
