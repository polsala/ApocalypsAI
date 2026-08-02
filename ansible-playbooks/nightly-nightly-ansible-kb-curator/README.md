# Nightly Ansible Knowledge Base Curator

This Ansible playbook, the "Wasteland Wisdom Archivist," helps maintain the health and consistency of your digital knowledge base or "Wasteland Wisdom Archive." It scans markdown files for missing metadata, identifies stale documents, and generates a comprehensive report to guide your curation efforts.

## Features

*   **Metadata Check**: Verifies that markdown files have a YAML front matter with essential fields like `title` and `tags`.
*   **Staleness Detection**: Flags files that haven't been modified recently, based on a configurable threshold.
*   **Curation Report**: Generates a detailed report summarizing findings, including files needing attention.

## Usage

1.  **Prerequisites**:
    *   Ansible installed (`pip install ansible`).
    *   A knowledge base directory containing markdown files.

2.  **Configuration**:
    Edit `src/vars/config.yml` to specify:
    *   `knowledge_base_path`: The absolute path to your knowledge base directory.
    *   `stale_threshold_days`: The number of days after which a file is considered stale if not modified.

    Example `src/vars/config.yml`:
    ```yaml
    knowledge_base_path: "/path/to/your/wasteland_wisdom_archive"
    stale_threshold_days: 180 # Files not modified in 180 days are stale
    ```

3.  **Run the Playbook**:
    Navigate to the `ansible-playbooks/nightly-ansible-kb-curator` directory and run:
    ```bash
    ansible-playbook -i src/inventory.ini src/curate_knowledge_base.yml
    ```
    The playbook will generate a `curation_report.txt` in the playbook directory.

## Example Report Output

```
Wasteland Wisdom Archive Curation Report (Generated: YYYY-MM-DD HH:MM:SS)
-----------------------------------------------------------------------

Total Files Scanned: 5
Files Needing Attention: 3

--- Files with Missing Metadata ---
- /path/to/your/kb/missing_meta_doc.md: Missing title, Missing tags

--- Stale Files (Modified > 180 days ago) ---
- /path/to/your/kb/old_research.md (Last Modified: YYYY-MM-DD)

--- Healthy Files ---
- /path/to/your/kb/daily_log.md
- /path/to/your/kb/new_discovery.md
```

## Development & Testing

To run the tests, ensure you have Ansible installed. The tests use a local `tests/test_inventory.ini` and a set of mock files in `tests/test_files`.

```bash
# From the root of the nightly-ansible-kb-curator directory
ansible-playbook -i tests/test_inventory.ini tests/test_curate_knowledge_base.yml
```
This will execute the playbook against the test files and verify the generated report.
