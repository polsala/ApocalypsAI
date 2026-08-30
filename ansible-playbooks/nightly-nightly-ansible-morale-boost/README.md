# Nightly Ansible Morale Booster

This Ansible playbook is designed to uplift spirits and maintain community morale by distributing and activating whimsical, yet essential, content across designated nodes. In the face of existential threats, a steady supply of inspirational quotes, comforting affirmations, or even silly sounds can be crucial.

## Features

*   **Content Distribution**: Copies text files (quotes, affirmations) and optional media files to target hosts.
*   **Automated Display**: Sets up a cron job to periodically display a random piece of content (e.g., to `/etc/motd` or a custom log file).
*   **Customizable**: Easily extendable with different content types and display mechanisms.

## Usage

1.  **Prepare your Inventory**:
    Create an `inventory.ini` file listing your target hosts. For example:
    ```ini
    [community_nodes]
    node1.example.com
    node2.example.com
    ```

2.  **Define Morale Content**:
    Place your `quotes.txt` and `affirmations.txt` (or other text files) in the `src/files/` directory. Each line should be a separate piece of content.

3.  **Run the Playbook**:
    ```bash
    ansible-playbook -i inventory.ini src/morale_booster.yml
    ```

    To run with specific variables (e.g., a different content directory or cron schedule):
    ```bash
    ansible-playbook -i inventory.ini src/morale_booster.yml -e "morale_content_dir=/opt/morale cron_schedule='*/5 * * * *'"
    ```

## Configuration Variables

You can override these variables in `vars/main.yml`, via `--extra-vars (-e)`, or in your inventory:

*   `morale_content_dir`: Path on target hosts where morale content will be stored. Default: `/opt/apocalypsai_morale`
*   `morale_display_script_path`: Path for the script that displays content. Default: `/usr/local/bin/display_morale.sh`
*   `cron_schedule`: Cron schedule for the display script. Default: `0 */6 * * *` (every 6 hours)
*   `motd_path`: Path to the Message of the Day file. Default: `/etc/motd` (Note: requires root privileges to write to `/etc/motd`)

## Example Content (`src/files/quotes.txt`)

```
"Even in the darkest void, a single spark of hope can ignite a galaxy."
"The future is not written, it is built, one act of kindness at a time."
"Remember, even a broken clock is right twice a day. Keep ticking!"
```

## Example Content (`src/files/affirmations.txt`)

```
"I am resilient. I adapt. I overcome."
"My spirit is a beacon, even in the gloom."
"Today, I choose joy, even if it's just for a moment."
```
