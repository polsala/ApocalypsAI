## Nightly Ansible Environment Sync Agent

This Ansible playbook synchronizes environment variables across a defined set of hosts. It's designed to ensure that critical environment variables are consistently set, preventing configuration drift and simplifying deployment.

### Philosophy

"Anarchy with discipline" - this playbook aims to bring order to the chaos of environment variable management through automated, testable, and documented Ansible playbooks.

### Usage

1.  **Prerequisites**: Ansible installed on your control node.
2.  **Inventory**: Create or modify the `inventory.ini` file to list your target hosts and any necessary connection details.
3.  **Variables**: Define the environment variables you wish to synchronize in `vars/environment_vars.yml`. Each variable should be a key-value pair.
4.  **Execution**: Run the playbook using the `ansible-playbook` command:
    ```bash
    ansible-playbook -i inventory.ini sync_env.yml
    ```

### Playbook Structure

*   `sync_env.yml`: The main playbook orchestrating the synchronization.
*   `inventory.ini`: Defines the target hosts for the playbook.
*   `vars/environment_vars.yml`: Contains the list of environment variables to be managed.
*   `templates/env_vars.sh.j2`: Jinja2 template used to generate a script that sets the environment variables.
*   `tests/test_sync_env.yml`: An Ansible playbook for testing the functionality of `sync_env.yml`.
*   `tests/inventory_test.ini`: An inventory file specifically for testing.

### Testing

To run the tests, ensure you have a test environment set up (e.g., using Docker or Vagrant) and then execute:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_sync_env.yml
```

This will apply the playbook to the test inventory and verify that the environment variables are set correctly.
