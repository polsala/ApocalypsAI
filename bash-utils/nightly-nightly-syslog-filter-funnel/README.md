# Nightly Syslog Filter Funnel

This utility is a whimsical yet practical bash script designed to filter and categorize incoming syslog messages. It adds a touch of fun to system administration by tagging messages with playful, context-aware labels before directing them to different output streams or files.

## Features

*   **Real-time Filtering**: Processes syslog messages as they arrive.
*   **Whimsical Tagging**: Assigns fun, descriptive tags based on message content.
*   **Configurable Output**: Directs tagged messages to different standard outputs or files.
*   **Simple to Use**: A straightforward bash script requiring minimal setup.

## Usage

1.  **Make the script executable**: `chmod +x src/main.sh`
2.  **Run the script**: `src/main.sh <input_log_file_or_pipe>`

**Example**: To filter messages from `/var/log/syslog` and send "error" messages to `errors.log` and "warning" messages to `warnings.log`:

```bash
sudo tail -f /var/log/syslog | ./src/main.sh > /dev/null
```

*(Note: The script itself will output to stdout by default. To redirect specific tags, you'd modify the script or pipe its output further. The example above assumes the script is modified to handle specific tag outputs.)*

## Configuration

The script uses simple `if/elif/else` statements to define filtering rules and tags. You can easily modify these within the `src/main.sh` file to suit your needs.

## Testing

Run the tests using the provided `tests/test_main.sh` script.

```bash
./tests/test_main.sh
```
