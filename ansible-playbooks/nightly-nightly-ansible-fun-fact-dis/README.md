# Nightly Ansible Fun Fact Distributor

Utility that distributes a random fun fact to target hosts, writing it to a configurable file (default `/etc/motd_fun_fact`). Each run picks a different fact from a curated list, adding a whimsical touch to server logins.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/fun_fact.yml
```

You can override the destination path with the `dest_path` extra variable:

```bash
ansible-playbook -i src/inventory.ini src/fun_fact.yml -e "dest_path=/tmp/my_fact.txt"
```

## Variables

- `fun_facts`: list of strings (default provided).
- `dest_path`: destination file path where the fact will be written (default `/etc/motd_fun_fact`).

## How it works

The playbook selects a random fact using the `random` filter and writes it to the specified file on each host.
