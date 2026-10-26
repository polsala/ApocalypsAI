# Nightly Package Gardener

The `nightly-package-gardener` is an Ansible playbook designed to keep your systems' package installations in a state of serene balance. It acts as a digital horticulturist, ensuring that all your "essential" software packages are present and up-to-date, while gracefully "weeding out" any "whimsical" or non-essential packages that might have sprouted unexpectedly.

## Features

*   **Essential Package Nurturing:** Automatically installs any missing packages defined as essential.
*   **Whimsical Package Pruning:** Removes specified non-essential packages to keep your system lean and focused.
*   **Idempotent Operation:** Running the playbook multiple times will achieve the same desired state without redundant actions.
*   **Customizable:** Easily define your list of essential and whimsical packages.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (sudo/become).

### 1. Configure Inventory

Edit `src/inventory.ini` to list your target servers. For local testing, `localhost` is pre-configured.

```ini
# src/inventory.ini
[servers]
localhost ansible_connection=local
# server1.example.com
# server2.example.com
```

### 2. Define Packages

Edit `vars/main.yml` to specify your `essential_packages` (always present) and `whimsical_packages` (always absent).

```yaml
# vars/main.yml
essential_packages:
  - curl
  - wget
  - git
  - htop
whimsical_packages:
  - cowsay
  - fortune-mod
  - sl
```

### 3. Run the Playbook

Execute the playbook from the root of the `nightly-package-gardener` directory:

```bash
ansible-playbook -i src/inventory.ini src/package_gardener.yml
```

To perform a dry run and see what changes would be made without actually applying them:

```bash
ansible-playbook -i src/inventory.ini src/package_gardener.yml --check
```

## Testing

The utility includes a self-contained test playbook that mocks system facts to verify the core logic of identifying packages for installation and removal.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_package_gardener.yml
```

This will run through predefined scenarios, asserting that the playbook correctly identifies which packages should be installed or removed based on mocked system states.
