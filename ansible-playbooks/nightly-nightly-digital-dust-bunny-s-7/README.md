# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your servers tidy by identifying and optionally cleaning up old, forgotten files and directories – what we affectionately call "digital dust bunnies." It's designed to be run periodically to maintain system hygiene and reclaim disk space.

## Features

*   **Configurable Paths**: Specify which directories to scan.
*   **Age Thresholds**: Define how old files/directories must be to be considered "dust bunnies."
*   **Exclusion Patterns**: Ignore specific files or directories.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Detailed Reporting**: Generate a summary of identified and cleaned items.

## Usage

1.  **Inventory**: Prepare your Ansible inventory (`inventory.ini`) with the hosts you want to sweep.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Configuration**: Review and adjust the variables in `vars/main.yml`.

    ```yaml
    ---
    # vars/main.yml
    dust_bunny_paths:
      - /var/log
      - /tmp
      - /opt/old_backups
      - /home/*/.cache
    
    dust_bunny_age_days: 30 # Files/dirs older than this will be considered
    
    dust_bunny_exclude_patterns:
      - "*.conf"
      - "important_data"
    
    dust_bunny_dry_run: true # Set to 'false' to actually remove files
    
    dust_bunny_report_path: "/tmp/dust_bunny_report_{{ ansible_hostname }}.txt"
    ```

3.  **Run in Dry Run Mode (Recommended First!)**:
    This will only report what *would* be cleaned without making any changes.

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dust_bunny_dry_run=true"
    ```

    After running, check the generated reports on each host (e.g., `/tmp/dust_bunny_report_web1.example.com.txt`).

4.  **Run for Cleanup**:
    Once you are confident with the dry run report, set `dust_bunny_dry_run` to `false` (either in `vars/main.yml` or via `-e` flag) to perform the actual cleanup.

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dust_bunny_dry_run=false"
    ```

## Playbook Structure

*   `dust_bunny_sweeper.yml`: The main playbook.
*   `inventory.ini`: Example inventory file.
*   `vars/main.yml`: Customizable variables for paths, age, exclusions, and dry run mode.
*   `templates/report.j2`: Jinja2 template for generating cleanup reports.
*   `tests/test_dust_bunny_sweeper.yml`: Molecule-style test playbook for local validation.

## Requirements

*   Ansible (core)
*   Python `jmespath` (for `json_query` filter, often included with Ansible)

## Contributing

Feel free to suggest improvements or new features!
