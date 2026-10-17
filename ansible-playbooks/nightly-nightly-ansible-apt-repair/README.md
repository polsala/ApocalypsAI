# nightly-ansible-apt-repair

**Purpose**: Quickly bring a Debian/Ubuntu system back from the brink of package chaos after a simulated apocalypse. The playbook updates the package index, upgrades all packages, removes orphaned packages, and sets a friendly fact indicating the system has been healed.

## How it works
1. **Update APT cache** – ensures we have the latest package information.
2. **Upgrade packages** – applies any pending upgrades.
3. **Autoremove** – cleans up packages that are no longer needed.
4. **Set a fact** `apt_repaired: true` – used by the test suite to verify success.
5. **Display a whimsical message** – because even servers deserve a morale boost.

## Usage
```bash
# From the repository root
ansible-playbook -i src/inventory.ini src/playbook.yml
```

## Running the tests
The test suite validates that the `apt_repaired` fact is set after the playbook runs.
```bash
ansible-playbook -i src/inventory.ini tests/test_playbook.yml
```
If the playbook completes without errors and the assertion passes, you will see a green success message.

## Disclaimer
This playbook is safe to run on any Debian‑based host. It only performs standard APT operations and does not modify system files beyond the package manager.
