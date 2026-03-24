# Nightly Cosmic Configuration Auditor (nightly-cosmic-config-audit)

## Summary
This utility acts as a vigilant sentinel, auditing critical system configuration files against a pre-established baseline of SHA256 checksums. It's designed to detect any unauthorized or accidental modifications, providing an early warning system against cosmic ray-induced bit flips or more mundane human errors.

## Usage

### Prerequisites
- Bash shell
- `sha256sum` utility (standard on most Linux/Unix systems)

### Setup
1.  **Create a configuration file list**: Create a file (e.g., `config_files.txt`) listing the absolute paths of the configuration files you wish to monitor, one path per line.
    ```
    /etc/passwd
    /etc/sudoers
    /etc/ssh/sshd_config
    /etc/fstab
    /etc/nginx/nginx.conf
    ```

2.  **Initialize the baseline**: Run the script with the `init` command to create the initial checksum baseline. This will calculate the SHA256 hash for each file in your list and store it in a designated baseline directory.
    ```bash
    ./src/cosmic_audit.sh init /path/to/your/config_files.txt /path/to/your/baseline_directory
    ```
    Example:
    ```bash
    ./src/cosmic_audit.sh init ./config_files.txt ~/.cosmic_audit_baseline
    ```
    *Note: The baseline directory will be created if it doesn't exist. Ensure it's a secure location.*

### Auditing
Once the baseline is initialized, you can run the audit command to check for changes:

```bash
./src/cosmic_audit.sh audit /path/to/your/config_files.txt /path/to/your/baseline_directory
```
Example:
```bash
./src/cosmic_audit.sh audit ./config_files.txt ~/.cosmic_audit_baseline
```

The script will output the status for each monitored file: `OK`, `CHANGED`, `FILE NOT FOUND`, or `NO BASELINE`.

### Example Output
```
Auditing /etc/passwd... OK
Auditing /etc/sudoers... CHANGED (Current: 1a2b3c..., Baseline: d4e5f6...)
Auditing /etc/ssh/sshd_config... OK
Auditing /etc/fstab... NO BASELINE (Run 'init' to create)
Auditing /nonexistent/file... FILE NOT FOUND (Current system)
```

## Integration
This utility is ideal for daily cron jobs or CI/CD pipelines to ensure configuration integrity across your systems. Schedule it to run regularly and pipe its output to a logging system or alert mechanism to be notified of any deviations. The script exits with status `0` if all files are `OK`, and `1` if any file is `CHANGED`, `FILE NOT FOUND`, or `NO BASELINE`.

## Development
To run tests, navigate to the utility's root directory and execute:
```bash
./tests/test_cosmic_audit.sh
```
