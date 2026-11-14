# Nightly System Health Reporter

This utility is a whimsical bash script designed to report the health of your system in a way that's both informative and slightly apocalyptic. It gathers key system metrics and presents them with a touch of flair.

## Features

*   Reports CPU usage.
*   Reports memory usage.
*   Reports disk usage.
*   Reports network interface status.
*   Provides a "survival readiness" score based on these metrics.
*   Uses fun, thematic output messages.

## Usage

Simply run the script from your terminal:

```bash
./nightly-sys-health-reporter.sh
```

## Installation

1.  Clone the repository.
2.  Navigate to the `bash-utils/nightly-sys-health-reporter` directory.
3.  Make the script executable:
    ```bash
    chmod +x src/nightly-sys-health-reporter.sh
    ```

## Tests

Automated tests are included to ensure the script functions as expected. Run them using:

```bash
./tests/run_tests.sh
```
