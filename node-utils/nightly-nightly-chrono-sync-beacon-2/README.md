# Nightly Chrono-Sync Beacon

A Node.js CLI utility designed to help synchronize your local system time with a reliable (albeit simulated for safety and determinism) external time source, with an optional "temporal distortion" offset. In the chaotic aftermath, maintaining accurate time is crucial for logging, security, and coordinating efforts. This beacon helps you stay on schedule, even when reality itself seems to warp.

## Features

*   **Time Synchronization Check**: Compares local system time against a simulated external time source.
*   **Temporal Distortion Offset**: Apply a configurable offset (e.g., `+5s`, `-10m`, `+1h`) to the external time to simulate various temporal anomalies or adjust for known regional time drifts.
*   **Synchronization Recommendation**: Provides a `sudo date -s` command suggestion to correct your system time if it's significantly off.
*   **Cross-Platform (Node.js)**: Runs wherever Node.js is supported.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-chrono-sync-beacon
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js [options]
```

### Options

*   `--offset <value>`: Apply a temporal distortion offset to the external time.
    *   `<value>` format: `[+|-]<number>[s|m|h]`
    *   Examples: `+10s` (add 10 seconds), `-5m` (subtract 5 minutes), `+1h` (add 1 hour).

### Examples

1.  **Check time synchronization without any distortion**:
    ```bash
    node src/index.js
    ```
    This will compare your local time against the (mocked) external time and recommend a sync if needed.

2.  **Check time synchronization with a positive temporal distortion of 30 seconds**:
    ```bash
    node src/index.js --offset +30s
    ```
    The external time will be treated as 30 seconds ahead of its actual value for the comparison.

3.  **Check time synchronization with a negative temporal distortion of 5 minutes**:
    ```bash
    node src/index.js --offset -5m
    ```
    The external time will be treated as 5 minutes behind its actual value for the comparison.

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests are deterministic and offline, using mocks for time-related functions and `console.log` to ensure consistent results across different environments and times.

## Mock Rationale

*   **External Time Source**: In a real-world scenario, this utility would connect to an NTP server or a trusted time API. For the purpose of a self-contained, deterministic utility, the `_getExternalTime` function is mocked in tests to return a controlled timestamp. This allows tests to simulate various external time conditions without external network dependencies.
*   **Local System Time**: Similarly, `_getLocalTime` is mocked in tests to simulate different local system clock states, enabling comprehensive testing of the synchronization logic.
*   **`console.log`**: Output is captured during tests to verify the exact messages and commands suggested by the utility.
