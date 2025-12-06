# Nightly Apocalyptic Garden Tender

## Summary
This Ansible playbook, `nightly-apoc-garden-tender`, automates the setup and simulated tending of a post-apocalyptic garden plot. It includes tasks for environmental monitoring, resource management (like simulated watering and fertilizing), and generating a basic harvest report. It's designed to help survivors efficiently manage their vital food sources in a resource-scarce world, albeit in a simulated environment.

## How it Works
The playbook orchestrates several roles:
1.  **`garden_setup`**: Initializes the garden environment, creating necessary directories and simulating the installation of basic tools.
2.  **`garden_monitor`**: Simulates environmental sensor readings (e.g., soil moisture, temperature) and logs them.
3.  **`garden_tend`**: Based on the simulated sensor data, it performs conditional actions like 'watering' or 'fertilizing' the plot.
4.  **`garden_report`**: Compiles a summary of the garden's status and actions taken into a readable report.

All interactions with the 'garden' are simulated through file operations and variable manipulation, making it safe to run and easy to test.

## Prerequisites
-   Ansible (version 2.9 or higher recommended)
-   A target host (can be `localhost` for simulation, or a remote server/VM).

## Usage
1.  **Clone the repository (or copy this utility's folder).**
2.  **Navigate to the `nightly-apoc-garden-tender` directory.**
3.  **Edit `src/inventory.ini`**: Specify your target host(s) under the `[garden_hosts]` group. For local simulation, `localhost` is sufficient.
    ```ini
    [garden_hosts]
    localhost ansible_connection=local
    # Or for a remote host:
    # your_garden_server_ip ansible_user=your_user ansible_ssh_private_key_file=~/.ssh/id_rsa
    ```
4.  **Run the playbook**: 
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

## Configuration
You can override variables by passing them via the command line (`-e "key=value"`) or by creating a `vars.yml` file and including it.

Key variables:
-   `garden_base_dir`: The base directory where garden files will be managed (default: `/tmp/apoc_garden`).
-   `simulated_soil_moisture`: An integer representing current soil moisture (0-100). Default: `50`.
-   `simulated_temperature`: An integer representing current temperature (Celsius). Default: `20`.
-   `moisture_threshold_low`: Below this, watering is triggered (default: `30`).
-   `temp_threshold_high`: Above this, a heat warning is issued (default: `30`).

Example with custom variables:
```bash
ansible-playbook -i src/inventory.ini src/playbook.yml -e "simulated_soil_moisture=25 simulated_temperature=35"
```

## Output
After running, check the `garden_base_dir` (default: `/tmp/apoc_garden`) for:
-   `sensor_data.log`: Simulated raw sensor readings.
-   `garden_log.txt`: A log of actions taken (watering, fertilizing).
-   `garden_report.txt`: The final summary report.

## Testing
To run the automated tests, use the provided test playbook:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_playbook.yml
```
This will run the main playbook with various simulated conditions and assert the expected outcomes.
