# nightly-apt-mirror-magic

Synchronize a remote APT package mirror to a local directory using rsync.
Useful for creating offline package caches for isolated environments.

## Requirements

- Ansible 2.9+
- rsync installed on the target host
- SSH access to the remote mirror host

## Variables

- `remote_mirror`: URL of the remote mirror (e.g., user@mirror.example.com:/var/www/ubuntu)
- `local_mirror_dir`: Path on the target where the mirror will be stored (default: /var/local/apt-mirror)

## Usage

Create an inventory file with the target host(s) and run:

```
ansible-playbook -i inventory.ini src/playbook.yml -e "remote_mirror=user@mirror.example.com:/var/www/ubuntu"
```

The playbook will ensure the local directory exists and then rsync the contents.

## License

MIT
