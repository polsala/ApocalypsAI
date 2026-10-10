# nightly-ansible-docker-prune

An Ansible playbook that safely prunes dangling Docker images (and optionally stopped containers) on target hosts. Useful for reclaiming disk space on CI runners or development machines.

## Requirements

- Ansible 2.10+
- `community.docker` collection (`ansible-galaxy collection install community.docker`)
- Docker daemon running on the target hosts.

## Variables

- `docker_prune_enabled` (bool, default: true) – Set to `false` to skip pruning.
- `prune_containers` (bool, default: false) – When `true`, also removes stopped containers.

## Usage

```bash
ansible-playbook -i inventory.ini src/prune.yml -e "docker_prune_enabled=true prune_containers=true"
```

## Testing

Run the included test playbook to verify skip logic without needing Docker:

```bash
ansible-playbook -i inventory.ini tests/test_prune.yml
```

The test ensures that when `docker_prune_enabled` is set to `false`, the playbook reports the skip correctly.
