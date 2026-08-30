# Nightly Ansible Digital Garden

## Overview

In the post-apocalyptic digital landscape, even servers need a little tender loving care. The `nightly-ansible-digital-garden` is a whimsical-yet-useful Ansible playbook designed to keep your systems tidy, much like a diligent gardener tending to their digital plots. It "prunes" old temporary files, "weeds" out stale caches, and "composts" old logs, ensuring your systems remain healthy and efficient.

After its work, it generates a charming "Digital Garden Report" summarizing its efforts.

## Features

*   **Prune Old Files**: Deletes files older than a configurable age in specified temporary directories.
*   **Weed Out Caches**: Clears user cache directories to free up space.
*   **Compost Old Logs**: Manages log files, optionally deleting or archiving them based on age.
*   **Digital Garden Report**: Generates a summary of the gardening activities.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access (or local connection) to the target hosts.

2.  **Clone the repository (or copy this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-ansible-digital-garden
    ```

3.  **Configure your inventory**: 
    Edit `src/inventory.ini` to list your target hosts. For local execution, the default `[local]` group is sufficient.

    ```ini
    # src/inventory.ini
    [local]
    localhost ansible_connection=local

    [servers]
    server1.example.com
    server2.example.com
    ```

4.  **Customize variables (optional)**:
    Review and modify `src/vars/main.yml` to adjust the pruning age, target paths, and log composting behavior.

    ```yaml
    # src/vars/main.yml
    garden_prune_age_days: 7
    garden_log_age_days: 30
    garden_paths_to_prune:
      - "/tmp"
      - "~/.cache"
    garden_log_paths_to_compost:
      - "/var/log"
    garden_report_path: "/tmp/digital_garden_report.txt"
    ```

5.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/digital_garden.yml
    ```

    After execution, check the `garden_report_path` (default: `/tmp/digital_garden_report.txt`) on your target host for the summary.

## Example Digital Garden Report

```
Digital Garden Report for server.example.com
Date: 2023-10-27

--- Pruning Summary ---
Paths targeted for pruning (files older than 7 days):
  - /tmp
  - ~/.cache

--- Composting Summary ---
Paths targeted for composting (logs older than 30 days):
  - /var/log

--- Overall Status ---
Your digital garden is looking spick and span!
```

## Testing

To run the self-contained tests for this playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_digital_garden.yml
```

The tests will create temporary files, run the cleanup playbook, and then verify that the old files have been removed and the report generated. They are designed to be deterministic and run offline.
