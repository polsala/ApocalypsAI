# Nightly Ansible SSH Key Rotator

Utility that rotates SSH host keys and updates authorized_keys across all hosts in an Ansible inventory. Useful for periodic key rotation to improve security.

## Usage

```sh
ansible-playbook -i inventory.ini src/playbook.yml
```

The playbook will:

1. Generate a new SSH host key pair.
2. Distribute the new public key to all hosts' `authorized_keys`.
3. Restart the SSH service.

## Testing

Run the unit test with:

```sh
python -m unittest discover -s tests
```

The test mocks the `ansible-playbook` command to ensure the playbook can be invoked without errors.
