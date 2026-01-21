# Nightly Zen Quote MOTD

An Ansible playbook that installs a daily rotating Zen quote as the system MOTD. It copies a set of inspirational quotes, installs a script that picks a random quote each day, and schedules it via cron.

## Usage

```sh
ansible-playbook -i inventory.ini playbook.yml
```

The playbook works on any Linux host with `shuf` available.
