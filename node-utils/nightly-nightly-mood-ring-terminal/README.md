# Nightly Mood Ring Terminal

A whimsical CLI tool that analyzes log files for keywords and displays a "mood" with corresponding terminal colors. Ever wondered if your system logs are feeling "happy" or "anxious"? The Mood Ring Terminal will tell you!

## Features

*   **Mood Detection**: Scans log files for predefined keywords to determine the overall "mood" of your system's activity.
*   **Color-Coded Output**: Displays the detected mood using vibrant ANSI terminal colors (Red for Angry, Yellow for Anxious, Green for Happy, Blue for Calm, Magenta for Mysterious).
*   **Simple CLI**: Easy to use with a single command and a log file path.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js is supported.

## Moods

The utility detects the following moods based on keyword frequency:

*   **🔴 Angry**: Indicates critical errors, failures, panics, or denied access.
*   **🟡 Anxious**: Suggests warnings, timeouts, retries, or pending operations.
*   **🟢 Happy**: Signifies successful operations, completions, deployments, or healthy states.
*   **🔵 Calm**: Represents normal information, status checks, or idle periods.
*   **🟣 Mysterious**: For logs with very mixed signals, unknown anomalies, or ambiguous content.

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher recommended) to run this utility.
    You can download it from [nodejs.org](https://nodejs.org/).

2.  **Clone the repository (or copy the utility folder)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-mood-ring-terminal
    ```

3.  **Install dependencies**:
    ```bash
    npm install
    ```

4.  **Make the script executable (optional, but recommended for direct use)**:
    ```bash
    chmod +x src/mood-ring.js
    ```

## Usage

Run the `mood-ring` command followed by the path to your log file:

```bash
./src/mood-ring.js <path-to-your-log-file>
```

**Example:**

```bash
# Create a sample log file
echo "INFO: System started. All good." > system.log
echo "WARNING: Disk space low." >> system.log
echo "ERROR: Database connection failed." >> system.log
echo "INFO: User 'admin' logged in." >> system.log
echo "SUCCESS: Backup completed." >> system.log

# Check the mood of the system.log
./src/mood-ring.js system.log
```

**Expected Output (example, colors will vary based on dominant mood):**

```
Mood Ring Terminal: A nervous energy hums through the data streams.
```
*(The actual color would be yellow if 'WARNING' is dominant, or red if 'ERROR' is dominant, or magenta if mixed)*

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use mocked file system operations to ensure determinism and offline execution.
