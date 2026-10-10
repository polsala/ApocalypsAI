# Nightly Morale Booster Deployer

This Ansible playbook ensures that designated "morale-boosting" directories exist on your remote hosts and deploys a daily whimsical survival tip to a dated file within them. Keep spirits high even when the world is... well, you know.

## Features

*   **Directory Management**: Automatically creates `/opt/apocalypsai_morale` and `/opt/apocalypsai_morale/daily_tips` on target hosts.
*   **Whimsical Tips**: Selects a random, light-hearted survival tip from a predefined list.
*   **Daily Deployment**: Places the chosen tip into a date-stamped file (e.g., `2023-10-27.txt`) in the `daily_tips` directory.
*   **Idempotent**: Running the playbook multiple times will only make changes if directories don't exist or the tip for the current day hasn't been deployed yet.

## Prerequisites

*   **Ansible**: Version 2.10 or higher.
*   **Target Hosts**: SSH access to the hosts defined in your `src/inventory.ini` file.
*   **Privileges**: The Ansible user needs `become` (sudo) privileges on the target hosts to create directories in `/opt`.

## Usage

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-morale-booster-deployer
    ```

2.  **Configure your inventory**:
    Edit `src/inventory.ini` to list your target hosts.
    ```ini
    [apocalypsai_hosts]
    # Example:
    # server1.example.com
    # server2.example.com
    # Or for local testing:
    localhost ansible_connection=local
    ```

3.  **Customize morale tips (optional)**:
    Edit `src/vars/morale_tips.yml` to add or modify the whimsical survival tips.

4.  **Run the playbook**:
    Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_morale.yml --ask-become-pass
    ```
    (Remove `--ask-become-pass` if you have passwordless sudo configured for your Ansible user.)

    To run in check mode (dry run):
    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_morale.yml --check --ask-become-pass
    ```

## Automated Tests

Tests are written as an Ansible playbook that runs locally and verifies the expected behavior in both `check_mode` and actual execution (within a temporary directory). The random tip selection and date are mocked for deterministic results.

To run the tests:

1.  Ensure you have Ansible installed.
2.  Navigate to the utility's directory:
    ```bash
    cd ApocalypsAI/ansible-playbooks/nightly-morale-booster-deployer
    ```
3.  Execute the test playbook:
    ```bash
    ansible-playbook -i src/inventory.ini tests/test_deploy_morale.yml
    ```
    This will create a temporary directory (`/tmp/apocalypsai_morale_test`), simulate the playbook's actions, verify outcomes, and then clean up.
