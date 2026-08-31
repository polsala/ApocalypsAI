# Nightly MOTD Morale Booster

An Ansible playbook to distribute whimsical apocalyptic wisdom to server login banners (MOTD) for daily morale boosts. In the grim darkness of the post-apocalyptic future, a little wisdom goes a long way to keep spirits high (or at least mildly amused) for your server administrators.

## Features

*   **Whimsical Wisdom**: Delivers a pre-defined message to `/etc/motd` on target servers.
*   **Daily Refresh**: Designed to be run periodically (e.g., via cron) to update the MOTD.
*   **Customizable Source**: Easily point to your own file containing the wisdom messages.
*   **Timestamped**: Includes a timestamp in the MOTD for freshness.

## Usage

1.  **Prepare your inventory**:
    Create an `inventory.ini` file listing your target servers.

    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11
    ```

2.  **Create your wisdom source file**:
    Create a file (e.g., `wisdom.txt`) containing the message you want to display. Each line can be a separate message, or it can be a single multi-line message. The playbook will read the entire content of this file.

    ```
    "Even in the darkest byte, there is a flicker of hope. Or at least, a well-commented config file."
    ```

3.  **Run the playbook**:
    Execute the playbook, specifying your inventory and the path to your wisdom source file.

    ```bash
    ansible-playbook -i inventory.ini src/motd_booster.yml --extra-vars "motd_wisdom_source_path=/path/to/your/wisdom.txt"
    ```

    For testing purposes, you can use the provided `tests/inventory_test.ini` (which targets `localhost`) and the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_motd_booster.yml
    ```

## Configuration

The playbook uses the following variables, which can be overridden via `--extra-vars` or in `src/vars/main.yml`:

*   `motd_wisdom_source_path`: The absolute path to the file containing the wisdom message on the Ansible control node.
*   `motd_target_path`: The path on the target server where the MOTD will be written (default: `/etc/motd`).

## Example MOTD Output

```
*******************************************************************************
* Nightly ApocalypsAI Wisdom                                                  *
*******************************************************************************

"Even in the darkest byte, there is a flicker of hope. Or at least, a well-commented config file."

Last updated: 2023-10-27 10:30:00 UTC
```
