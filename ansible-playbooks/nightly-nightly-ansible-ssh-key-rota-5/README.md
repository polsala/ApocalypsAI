# nightly-ansible-ssh-key-rotator

## Overview

`nightly-ansible-ssh-key-rotator` is a whimsical yet practical Ansible playbook that rotates the SSH host keys on every host in your inventory. Fresh host keys improve security and help you avoid the dreaded "unknown host" warnings after a server rebuild.

## Features

- Generates RSA, ECDSA, and Ed25519 host keys if they are missing.
- Reloads the `sshd` service only when new keys are created.
- Works with any inventory (static or dynamic).
- Safe to run repeatedly – it will not overwrite existing keys unless you explicitly delete them.

## Usage

```bash
# Install Ansible if you haven't already
pip install ansible

# Clone the repository (or copy the files into your own repo)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/ansible-playbooks/nightly-ansible-ssh-key-rotator

# Review or edit the sample inventory (src/inventory.ini)
cat src/inventory.ini

# Run the playbook (you will need sudo privileges on the target hosts)
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -K
```

The `-K` flag prompts for the become password. If you have password‑less sudo configured, you can omit it.

## Testing

A deterministic, offline test is provided under `tests/`. It runs the playbook in **check mode** against the sample inventory and asserts that the execution exits with a zero status code.

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```

## License

MIT © ApocalypsAI community
