# Nightly Beacon Network Synchronizer

In the desolate expanse of the post-apocalyptic world, reliable communication is the lifeline that connects scattered outposts and ensures the survival of our community. The `nightly-beacon-sync` utility is an Ansible playbook designed to maintain the temporal integrity and operational readiness of our vital communication beacon network.

This playbook performs critical tasks:
1.  **Temporal Drift Correction**: Synchronizes the system clock of each beacon with a reliable time source, preventing temporal anomalies that could disrupt coordinated efforts.
2.  **Signal Emitter Activation**: Ensures the primary "Beacon Signal Emitter" service is running and enabled, guaranteeing continuous signal broadcast.
3.  **Signal Integrity Check**: Verifies the presence of the beacon's signal log, a crucial indicator of its operational health.

Keep your beacons humming and your messages flowing!

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your beacon hosts (or `ansible_connection=local` for localhost testing).
*   Python installed on your beacon hosts (for Ansible's remote modules).

### Inventory

Create an `inventory.ini` file listing your beacon hosts. For local testing, you can use `localhost`:

```ini
[beacons]
beacon1.example.com
beacon2.example.com

# For local testing:
# localhost ansible_connection=local
```

### Variables

The playbook uses variables defined in `vars/main.yml`. You can override these via `--extra-vars` or by creating a `group_vars/beacons.yml` file.

*   `ntp_server`: The NTP server to use for time synchronization (default: `pool.ntp.org`).
*   `beacon_service_name`: The name of the beacon's signal emitter service (default: `beacon_signal_emitter`).

### Running the Playbook

To synchronize your beacon network, execute the playbook:

```bash
ansible-playbook -i inventory.ini beacon_sync.yml
```

To run with specific variables:

```bash
ansible-playbook -i inventory.ini beacon_sync.yml --extra-vars "ntp_server=time.nist.gov beacon_service_name=my_custom_beacon"
```

## Development and Testing

### Local Testing

The `tests/test_beacon_sync.yml` playbook, combined with `tests/run_tests.sh`, provides a self-contained way to test the utility locally without actual remote hosts. It mocks the necessary system states.

To run tests:

```bash
cd nightly-beacon-sync
./tests/run_tests.sh
```

This script will:
1.  Ensure Ansible is installed.
2.  Execute the `test_beacon_sync.yml` playbook against `localhost`.
3.  The `test_beacon_sync.yml` playbook itself handles:
    *   Creating a temporary directory to simulate beacon system paths (`/etc`, `/var/log`).
    *   Creating mock service files and log files within this temporary structure.
    *   Mocking the `ntpdate` command and Ansible's service manager path to operate within the temporary environment.
    *   Running the main `beacon_sync.yml` playbook.
    *   Cleaning up the temporary directory upon completion.
4.  Verify the playbook's successful execution via its exit code.
