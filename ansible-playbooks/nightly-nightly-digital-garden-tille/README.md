# Nightly Digital Garden Tiller

## Summary
An Ansible playbook designed to cultivate a 'digital garden' on remote hosts. It ensures a base directory exists, creates specified markdown 'garden plot' files if they don't exist, and updates a 'daily wisdom' message file with a new thought or quote.

## Whimsical Purpose
In the ever-shifting digital landscape of the apocalypse, maintaining a serene and organized space for your thoughts, notes, and inspirations is crucial. The Digital Garden Tiller helps you keep your intellectual plots well-tended, ensuring your seeds of wisdom can always find fertile ground.

## Useful Purpose
This playbook is a practical example of using Ansible for idempotent content management. It can be adapted to:
- Ensure critical configuration files or documentation templates exist across a fleet of servers.
- Deploy daily messages, announcements, or motivational quotes to user login screens or internal dashboards.
- Maintain a consistent directory structure and initial file content for new projects or user environments.

## Prerequisites
- Ansible installed on your control machine.
- SSH access to your target hosts (if not running locally).

## Usage
1.  **Define your inventory**: Create or update `src/inventory.ini` with your target hosts.
    ```ini
    [garden_hosts]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```
2.  **Configure your garden**: Edit `src/vars/garden_config.yml` to specify the base path for your garden, the markdown files (garden plots) you want to maintain, and the list of wisdom messages.
3.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/tiller_playbook.yml
    ```

## Configuration (`src/vars/garden_config.yml`)
-   `garden_base_path`: The absolute path where your digital garden will reside (e.g., `/home/user/my_garden`).
-   `garden_plots`: A list of relative paths for markdown files that should exist within `garden_base_path` (e.g., `ideas/brainstorm.md`).
-   `daily_wisdom_file`: The name of the file that will contain the daily wisdom message.
-   `wisdom_messages`: A list of strings, each representing a wisdom message. The playbook will deterministically pick the first one for consistency.

## Example `src/vars/garden_config.yml`
```yaml
---
garden_base_path: "/tmp/digital_garden"
garden_plots:
  - "ideas/brainstorm.md"
  - "notes/daily_log.md"
  - "reflections/future_self.md"
daily_wisdom_file: "wisdom_of_the_day.md"
wisdom_messages:
  - "Even in the digital wasteland, a thought can bloom."
  - "Cultivate your ideas, for they are the seeds of tomorrow's solutions."
  - "The byte you plant today may grow into a forest of knowledge."
  - "A well-tended digital garden yields bountiful insights."
```

## Testing
To run the automated tests, execute the test playbook:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_tiller_playbook.yml
```
This will create a temporary digital garden at `/tmp/digital_garden` (or the path specified in `garden_config.yml`), run the cultivation tasks, and then verify the existence and content of the expected files before cleaning up.
