## Nightly Ansible Environment Sync

This utility provides an Ansible playbook designed to synchronize a defined set of environment variables across multiple hosts. It's useful for ensuring consistency in application configurations or system settings that rely on environment variables.

### Philosophy

* **Consistency is key**: Ensure your distributed systems have the same environmental context.
* **Automated and idempotent**: Run this playbook to bring your environments into a desired state.

### Usage

1.  **Prerequisites**: Ensure you have Ansible installed and SSH access to your target hosts.
2.  **Inventory**: Create or modify the `inventory.ini` file to list your target hosts and any necessary connection details.
3.  **Variables**: Define the environment variables you wish to synchronize in `vars/environment_vars.yml`. Each variable should be a key-value pair.
4.  **Run the Playbook**: Execute the playbook using the `ansible-playbook` command:
    ```bash
    ansible-playbook -i inventory.ini sync_env.yml
    ```

### Playbook Structure

*   `sync_env.yml`: The main playbook file.
*   `inventory.ini`: Defines the target hosts.
*   `vars/environment_vars.yml`: Contains the list of environment variables to synchronize.
*   `templates/env_vars.sh.j2`: Jinja2 template to generate a script that sets the environment variables.
*   `tests/test_sync_env.yml`: A basic Ansible playbook to test the functionality.
*   `tests/inventory_test.ini`: An inventory file for testing.

### Example `vars/environment_vars.yml`

```yaml
environment_variables:
  APP_ENV: "production"
  DATABASE_URL: "postgres://user:pass@host:port/db"
  LOG_LEVEL: "INFO"
```

### Example `inventory.ini`

```ini
[webservers]
server1.example.com
server2.example.com

[databases]
db1.example.com
```

### Testing

This utility includes a basic test playbook. To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_sync_env.yml
```

This test playbook will target a dummy host and verify that the environment variables are set correctly (or at least that the playbook runs without errors).
