# Nightly Scroll Scribe

The Nightly Scroll Scribe is a diligent Ansible playbook designed to maintain the pristine order of your digital knowledge base. Like an ancient librarian, it meticulously checks your markdown files (or other text-based "scrolls") to ensure they adhere to predefined structural conventions, such as the presence of YAML front matter and specific tags.

## Features

*   **Front Matter Validation**: Checks if specified files contain valid YAML front matter.
*   **Key Enforcement**: Ensures required keys (e.g., `title`, `date`) are present within the front matter.
*   **Tag Enforcement**: Ensures required tags are present within the `tags` list in the front matter.
*   **Customizable Rules**: Easily configure target directories, required front matter keys, and tags.
*   **Detailed Reporting**: Provides a summary of compliant and non-compliant scrolls with specific issues.

## Prerequisites

*   Ansible (version 2.9 or higher)
*   Python 3 (for Ansible)
*   `jq` (for running automated tests, used to parse Ansible's JSON output)

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) that targets the machine where your scrolls reside. For local execution, you can use `localhost`.

    ```ini
    [local]
    localhost ansible_connection=local
    ```

2.  **Configure your rules**:
    Edit `vars/main.yml` to specify:
    *   `scroll_directory`: The path to the directory containing your markdown files.
    *   `required_front_matter_keys`: A list of keys that *must* be present in the YAML front matter (e.g., `title`, `date`, `tags`).
    *   `required_tags`: A list of specific tags that *must* be present in the `tags` list within the front matter.

    Example `vars/main.yml`:
    ```yaml
    scroll_directory: "/path/to/your/notes"
    required_front_matter_keys:
      - title
      - date
      - tags
    required_tags:
      - knowledge
      - reference
    ```

3.  **Run the Scribe**:
    Execute the playbook using Ansible:

    ```bash
    ansible-playbook -i inventory.ini scribe_playbook.yml
    ```

    The playbook will scan your scrolls and report any inconsistencies directly to your console.

## Automated Tests

To run the automated tests:

```bash
./run_tests.sh
```

This script will:
1.  Create a temporary directory with mock markdown files, some compliant and some non-compliant.
2.  Run the `test_scribe_playbook.yml` which executes the main `scribe_playbook.yml` against these mock files, overriding the `scroll_directory` variable.
3.  Parse the JSON output from Ansible using `jq`.
4.  Assert that the playbook correctly identifies the compliant and non-compliant files based on the defined rules and reports specific issues.

## Example Output

```
PLAY [Ensure digital scrolls are properly formatted] ***************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Initialize compliance lists] *********************************************
ok: [localhost]

TASK [Find all markdown scrolls] ***********************************************
ok: [localhost]

TASK [Check front matter and tags for each scroll] *****************************
ok: [localhost] => (item=/tmp/scroll_scribe_test/good_scroll.md)
ok: [localhost] => (item=/tmp/scroll_scribe_test/no_front_matter.md)
ok: [localhost] => (item=/tmp/scroll_scribe_test/missing_key.md)
ok: [localhost] => (item=/tmp/scroll_scribe_test/missing_tag.md)
ok: [localhost] => (item=/tmp/scroll_scribe_test/malformed_front_matter.md)

TASK [Report compliant scrolls] ************************************************
ok: [localhost] => {
    "msg": "COMPLIANT SCROLLS: ['/tmp/scroll_scribe_test/good_scroll.md']"
}

TASK [Report non-compliant scrolls] ********************************************
ok: [localhost] => {
    "msg": "NON-COMPLIANT SCROLLS: ['/tmp/scroll_scribe_test/no_front_matter.md', '/tmp/scroll_scribe_test/missing_key.md', '/tmp/scroll_scribe_test/missing_tag.md', '/tmp/scroll_scribe_test/malformed_front_matter.md']"
}

TASK [Display detailed issues for non-compliant scrolls] ***********************
ok: [localhost] => {
    "msg": "ISSUES FOR /tmp/scroll_scribe_test/no_front_matter.md: ['Missing or malformed YAML front matter']"
}
ok: [localhost] => {
    "msg": "ISSUES FOR /tmp/scroll_scribe_test/missing_key.md: ['Missing required key: date']"
}
ok: [localhost] => {
    "msg": "ISSUES FOR /tmp/scroll_scribe_test/missing_tag.md: ['Missing required tag: reference']"
}
ok: [localhost] => {
    "msg": "ISSUES FOR /tmp/scroll_scribe_test/malformed_front_matter.md: ['Missing or malformed YAML front matter']"
}

PLAY RECAP *********************************************************************
localhost                  : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
