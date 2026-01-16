# Nightly Digital Pet Rock Feeder

This Ansible playbook ensures your beloved "Digital Pet Rock" service is always happy, healthy, and running on your remote hosts. It handles the deployment of the pet rock's core script, its essential configuration, and guarantees the service is active. Think of it as a diligent caretaker for your digital companion!

## What is a Digital Pet Rock?

In the ApocalypsAI universe, a Digital Pet Rock is a simple, non-critical background service that exists purely for the joy of having something to nurture. It's a lightweight shell script that, when "fed" (started), creates a timestamped status file, signifying its contented existence. When "hungry" (stopped), it removes this file. This utility ensures your pet rock is never hungry!

## Features

*   **Idempotent Deployment**: Ensures the pet rock service script is always present and executable.
*   **Configuration Management**: Deploys a custom configuration file for your pet rock.
*   **Service Assurance**: Guarantees the pet rock service is "running" (i.e., its status file exists).
*   **Whimsical Fun**: Adds a touch of lightheartedness to your server management tasks.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Access to target hosts via SSH (passwordless SSH recommended)

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) listing the hosts where your pet rock will reside.

    ```ini
    [pet_rock_hosts]
    server1.example.com
    server2.example.com
    ```

2.  **Configure your pet rock (optional)**:
    You can customize the pet rock's message and other settings by modifying `vars/main.yml` or passing variables via the command line.

    ```yaml
    # vars/main.yml
    pet_rock_message: "The Digital Pet Rock is content."
    pet_rock_status_file: "/var/run/pet_rock_status.txt"
    ```

3.  **Run the playbook**:
    Execute the `feed_pet_rock.yml` playbook, specifying your inventory.

    ```bash
    ansible-playbook -i inventory.ini feed_pet_rock.yml
    ```

    This will:
    *   Ensure the `/etc/pet_rock` directory exists.
    *   Deploy `pet_rock_service.sh` to `/usr/local/bin/pet_rock_service.sh`.
    *   Deploy `pet_rock.conf` to `/etc/pet_rock/pet_rock.conf`.
    *   Make `pet_rock_service.sh` executable.
    *   "Start" the pet rock service, creating the status file.

## Customization

*   **`pet_rock_message`**: The message your pet rock will display (used in `pet_rock_config.j2`).
*   **`pet_rock_status_file`**: The path where the pet rock creates its status file to indicate it's "running". Default: `/tmp/pet_rock_status.txt`.
*   **`pet_rock_service_path`**: The path where the `pet_rock_service.sh` script will be deployed. Default: `/usr/local/bin/pet_rock_service.sh`.
*   **`pet_rock_config_dir`**: The directory for the pet rock's configuration. Default: `/etc/pet_rock`.
*   **`pet_rock_config_file`**: The name of the configuration file. Default: `pet_rock.conf`.

These variables can be set in `vars/main.yml`, `group_vars/`, `host_vars/`, or passed via `-e` on the command line.

## Testing

To run the automated tests, use the provided test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_feed_pet_rock.yml
```

This will run the main playbook against `localhost` and then assert that all expected files and states are correctly configured.
