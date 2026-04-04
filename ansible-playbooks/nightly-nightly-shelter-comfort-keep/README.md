# Nightly Shelter Comfort Keeper

## Overview

The `nightly-shelter-comfort-keeper` is an Ansible playbook designed to automate the daily inspection and light maintenance of a survivor's shelter. In the post-apocalyptic world, consistent comfort and operational amenities are crucial for morale and survival. This playbook ensures that your whimsical yet vital shelter systems are in tip-top shape.

It checks on:
*   **Solar Shimmer Panels**: Ensures they are clean and generating power.
*   **Aqua-Purifier Gurgle-Filter**: Verifies the water purification system is clear and functional.
*   **Glow-Moss Luminescence Array**: Confirms the bioluminescent lighting is adequately bright.
*   **Automated Nosh Nook**: Checks the stock level of the essential snack dispenser.
*   **Whisper-Wind Chimes**: Inspects the perimeter security chimes for tangles or dislodgement.

If any issues are detected, it will report them and, where possible, suggest or perform minor corrective actions.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Python 3 on the control node and target hosts
*   SSH access to target hosts (if not running locally)

## Usage

1.  **Define your inventory**: Edit `inventory.ini` to list your shelter hosts. For local testing, `localhost` is pre-configured.

    ```ini
    [shelters]
    localhost ansible_connection=local
    # my_shelter_alpha ansible_host=192.168.1.10 ansible_user=survivor
    # my_shelter_beta ansible_host=192.168.1.11 ansible_user=survivor
    ```

2.  **Run the playbook**:

    ```bash
    ansible-playbook -i inventory.ini playbook.yml
    ```

    To perform a dry run without making any changes:

    ```bash
    ansible-playbook -i inventory.ini playbook.yml --check
    ```

    The playbook will output a summary report to the console and also save a detailed `comfort_report.txt` in the current directory.

## Playbook Structure

*   `inventory.ini`: Defines the hosts to manage.
*   `playbook.yml`: The main playbook orchestrating all checks.
*   `tasks/`: Contains modular task files for each system check.
    *   `check_power.yml`
    *   `check_water.yml`
    *   `check_lighting.yml`
    *   `check_snacks.yml`
    *   `check_security.yml`
*   `templates/comfort_report.j2`: Jinja2 template for generating the final report.
*   `tests/test_playbook.yml`: Automated tests for the playbook logic.

## Extending and Customizing

You can easily add more checks by creating new task files in the `tasks/` directory and including them in `playbook.yml`. Adjust thresholds and desired states within the task files as needed.
