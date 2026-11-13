# Nightly Cron Whisperer

"Listen closely, for the temporal echoes of your scheduled tasks hold secrets..."

The `Nightly Cron Whisperer` is a whimsical utility designed to peek into your system's cron jobs and interpret their "mood" or "purpose" with a touch of apocalyptic charm. Instead of just listing mundane commands, it assigns a "whisper" to each job, helping you understand its role in the grand temporal tapestry of your system.

## Features

- **Cron Job Interpretation**: Scans your user's cron jobs and assigns a descriptive "whisper" based on keywords in the command.
- **Temporal Anomaly Detection**: Highlights hyper-frequent jobs as "Hyper-Vigilant Sentinels".
- **Simple & Self-Contained**: A pure Bash script, easy to run and understand.

## Whispers You Might Hear

- **Guardian of the Archives**: For backup, sync, or archive tasks.
- **Wasteland Scavenger**: For cleanup, removal, or deletion tasks.
- **Temporal Harmonizer**: For system updates or upgrades.
- **System's Slumber**: For reboot or shutdown commands.
- **Silent Observer**: For monitoring or logging tasks.
- **Hyper-Vigilant Sentinel**: For jobs running every minute (`* * * * *`).
- **Mysterious Routine**: For anything else, hinting at unknown temporal machinations.

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd bash-utils/nightly-cron-whisperer
    ```

2.  **Make the script executable**:
    ```bash
    chmod +x src/cron_whisperer.sh
    ```

3.  **Run the whisperer**:
    ```bash
    ./src/cron_whisperer.sh
    ```

    The output will list your cron jobs along with their assigned whispers:

    ```
    --- Nightly Cron Whisperer ---
    Listening to the temporal echoes of your scheduled tasks...

      - Schedule: 0 0 * * *
        Command:  /usr/local/bin/backup_data.sh
        Whisper:  Guardian of the Archives

      - Schedule: */1 * * * *
        Command:  /usr/bin/check_heartbeat.sh
        Whisper:  Hyper-Vigilant Sentinel (Mysterious Routine)

    --- End of Whispers ---
    Total active cron jobs analyzed: 2
    ```

## Development & Testing

To run the tests:

1.  **Navigate to the utility directory**:
    ```bash
    cd bash-utils/nightly-cron-whisperer
    ```

2.  **Make the test script executable**:
    ```bash
    chmod +x tests/test_cron_whisperer.sh
    ```

3.  **Execute the tests**:
    ```bash
    ./tests/test_cron_whisperer.sh
    ```

The tests use a mocked `crontab` command to ensure deterministic and offline execution, verifying that the script correctly interprets various cron job scenarios.
