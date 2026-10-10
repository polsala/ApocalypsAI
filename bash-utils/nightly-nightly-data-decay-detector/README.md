# nightly-data-decay-detector

A whimsical bash utility to detect and report on old, potentially decaying files and directories in your digital wasteland. It helps you identify and optionally quarantine digital clutter that has been left untouched for too long, preventing your system from becoming a forgotten ruin.

## Features

*   **Decay Detection**: Scans a specified directory for files and subdirectories older than a configurable number of days.
*   **Reporting**: Lists all identified "decaying" items.
*   **Quarantine Mode**: Optionally moves decaying items to a designated "quarantine" directory, isolating them from active use without immediate deletion.
*   **Whimsical Naming**: Embrace the post-apocalyptic theme for your digital cleanup!

## Usage

### Prerequisites

*   Bash shell
*   `find` utility
*   `mkdir` utility
*   `mv` utility
*   `xargs` utility

These are standard utilities available on most Unix-like systems.

### Basic Scan

To scan your current directory for items older than 90 days (default):

```bash
./src/decay_detector.sh .
```

To scan a specific directory for items older than 180 days:

```bash
./src/decay_detector.sh -a 180 /path/to/your/digital/wasteland
```

### Quarantine Mode

To move items older than 365 days from `/path/to/old_data` to a quarantine directory `/tmp/digital_quarantine`:

```bash
./src/decay_detector.sh -a 365 -q -d /tmp/digital_quarantine /path/to/old_data
```

The quarantine directory will be created if it doesn't exist.

### Options

*   `-a, --age <days>`: Minimum age in days for files/directories to be considered 'decaying'. Default is 90 days.
*   `-q, --quarantine`: Enable quarantine mode. Decaying items will be moved.
*   `-d, --quarantine-dir <path>`: Specifies the directory to move quarantined items to. Required when `-q` is used.
*   `-h, --help`: Display the usage information.

## Development and Testing

### Running Tests

To run the automated tests, navigate to the `tests/` directory and execute the test script:

```bash
cd tests/
./test_decay_detector.sh
```

The tests will create temporary files and directories to simulate different scenarios and verify the script's behavior. They are designed to be deterministic and self-contained.

### Mock Rationale

The tests achieve determinism by creating a controlled temporary filesystem environment. Instead of mocking the `find` command directly, which can be complex in shell scripting, we leverage `touch -d` to precisely set the modification times of files and directories within these temporary structures. This allows the `decay_detector.sh` script to operate on a real, yet fully controlled and predictable, filesystem state, ensuring consistent test results without external dependencies or network calls.
