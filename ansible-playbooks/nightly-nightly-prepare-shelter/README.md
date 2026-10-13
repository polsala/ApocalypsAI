# nightly-prepare-shelter

**Purpose**: Quickly provision a “shelter” on any Linux host. The playbook creates a dedicated directory (`/tmp/shelter`) and drops a `ready.txt` flag file containing a friendly message. Perfect for testing, demos, or just adding a bit of post‑apocalyptic flair to your CI runners.

## Files
- `src/prepare_shelter.yml` – The Ansible playbook.
- `src/inventory.ini` – Simple inventory targeting `localhost`.
- `tests/test_prepare_shelter.yml` – Automated test that runs the playbook and verifies the flag file.

## Requirements
- Ansible 2.9+ installed on the machine where you run the playbook.
- No special privileges are required; everything lives under `/tmp`.

## Usage
```bash
# Clone the repository (or copy the utility folder) and cd into it
cd ansible-playbooks/nightly-prepare-shelter

# Run the playbook
ansible-playbook -i src/inventory.ini src/prepare_shelter.yml
```

You should see a message like:
```
TASK [Create shelter readiness flag] *******************************************
changed: [localhost]
```

After execution, verify the file:
```bash
cat /tmp/shelter/ready.txt
```
Output:
```
Shelter is ready. Stay safe!
```

## Testing
The repository includes an Ansible test playbook that runs the same playbook and asserts the flag file exists and contains the expected text.
```bash
ansible-playbook -i src/inventory.ini tests/test_prepare_shelter.yml
```
All tasks should pass with `ok` status.

---
*Feel free to adapt the directory or message to suit your own post‑apocalyptic scenario!*
