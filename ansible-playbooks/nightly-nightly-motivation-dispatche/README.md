# Nightly Motivation Dispatcher

## Overview

`nightly-motivation-dispatcher` is a tiny Ansible playbook that picks a random motivational quote from a builtâin list and writes it to a file (default: `/tmp/motivation.txt`).  It can be used in cron jobs, CI pipelines, or any automation that needs a daily boost of inspiration.

## Files

- `inventory.ini` â simple inventory targeting the local host.
- `playbook.yml` â the main playbook that selects a quote and writes it.
- `vars/quotes.yml` â a small collection of quotes.
- `tests/test_playbook.yml` â an offline deterministic test that runs the playbook with a known quote and asserts the file content.

## Usage

```bash
# Install Ansible if you don't have it
python3 -m pip install ansible

# Run the playbook (will pick a random quote)
ansible-playbook -i inventory.ini playbook.yml

# Check the result
cat /tmp/motivation.txt
```

## Running the Tests

The test suite is pure Ansible and does not require network access.  It forces a deterministic quote and verifies the output file.

```bash
ansible-playbook -i inventory.ini tests/test_playbook.yml
```

If the test passes you will see `PLAY RECAP` with `ok=3` and no failures.

## Customisation

- **Change the destination file**: edit the `dest` parameter in `playbook.yml`.
- **Add your own quotes**: edit `vars/quotes.yml` and add more entries to the `quotes` list.
- **Integrate with Slack or email**: replace the `copy` task with a `uri` or `mail` task using the `selected_quote` variable.

---

*Created by the ApocalypsAI Nightly Integrator*
