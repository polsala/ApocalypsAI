# Nightly Digital Garden Seed Sower

## Overview

The `nightly-garden-seed-sower` is an Ansible playbook designed to help cultivate your digital garden by automatically creating daily templated markdown files. These files can serve as daily journal prompts, thought seeds, or structured starting points for new notes, ensuring a consistent and regular contribution to your knowledge base.

It checks if a daily note for the current date already exists in your specified garden path. If not, it creates one based on a Jinja2 template, encouraging daily reflection and content generation.

## Features

*   **Automated Daily Note Creation**: Generates a new markdown file for each day if one doesn't already exist.
*   **Templated Content**: Uses a customizable Jinja2 template for consistent note structure and prompts.
*   **Idempotent**: Will not overwrite or create duplicate daily notes.
*   **Configurable**: Easily adjust the garden path, filename prefix, and date format.

## Prerequisites

*   Ansible (version 2.9 or higher recommended)
*   A local machine or remote host where your digital garden resides.

## Usage

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the utility directory**:
    ```bash
    cd ansible-playbooks/nightly-garden-seed-sower
    ```
3.  **Configure your garden settings**: Edit `src/vars/garden_settings.yml` to define your `garden_path`, `filename_prefix`, and `date_format`.

    ```yaml
    # src/vars/garden_settings.yml
    garden_path: "/path/to/your/digital/garden" # e.g., "~/Documents/MyDigitalGarden"
    filename_prefix: "daily-seed"             # e.g., "journal", "daily-note"
    date_format: "%Y-%m-%d"                   # Format for the date in the filename (e.g., 2023-10-27)
    ```

4.  **Customize the daily note template**: Modify `src/templates/daily_seed.md.j2` to include your preferred front matter, prompts, or structure.

    ```jinja2
    # src/templates/daily_seed.md.j2
    ---
    title: Daily Thought Seed - {{ current_date }}
    date: {{ current_date }}
    tags: [daily, thoughts, garden]
    status: seedling
    ---

    # Daily Thought Seed for {{ current_date }}

    What new ideas are sprouting in your mind today?
    What connections can you make between existing notes?
    Reflect on something you learned yesterday.

    ---
    ## Notes:
    ```

5.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/sow_seeds.yml
    ```

    This will create a new markdown file (e.g., `daily-seed-2023-10-27.md`) in your `garden_path` if one for today's date doesn't already exist.

## Testing

To run the automated tests for this utility:

```bash
ansible-playbook -i tests/test_inventory.ini tests/test_sow_seeds.yml
```

The tests will:
*   Verify that a new daily seed file is created when it doesn't exist.
*   Verify that no changes are made when a daily seed file for the current date already exists (idempotency).
*   Clean up any test-generated files and directories.
