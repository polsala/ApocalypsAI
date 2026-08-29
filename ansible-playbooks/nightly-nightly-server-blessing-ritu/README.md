# Nightly Server Blessing Ritual

Bestow a whimsical, randomly generated blessing upon your servers! This Ansible playbook updates your server's Message Of The Day (MOTD) or logs a positive affirmation, bringing good vibes and a touch of magic to your infrastructure.

## Features

*   **Whimsical Blessings**: Choose from a predefined list of quirky, positive messages.
*   **MOTD Integration**: Optionally updates `/etc/motd.d/ansible-blessing` to greet users with a blessing upon login.
*   **Logging**: Logs the blessing for historical record or simple confirmation.
*   **Customizable**: Easily add your own blessings or modify the output format.

## Usage

1.  **Prepare your inventory**:
    Create an `inventory.ini` file listing your target servers.

    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11
    ```

2.  **Run the playbook**:
    Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i inventory.ini src/bless_server.yml
    ```

    You can also specify a different output path for the blessing:
    ```bash
    ansible-playbook -i inventory.ini src/bless_server.yml -e "blessing_output_path=/var/log/server_blessings.log"
    ```

3.  **Check the blessing**:
    Log in to your server or check the specified output path.

    Example MOTD output:
    ```
    *****************************************
    *   May your caches be warm and your    *
    *   latency be ever low.                *
    *****************************************
    ```

## Configuration

*   `src/vars/blessings.yml`: Edit this file to add, remove, or modify the list of blessings.
*   `src/templates/blessing.j2`: Customize the template used to format the blessing message.
*   `blessing_output_path` (default: `/etc/motd.d/ansible-blessing`): Override this variable to change where the blessing is written.

## Testing

To run the automated tests, ensure you have Ansible installed.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_bless_server.yml --connection=local
```

The tests will run the playbook against a local connection, mock the blessing selection to be deterministic, and verify that the blessing is written to a temporary file as expected.
