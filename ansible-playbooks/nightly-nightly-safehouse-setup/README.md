# Nightly Safehouse Setup

An Ansible playbook that creates a post‑apocalyptic safe‑house directory structure for storing essential supplies.

## Features

- Creates a base directory (default `/tmp/safehouse`) with subfolders:
  - `food`
  - `water`
  - `tools`
  - `medicine`

## Usage

```sh
ansible-playbook -i inventory.ini src/setup_safehouse.yml -e "base_path=/path/to/safehouse"
```

If `base_path` is omitted, `/tmp/safehouse` is used.

## Testing

Run the provided test playbook:

```sh
ansible-playbook -i inventory.ini tests/test_setup_safehouse.yml
```
