# Nightly Digital Gardener

## Whimsical-yet-Useful Utility: Cultivating Your Digital Garden

This Ansible playbook, the `Nightly Digital Gardener`, helps you maintain a healthy and well-organized collection of markdown notes, often referred to as a "digital garden" or knowledge base. It ensures your notes adhere to a consistent structure, preventing your garden from becoming overgrown with unkempt files and wilting metadata.

### Features

*   **Front Matter Validation**: Checks if your markdown files (`.md`) have the required YAML front matter fields (e.g., `title`, `tags`, `date`).
*   **Report Generation**: Creates a `garden_report.txt` summarizing healthy notes and those needing "pruning" (i.e., attention due to missing or malformed front matter).
*   **Whimsical Naming**: Embrace the joy of gardening while keeping your digital space tidy!

### Prerequisites

*   Ansible (version 2.10 or newer recommended)
*   A directory containing your markdown notes (your "digital garden").

### How to Use

1.  **Define Your Garden**: Create an `inventory.ini` file (or use `localhost` as shown in the example) and a `vars/garden_config.yml` file to specify the path to your digital garden and the required front matter fields.

    **`inventory.ini` example:**
    ```ini
    [gardeners]
    localhost
    ```

    **`vars/garden_config.yml` example:**
    ```yaml
    garden_path: "./my_notes"
    required_front_matter_fields:
      - title
      - tags
      - date
    ```

2.  **Run the Gardener**: Execute the playbook from the utility's root directory:

    ```bash
    ansible-playbook -i inventory.ini src/garden_playbook.yml
    ```

3.  **Review the Report**: After execution, a `garden_report.txt` will be generated in your specified `garden_path`. This report will list:
    *   `Healthy Notes`: Files that meet all specified criteria.
    *   `Notes Needing Pruning`: Files with missing or malformed front matter, along with the reasons.

### Example Output (`garden_report.txt`)

```
Digital Garden Cultivation Report - 2023-10-27T10:30:00

---
Healthy Notes (1):
- /path/to/my_notes/my_first_healthy_note.md

---
Notes Needing Pruning (2):
- /path/to/my_notes/untitled_thought.md
  Reason: Missing or incomplete front matter
  Missing Fields: title, tags
- /path/to/my_notes/broken_yaml.md
  Reason: Missing or incomplete front matter

---
Summary:
Total notes scanned: 3
Healthy notes: 1
Notes needing pruning: 2
```

### Development & Testing

To run the automated tests for this utility:

```bash
ansible-playbook -i inventory.ini tests/test_garden_playbook.yml
```

This will create a temporary digital garden, populate it with test files, run the main playbook, and assert the correctness of the generated report. The temporary garden will be cleaned up automatically.
