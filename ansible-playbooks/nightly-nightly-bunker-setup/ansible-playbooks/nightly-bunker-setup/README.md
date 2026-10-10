# Nightly Bunker Setup

**Utility:** `nightly-bunker-setup`

**Purpose**: Spin up a playful, post‑apocalyptic "bunker" directory hierarchy on any host. The playbook creates a `bunker` folder in the user's home directory with sub‑folders for food, water, and tools, each containing a whimsical README.

## Files
- `src/setup_bunker.yml` – The main Ansible playbook.
- `inventory.ini` – Simple localhost inventory.
- `tests/test_setup_bunker.yml` – Automated test that runs the playbook and verifies the created structure.

## Usage
```bash
# Install Ansible if you don't have it
pip install ansible

# Run the playbook
ansible-playbook -i inventory.ini src/setup_bunker.yml
```

## Running the Tests
```bash
ansible-playbook -i inventory.ini tests/test_setup_bunker.yml
```
The test imports the main playbook, executes it, and then asserts that the expected directories and README files exist.

## Whimsical Touch
Each README contains a tongue‑in‑cheek note like "Canned beans and hope." – perfect for a light‑hearted devops break.
