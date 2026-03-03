# Nightly Ansible Daily Motivation

This utility is an Ansible playbook that selects a random motivational quote from a built‑in list and writes it to `motivation.txt` in the current working directory. Perfect for a quick morale boost during automation runs.

## Usage

```sh
ansible-playbook -i localhost, -c local ansible-playbooks/nightly-ansible-daily-motivation/src/playbook.yml
```

The playbook will create (or overwrite) `motivation.txt` with a random quote.

## Testing

Run the integration test with:

```sh
ansible-playbook -i localhost, -c local ansible-playbooks/nightly-ansible-daily-motivation/tests/test_motivation.yml
```

The test ensures the file is created and contains one of the expected quotes.
