Nightly Apocalypse Quote Rotator

This Ansible playbook installs a collection of apocalypse-themed quotes on the target host and configures a daily cron job that updates the system MOTD with a random quote each morning at 9:00 AM. It also updates the MOTD immediately when the playbook is run.

Prerequisites
- Ansible 2.9 or newer installed on the control machine.
- The target host must have the `shuf` utility (part of coreutils) available.

Installation
1. Clone the repository or copy the files into a directory.
2. Run the playbook:
   ansible-playbook -i src/inventory.ini src/setup_quotes.yml

What the playbook does
- Copies a list of quotes to /usr/local/share/apocalypse_quotes.txt on the target.
- Installs a cron job that runs daily at 09:00 and writes a random quote to /etc/motd.
- Immediately selects a random quote and writes it to /etc/motd so you see a new message right away.

Idempotence
The playbook is safe to run multiple times; Ansible will only make changes when necessary.

Testing
A simple syntax‑check test is provided under the tests/ directory. Run it with:
   ansible-playbook -i src/inventory.ini tests/test_setup_quotes.yml --check
