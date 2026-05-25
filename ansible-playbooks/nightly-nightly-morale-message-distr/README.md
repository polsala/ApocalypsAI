# Nightly Morale Message Distributor

## Summary
This Ansible playbook automates the distribution of whimsical, morale-boosting messages or crucial survival tips to various 'outpost terminals' (remote servers) within your post-apocalyptic network. Keep spirits high and information flowing, even when the world is upside down!

## How it Works
1.  **Message Selection**: The playbook loads a predefined list of messages from `vars/messages.yml`. For daily operations, it randomly selects one message.
2.  **Templating**: The selected message is rendered into a `message_of_the_day.j2` template.
3.  **Distribution**: The rendered message file is then copied to a specified target path on all designated 'outpost' hosts in your inventory.

## Prerequisites
*   **Ansible**: Ensure Ansible is installed on your control machine.
*   **Python**: Python 3.x is required on both the control machine and target hosts.
*   **SSH Access**: Passwordless SSH access (e.g., via SSH keys) from your control machine to all target hosts is recommended.

## Usage
1.  **Define your Outposts**: Edit `src/inventory.ini` to list your target servers under the `[outposts]` group.
    ```ini
    [outposts]
    terminal1.example.com
    terminal2.example.com
    # Add more hosts as needed
    ```
2.  **Customize Messages**: Modify `src/vars/messages.yml` to add, remove, or change the morale-boosting messages.
    ```yaml
    # src/vars/messages.yml
    messages:
      - "Remember, even in the darkest void, a single spark of hope can ignite a bonfire!"
      - "Today's survival tip: Always check your boots for scorpions before putting them on. You're welcome."
      - "A laugh a day keeps the existential dread away. Or at least distracts it for a bit."
      - "Did you know? The average human can survive three weeks without food, but only three days without a good meme. Prioritize accordingly."
    ```
3.  **Run the Playbook**: Execute the playbook from your control machine.
    ```bash
    ansible-playbook -i src/inventory.ini src/distribute_message.yml
    ```
    This will connect to all hosts in the `[outposts]` group, select a random message, and place it at `/etc/motd` (or your configured `motd_path`).

## Configuration
*   `src/inventory.ini`: Defines the target hosts.
*   `src/vars/messages.yml`: Contains the list of messages to be distributed.
*   `src/distribute_message.yml`: The main playbook, where you can adjust the `motd_path` variable if `/etc/motd` is not suitable for your terminals.

## Example Output (on a target terminal)
After the playbook runs, if you SSH into a `terminal1.example.com` and `cat /etc/motd` (assuming default `motd_path`):

```
Welcome, survivor!

Remember, even in the darkest void, a single spark of hope can ignite a bonfire!

Stay vigilant!
```
