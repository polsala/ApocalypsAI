# Nightly Server Serenity Setter

This Ansible playbook is designed to bring a touch of calm and order to your servers in the post-apocalyptic digital landscape. It performs two main tasks:

1.  **Sets a Whimsical Message Of The Day (MOTD)**: A random, calming message is selected from a predefined list and set as the server's MOTD, offering a moment of digital zen to anyone logging in.
2.  **Cleans Up Old Temporary Files**: It tidies up the `/tmp` directory by removing files older than one day, ensuring digital clutter doesn't accumulate and promoting a sense of system hygiene.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `localhost` for local execution).
*   `become` (sudo/root) privileges on the target servers for updating `/etc/motd` and cleaning `/tmp`.

### Running the Playbook

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) listing your target servers. For example:

    ```ini
    [servers]
    your_server_ip_or_hostname
    another_server_ip_or_hostname

    [all:vars]
    ansible_user=your_ssh_user
    # ansible_ssh_private_key_file=~/.ssh/id_rsa # Uncomment if using a specific key
    ```

    For local execution, you can use:

    ```ini
    [servers]
    localhost ansible_connection=local
    ```

2.  **Execute the playbook**:
    Navigate to the utility's root directory and run:

    ```bash
    ansible-playbook -i src/inventory.ini src/main_playbook.yml --ask-become-pass
    ```
    (Remove `--ask-become-pass` if you have passwordless sudo configured).

### Customization

*   **Serenity Messages**: You can modify the `src/vars/serenity_messages.yml` file to add, remove, or change the calming messages displayed in the MOTD.
*   **MOTD Path**: By default, the MOTD is written to `/etc/motd`. If you need to change this (e.g., for testing or specific system configurations), you can override the `motd_dest_path` variable when running the playbook:
    ```bash
    ansible-playbook -i src/inventory.ini src/main_playbook.yml -e "motd_dest_path=/path/to/custom/motd" --ask-become-pass
    ```

## Testing

The utility includes a self-contained test playbook that can be run locally.

### Running Tests

1.  **Ensure Ansible is installed.**
2.  **Navigate to the utility's root directory.**
3.  **Execute the test playbook**:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_serenity_setter.yml --ask-become-pass
    ```

    This test playbook will:
    *   Create dummy MOTD and temporary files.
    *   Run the core serenity-setting tasks, redirecting output to the dummy files.
    *   Assert that the dummy MOTD contains a valid serenity message and the expected footer.
    *   Assert that the dummy temporary file (marked as old) has been removed.
    *   Clean up all dummy files.

    The tests are designed to be deterministic and run offline (using `localhost` connection) by mocking file system interactions with temporary files.
