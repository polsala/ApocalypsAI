# nightly-ansible-apt-repo-sync

Synchronizes apt package lists across multiple Debian/Ubuntu hosts to ensure consistent repositories.

## Overview

The playbook updates the apt cache on all target hosts, gathers the list of installed packages, and then ensures each host has the same set of packages installed. It is useful for keeping a fleet of servers in lockstep after provisioning.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/playbook.yml
```

Edit `src/inventory.ini` to list your target hosts.

## How it works

1. Update apt cache.
2. Gather installed packages.
3. Compute the union of packages across all hosts.
4. Install missing packages on each host.

## License

MIT
