# Nightly Ansible Environment Sync Agent (with Age)

This Ansible playbook synchronizes environment variables across a defined set of hosts. It adds a whimsical twist by allowing variables to have an 'age' or expiration, effectively removing them after a specified duration.

## Features

*   **Environment Variable Synchronization**: Distributes environment variables to target hosts.
*   **Variable Expiration (Age)**: Supports defining an 'age' for variables, after which they are automatically removed.
*   **Idempotent**: Ensures that running the playbook multiple times has the same effect as running it once.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts with appropriate credentials.
*   Python installed on target hosts (required by Ansible modules).

## Usage

1.  **Define your inventory**: Update the `inventory.ini` file with your target hosts.
2.  **Configure environment variables**: Edit `vars/environment_vars.yml` to define your environment variables and their optional 'age' in days.
3.  **Run the playbook**: Execute the playbook using the `ansible-playbook` command:
    ```bash
    ansible-playbook -i inventory.ini sync_env.yml
    ```

## `vars/environment_vars.yml` Structure

Variables are defined as a list of dictionaries. Each dictionary represents an environment variable.

*   `name`: The name of the environment variable (required).
*   `value`: The value of the environment variable (required).
*   `age_days`: The number of days until the variable expires and is removed. If omitted, the variable is permanent.

**Example:**

```yaml
environment_vars:
  - name: "MY_APP_CONFIG"
    value: "/etc/myapp/config.json"
  - name: "TEMPORARY_TOKEN"
    value: "supersecret123"
    age_days: 7
  - name: "ANOTHER_VAR"
    value: "some_value"
    age_days: 1
```

## Testing

This playbook includes basic tests using `ansible-playbook` with a test inventory. To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_sync_env.yml
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
