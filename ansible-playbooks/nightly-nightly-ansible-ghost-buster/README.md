# nightly-ansible-ghost-buster

## Overview

`nightly-ansible-ghost-buster` is a whimsical yet practical Ansible playbook that searches for files with the **`.ghost`** extension (the kind of files that haunt your filesystem), archives them into `/tmp/ghosts.tar.gz`, and prints a short report.

The playbook is completely self‑contained and runs against any inventory you provide – the default example uses the local machine.

## Features

- Recursively finds `*.ghost` files in a configurable directory.
- Archives all discovered ghost files into a single tarball (`/tmp/ghosts.tar.gz`).
- Emits a concise debug message reporting how many ghosts were captured.
- Includes a tiny test harness that creates dummy ghost files, runs the playbook, and verifies the archive was produced.

## Quick Start

```bash
# Clone the repository (or copy this folder) and cd into it
cd ansible-playbooks/nightly-ansible-ghost-buster

# Run the bundled test (requires ansible and bash)
./tests/run_test.sh
```

If the test passes you will see something like:

```
PLAY [Ghost Buster] *****************************************************************
...
ok: [localhost] => {
    "msg": "Archived 2 ghost files."
}

PLAY RECAP ***********************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

TEST SUCCESS: Ghost archive created at /tmp/ghosts.tar.gz
```

## Customisation

- **search_path** – Change the directory to scan by editing the `search_path` variable in `playbook.yml` or by passing `-e search_path=/my/dir` on the command line.
- **archive_dest** – The destination of the tarball can be overridden similarly.

## License

MIT – feel free to adapt, share, and haunt responsibly!
