# nightly-ansible-apt-mirror-setup

## Summary
Sets up a local apt-mirror to cache Debian packages for offline use, ensuring your post‑apocalypse servers stay up‑to‑date.

## Usage
```sh
ansible-playbook -i inventory.ini src/setup_mirror.yml
```
Run with `--check` for a dry run.

## What it does
1. Installs the `apt-mirror` package.
2. Configures `/etc/apt/mirror.list` to mirror the main Debian repositories.
3. Executes `apt-mirror` to download packages.
4. Optionally serves the mirror via a simple HTTP server.

## Disclaimer
This playbook is intended for demonstration and testing in isolated environments. Adjust repository URLs and paths as needed for production.
