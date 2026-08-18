# Nightly Garden Bloom Orchestrator

This Ansible playbook helps you maintain a thriving digital garden or knowledge base by automating the identification of stale content, highlighting recently updated "blooming" notes, and generating a concise daily report. It's designed for markdown-based knowledge systems where files are stored on a server or local machine.

## Features

*   **Stale Note Detection**: Identifies markdown files that haven't been modified for a configurable period, suggesting they might need pruning or revisiting.
*   **Blooming Content Highlight**: Lists notes that have been recently created or updated, giving you an overview of your garden's current growth.
*   **Daily Bloom Report**: Generates a markdown report summarizing the findings, making it easy to integrate into your daily workflow or dashboard.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   Access (SSH or local) to the target machine where your digital garden resides.

2.  **Inventory Setup**:
    Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) that points to your digital garden host(s).

    ```ini
    [garden_hosts]
    localhost ansible_connection=local # For local digital gardens
    # my_server.example.com            # For remote digital gardens
    ```

3.  **Configuration**:
    Edit `src/vars/main.yml` to define your digital garden's path and thresholds:

    ```yaml
    ---
    garden_path: "/path/to/your/digital/garden" # e.g., /home/user/notes or /var/www/garden
    stale_threshold_days: 90                   # Days after which a note is considered stale
    bloom_threshold_days: 7                    # Days for a note to be considered 'blooming'
    report_output_path: "/tmp/bloom_report.md" # Path to save the generated report
    ```

4.  **Run the Playbook**:
    Execute the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i src/inventory.ini src/bloom_orchestrator.yml
    ```

    After execution, check the `report_output_path` (e.g., `/tmp/garden_bloom_report.md`) for your daily bloom report.

## Automated Tests

The utility includes a comprehensive test suite to ensure its functionality.

1.  **Install Ansible**: If you haven't already, install Ansible.
2.  **Navigate to the utility directory**: `cd ansible-playbooks/nightly-garden-bloom-orchestrator`
3.  **Run the test playbook**:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_playbook.yml
    ```

    This will:
    *   Set up a temporary digital garden with dummy markdown files.
    *   Run the `bloom_orchestrator.yml` playbook against this temporary garden.
    *   Assert that the generated report contains the expected content based on the dummy files.
    *   Clean up the temporary environment.

    The tests are designed to be deterministic and run offline, creating and verifying local file system changes.
