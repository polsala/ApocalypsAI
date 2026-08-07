# nightly-ghost-buster

**What it does**

This utility is an Ansible playbook that scans target hosts for processes owned by the `nobody` user (often leftover or mis‑configured "ghost" processes) and terminates them. After the cleanup it prints a fun exorcism message so you know the spirits have been banished.

**Why it exists**

* Ghost processes can waste CPU/RAM and make system monitoring noisy.
* Automating their removal saves admins from manual `ps | grep` gymnastics.
* The playful output keeps the operation light‑hearted in otherwise grim server maintenance.

**Requirements**

* Ansible 2.9+ installed on the control node.
* SSH access / appropriate inventory for the hosts you want to clean.

**Usage**

```bash
# Clone the repository (or copy the playbook into your own repo)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/ansible-playbooks/nightly-ghost-buster

# Run the playbook against your inventory
ansible-playbook -i inventory.ini src/ghost_buster.yml
```

**Inventory**

Create a simple `inventory.ini` in the same directory, for example:

```ini
[servers]
myhost.example.com ansible_user=admin
```

**Safety**

* The playbook only targets processes owned by `nobody`. Adjust the `command` line if you need a different criterion.
* It runs with `become: true`, so ensure you have sudo privileges on the remote hosts.

**Testing**

Run the bundled unit tests with:

```bash
python -m unittest discover -s tests
```

The tests verify that the playbook structure is as expected and that the mock execution logic behaves correctly.
