Nightly Apt Cleanup

Overview
This Ansible playbook helps keep Debian/Ubuntu hosts tidy after the apocalypse. It:
- Removes packages that are no longer required (apt autoremove).
- Cleans the local package cache (apt clean).
- Generates a plain-text report summarizing actions taken.

Usage
Run the playbook with:
ansible-playbook -i src/inventory.ini src/playbook.yml

The report is saved to apt_cleanup_report.txt on the control machine.

Files
src/playbook.yml – the main playbook.
src/inventory.ini – example inventory (localhost by default).
tests/test_playbook.py – unit tests that mock Ansible execution.

License
MIT
