# Nightly System Health Check

This utility performs a quick, whimsical system health check. It reports on critical system resources like disk space, memory usage, and running processes, all with a touch of apocalyptic flair.

## Usage

Run the script from your terminal:

```bash
./src/main.sh
```

## Features

*   **Disk Space Check**: Reports on available disk space, with a warning if it's getting low.
*   **Memory Usage**: Shows current memory usage and swap, with a grim outlook if it's high.
*   **Process Count**: Counts the number of running processes, hinting at potential system overload.
*   **Whimsical Output**: Uses themed messages to present the system status.

## Testing

Automated tests are included to ensure the script functions as expected. Run them using `bash tests/test_main.sh`.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or new features. Remember to add tests for any changes!
