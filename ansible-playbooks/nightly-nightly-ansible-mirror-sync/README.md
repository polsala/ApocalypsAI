# Nightly Ansible Mirror Sync

A whimsical Ansible playbook that synchronizes apt package mirrors across your fleet, ensuring every post‑apocalyptic outpost has the same package cache. Ideal for offline environments or when you just want to keep your mirrors in lockstep.

## Features

- Creates target mirror directory if missing
- (Mock) syncs packages from a source mirror URL to the target path
- Sets a fact `mirror_sync_success` that can be used in downstream automation
- Includes a simple test playbook that validates the sync succeeded

## Usage

```sh
ansible-playbook -i inventory.ini src/sync_mirror.yml
```

You can override variables:

```sh
ansible-playbook -i inventory.ini src/sync_mirror.yml \
  -e "source_mirror_url=http://archive.ubuntu.com/ubuntu target_mirror_path=/opt/mirror"
```

## Testing

Run the bundled test playbook:

```sh
ansible-playbook -i inventory.ini tests/test_sync_mirror.yml
```

It will import the main playbook and assert that `mirror_sync_success` is true.
