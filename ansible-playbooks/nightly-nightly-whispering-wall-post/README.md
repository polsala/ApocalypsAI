# Nightly Whispering Wall Post-it Manager

This Ansible playbook, `nightly-whispering-wall-postit`, helps you inject a dose of whimsy and wisdom (or just plain weirdness) into your server environments. It manages and rotates 'post-it' style messages, ensuring a fresh, morale-boosting, or thought-provoking snippet greets users or is available in a designated file.

## Features

*   **Whimsical Message Rotation**: Selects a message from a predefined list based on the current date, ensuring a consistent message for the day across all targeted hosts.
*   **Idempotent Deployment**: Uses Ansible's `copy` module to ensure the message file is updated only when necessary.
*   **Customizable Messages**: Easily add or modify your collection of 'whispering wall' messages.
*   **Flexible Target**: Configure the path where the message will be deployed (e.g., `/etc/motd` for login banners, or a custom file).

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing the servers where you want to deploy these messages.

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

    For local testing, you can use:

    ```ini
    [local]
    localhost ansible_connection=local
    ```

2.  **Customize your messages**: Edit `vars/messages.yml` to add your own collection of whimsical messages.

    ```yaml
    whispering_wall_messages:
      - "Remember, even in the void, your Wi-Fi signal is strong. Probably."
      - "Today's forecast: 100% chance of existential dread, with scattered hope."
      - "Don't forget to hydrate! The future is thirsty work."
    ```

3.  **Run the playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/postit_manager.yml \
      --extra-vars "target_file=/etc/motd"
    ```

    Replace `src/inventory.ini` with your inventory file and `/etc/motd` with your desired target file path. If you omit `target_file`, it defaults to `/opt/whispering_wall/message.txt`.

    *Note: Running against `/etc/motd` usually requires root privileges, so you might need to add `--become` to your command.* 

    ```bash
    ansible-playbook -i src/inventory.ini src/postit_manager.yml \
      --extra-vars "target_file=/etc/motd" --become
    ```

## Testing

To run the automated tests for this utility, use the following command:

```bash
ansible-playbook -i src/inventory.ini tests/test_postit_manager.yml
```

The tests will run the playbook against `localhost` using a temporary file and assert that the content matches one of the expected messages.
