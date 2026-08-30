# Nightly Digital Garden Cultivator

This Ansible playbook helps you cultivate and maintain a whimsical "digital garden" on your remote servers. It ensures a dedicated directory exists, plants new "seeds" (small text files with a timestamp and a random whimsical quote) daily, and prunes older plants to keep your digital ecosystem tidy.

## Features

*   **Garden Creation**: Ensures the specified digital garden directory exists.
*   **Daily Planting**: Adds a new "plant" (a timestamped file with a unique ID and a whimsical quote) to the garden.
*   **Automatic Pruning**: Removes the oldest plants to maintain a healthy garden size, preventing digital overgrowth.
*   **Status Reporting**: Gathers facts about the current state of your digital garden.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `ansible_connection=local` for local testing).

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) that lists your target servers.

    ```ini
    [garden_hosts]
    server1.example.com
    server2.example.com
    localhost ansible_connection=local
    ```

2.  **Configure your garden**: Review and optionally modify `src/vars/garden_config.yml`.

    ```yaml
    # src/vars/garden_config.yml
    digital_garden_path: "/var/digital_garden"
    max_garden_plants: 7 # Keep up to 7 plants in the garden
    ```

3.  **Run the playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/cultivate_garden.yml
    ```

    To run it daily, you can add it to a cron job on your control machine:

    ```bash
    # Example cron entry (runs daily at 3:00 AM)
    0 3 * * * /usr/bin/ansible-playbook -i /path/to/your/inventory.ini /path/to/src/cultivate_garden.yml
    ```

## Playbook Structure

*   `src/cultivate_garden.yml`: The main playbook orchestrating garden operations.
*   `src/inventory.ini`: Example inventory file.
*   `src/templates/plant_seed.j2`: Jinja2 template for the content of each new digital plant.
*   `src/vars/garden_config.yml`: Variables to customize garden behavior.

## Example Output

```
PLAY [Cultivate Digital Garden] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Ensure digital garden directory exists] **********************************
changed: [localhost]

TASK [Find existing plants] ****************************************************
ok: [localhost]

TASK [Prune oldest plants if exceeding max_garden_plants] **********************
ok: [localhost]

TASK [Generate new plant content] **********************************************
ok: [localhost]

TASK [Plant a new seed] ********************************************************
changed: [localhost]

TASK [Report Digital Garden Status] ********************************************
ok: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```
