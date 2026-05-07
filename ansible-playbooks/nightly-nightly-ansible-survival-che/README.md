# nightly‑ansible‑survival‑checklist‑generator

**Purpose**: Generate a simple, whimsical "Survival Checklist" text file on the target host using pure Ansible.  The checklist contains a few classic post‑apocalypse tasks (find water, locate shelter, etc.) and can be easily extended via the `checklist_items` variable.

## How to run
```bash
# From the repository root
ansible-playbook -i tests/inventory.ini src/main.yml
```

The playbook will create a file called `survival_checklist.txt` in the same directory as the playbook (`src/`).  The file will look like:
```
- Find water
- Locate shelter
- Gather food
- Signal for help
```

## Extending the checklist
Edit the `checklist_items` variable inside `src/main.yml` and add or remove items as you wish.  The playbook will automatically render the updated list.

## Tests
Run the bundled test suite with:
```bash
ansible-playbook -i tests/inventory.ini tests/test_checklist.yml
```
The test verifies that the file is created and contains the expected lines.
