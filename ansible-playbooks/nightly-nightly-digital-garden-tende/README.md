# Nightly Digital Garden Tender

This Ansible playbook acts as a diligent digital gardener, ensuring your markdown-based knowledge base (or "digital garden") remains healthy, organized, and free of neglect. It checks for essential front matter, identifies broken internal links, and gently reminds you about "wilting" (stale) content.

## Features

*   **Front Matter Validation**: Ensures all markdown files have required YAML front matter keys (e.g., `title`, `date`, `tags`).
*   **Broken Link Detection**: Scans for internal `[text](link.md)` style links and verifies if the target markdown files exist within the garden.
*   **Stale Content Identification**: Flags notes that haven't been modified recently, suggesting they might need a refresh or review.

## Prerequisites

*   Ansible (version 2.10 or higher recommended)
*   Access to the target machine(s) where your digital garden resides (local or remote).

## Setup

1.  **Inventory**: Create an `inventory.ini` file (or use an existing one) that lists the hosts where your digital garden is located. For a local garden, `localhost` with `ansible_connection=local` is sufficient.

    ```ini
    [garden_servers]
    localhost ansible_connection=local
    # For remote gardens, add your server details:
    # my_garden_server ansible_host=192.168.1.100 ansible_user=your_user
    ```

2.  **Configuration**: Review and optionally modify `src/vars/garden_config.yml` to define your garden's path, required front matter keys, and the threshold for considering content stale.

    ```yaml
    ---
    garden_path: "/path/to/your/digital/garden" # IMPORTANT: Change this to your actual garden path
    required_frontmatter_keys:
      - "title"
      - "date"
      - "tags"
    stale_days_threshold: 90 # Number of days after which a note is considered stale if not modified
    ```

## Usage

To run the digital garden tender, execute the playbook with your inventory:

```bash
ansible-playbook -i inventory.ini src/garden_tender.yml
```

The playbook will output warnings and suggestions directly to your console. It does not modify any files; it only reports on the state of your garden.

## Example Output

```
PLAY [Tend to the Digital Garden] **********************************************

TASK [Ensure digital garden path exists] ***************************************
ok: [localhost]

TASK [Find all markdown notes] *************************************************
ok: [localhost]

...

TASK [Report files missing front matter] ***************************************
[0;33m[WARNING]: File '/tmp/my_digital_garden/missing_frontmatter.md' is missing YAML front matter.[0m
ok: [localhost] => (item=/tmp/my_digital_garden/missing_frontmatter.md)

TASK [Report files missing required front matter keys] *************************
[0;33m[WARNING]: File '/tmp/my_digital_garden/missing_tags.md' is missing required front matter keys: tags.[0m
ok: [localhost] => (item={'file': '/tmp/my_digital_garden/missing_tags.md', 'missing_keys': ['tags']})

TASK [Report broken internal links] ********************************************
[0;33m[WARNING]: File '/tmp/my_digital_garden/broken_link_note.md' contains a broken link to 'non_existent_target.md'.[0m
ok: [localhost] => (item={'source_file': '/tmp/my_digital_garden/broken_link_note.md', 'link': 'non_existent_target.md', 'target_exists': False})

TASK [Report stale files] ******************************************************
[0;33m[WARNING]: File '/tmp/my_digital_garden/old_idea.md' hasn't been modified in 90 days. Perhaps it needs watering?[0m
ok: [localhost] => (item=/tmp/my_digital_garden/old_idea.md)

PLAY RECAP *********************************************************************
localhost                  : ok=12   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
