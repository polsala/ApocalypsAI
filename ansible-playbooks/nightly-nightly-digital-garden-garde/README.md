# Nightly Digital Garden Gardener

This Ansible playbook helps you maintain a tidy and organized "digital garden" of markdown notes, articles, or documentation. It ensures consistency in your files' front matter and automatically generates an index for easy navigation.

## Features

*   **Front Matter Validation**: Scans markdown files for required YAML front matter keys (e.g., `title`, `date`).
*   **Missing Key Reporting**: Reports files that are missing essential front matter fields.
*   **Automatic Index Generation**: Creates or updates a `_garden_index.md` file that lists all your garden notes with links.
*   **Whimsical Cultivation**: Keeps your knowledge base blooming with structure!

## Usage

### Prerequisites

*   Ansible installed (version 2.10+ recommended).
*   Access to the target machine (usually `localhost` for a personal garden).

### Files

*   `src/garden_playbook.yml`: The main Ansible playbook.
*   `src/inventory.ini`: A sample inventory file, configured for `localhost`.
*   `src/vars/garden_config.yml`: Configuration for your garden path and required front matter keys.
*   `templates/garden_index.j2`: Jinja2 template for the generated `_garden_index.md` file.

### Configuration

Edit `src/vars/garden_config.yml` to define your digital garden's root path and the front matter keys you deem essential:

```yaml
garden_path: "{{ playbook_dir }}/my_garden" # Path to your markdown files
required_front_matter_keys:
  - title
  - date
  - tags
```

### Running the Playbook

1.  Navigate to the `nightly-digital-garden-gardener` directory.
2.  Run the playbook:

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_playbook.yml
    ```

    To see what changes *would* be made without actually applying them (dry run):

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_playbook.yml --check
    ```

### Expected Output

The playbook will output a report indicating any markdown files with missing front matter keys. It will also create or update `_garden_index.md` in your specified `garden_path`.

## Testing

To run the automated tests for this utility:

```bash
ansible-playbook -i src/inventory.ini tests/test_garden_playbook.yml
```

The tests will:

1.  Create a temporary test garden directory.
2.  Populate it with mock markdown files, some valid, some with missing front matter.
3.  Run the main `garden_playbook.yml` against this temporary garden.
4.  Assert that the playbook correctly identifies files with missing front matter.
5.  Assert that the `_garden_index.md` file is generated and contains the expected entries.
6.  Clean up the temporary test environment.
