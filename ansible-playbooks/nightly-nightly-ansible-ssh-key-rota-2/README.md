Nightly Ansible SSH Key Rotator

Utility that rotates SSH host keys on a set of servers using Ansible.
It generates a fresh RSA key pair, distributes the public key, and removes the old private key.
Designed for local testing (localhost) but can be pointed at any inventory.

Usage:
1. Install Ansible if not present: pip install ansible
2. Run the playbook (dry-run): ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml --check
3. Run for real (will create keys in ./keys): ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml

The playbook stores generated keys under 'keys/' directory relative to the project root.

Files:
- src/rotate_ssh_keys.yml â Main playbook.
- src/inventory.ini â Inventory (default localhost).
- src/vars.yml â Variables (key directory, key type, size).
- tests/run_test.sh â Automated test script.

Whimsical Note:
Each rotation is a tiny apocalypse for the old keys, making way for fresh, hopeful beginnings.

