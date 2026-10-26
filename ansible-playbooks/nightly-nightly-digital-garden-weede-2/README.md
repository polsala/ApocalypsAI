# Nightly Digital Garden Weeder

This Ansible playbook helps maintain a tidy "digital garden" or personal knowledge base by identifying and "weeding" stale markdown notes. Notes that haven't been modified within a configurable number of days are moved to a designated "compost bin" directory, allowing you to review them later or simply keep your active garden fresh.

## Features

*   **Stale Note Detection**: Identifies `.md` files that haven't been touched in a while.
*   **Automated Weeding**: Moves stale notes to a specified "compost bin" directory.
*   **Configurable**: Easily adjust the garden path, stale threshold, and compost bin location.
*   **Idempotent**: Running the playbook multiple times will only move files once.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to the target machine(s) where your digital garden resides (or `ansible_connection=local` for local execution).
*   Python 3 on the target machine(s) (for Ansible's modules).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) that lists the hosts where your digital garden is located.

    ```ini
    [garden_hosts]
    your_garden_server ansible_host=your.server.ip.or.hostname
    # Or for local execution:
    # localhost ansible_connection=local
    ```

2.  **Configure variables**:
    Edit `src/vars/main.yml` to set your `garden_path`, `stale_days`, and `compost_path`.

    ```yaml
    # src/vars/main.yml
    garden_path: "/home/user/my_digital_garden"
    stale_days: 90 # Files not modified in the last 90 days are considered stale
    compost_path: "/home/user/my_digital_garden_compost"
    ```

3.  **Run the playbook**:
    Execute the `weeder.yml` playbook, specifying your inventory.

    ```bash
    ansible-playbook -i inventory.ini src/weeder.yml
    ```

    The playbook will report which files, if any, were moved to the compost bin.

## Example Output

```
PLAY [Weed the Digital Garden] *************************************************

TASK [Gathering Facts] *********************************************************
ok: [your_garden_server]

TASK [Ensure compost bin exists] ***********************************************
ok: [your_garden_server]

TASK [Find stale markdown files] ***********************************************
ok: [your_garden_server]

TASK [Move stale files to compost bin] *****************************************
changed: [your_garden_server] => (item={'path': '/home/user/my_digital_garden/old_idea.md', 'mtime': 1672531200.0})

TASK [Report on weeded files] **************************************************
ok: [your_garden_server] => {
    "msg": "Weeded 1 file(s) from the digital garden: ['/home/user/my_digital_garden/old_idea.md']"
}

PLAY RECAP *********************************************************************
your_garden_server         : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Development & Testing

The `tests/` directory contains a setup for local testing using `ansible-playbook` itself. This allows for deterministic, offline testing of the playbook's logic.

1.  **Setup test environment**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_setup.yml
    ```
    This creates dummy garden and compost directories with recent and stale files in `/tmp/test_digital_garden` and `/tmp/test_digital_garden_compost`.

2.  **Run the main weeder playbook against the test environment**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini src/weeder.yml -e "garden_path=/tmp/test_digital_garden compost_path=/tmp/test_digital_garden_compost"
    ```
    Note: The `-e` flags override the `vars/main.yml` paths to point to the test directories.

3.  **Verify the results**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_weeder.yml
    ```
    This playbook asserts that the correct files were moved and others remained.

4.  **Clean up test environment**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_cleanup.yml
    ```
