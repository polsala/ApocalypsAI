# Nightly Chrono-Echo CLI

A whimsical-yet-useful command-line utility that captures the output (stdout and stderr) and exit code of any shell command, saving it as a "temporal echo." Later, you can replay this echo, optionally introducing "temporal distortions" like delays or character shifts, or even a ghostly whisper from the past.

## Features

-   **Capture**: Run any command and save its complete output and exit status.
-   **Replay**: Play back the captured command's output as if it were running live.
-   **Temporal Delay**: Introduce a configurable delay before and between stdout/stderr output during replay.
-   **Character Shift Distortion**: Randomly shift a small percentage of alphanumeric characters in the output, simulating data corruption or "temporal static."
-   **Ghost Echo Distortion**: Append a subtle, ethereal message to the output, hinting at past runs.

## Why use it?

-   **Reproducible Demos**: Create consistent demonstrations of CLI tools without needing to run the actual commands repeatedly.
-   **Testing Resilience**: Test how your scripts or tools react to slow-responding commands or slightly corrupted/noisy input.
-   **Simulated Environments**: Mimic external service responses or complex command outputs for CI/CD pipelines or local development.
-   **Whimsical Fun**: Add a touch of temporal anomaly to your daily command-line interactions.

## Installation

This is a Node.js utility. Ensure you have Node.js (v14 or higher) installed.

1.  **Save the files**: Place `src/index.js`, `package.json`, and `README.md` into a directory named `nightly-chrono-echo-cli`.
2.  **Make executable**: 
    ```bash
    chmod +x nightly-chrono-echo-cli/src/index.js
    ```
3.  **Run directly**: You can then run it using `node nightly-chrono-echo-cli/src/index.js` or create a symlink for easier access.

## Usage

### 1. Capture a Command's Echo

To capture the output of a command, use the `--capture` flag and specify the command with `--command`.

```bash
# Capture the output of 'ls -l' and save it to 'my-ls-echo.json'
./src/index.js --capture --command "ls -l" --file my-ls-echo.json

# Capture a simple echo, default file is 'chrono-echo.json'
./src/index.js --capture --command "echo Hello, Chrononauts!"
```

The captured output, including stdout, stderr, and exit code, will be saved to the specified JSON file.

### 2. Replay a Temporal Echo

To replay a previously captured echo, use the `--replay` flag.

```bash
# Replay the default echo
./src/index.js --replay

# Replay a specific echo file
./src/index.js --replay --file my-ls-echo.json
```

### 3. Replay with Temporal Distortions

Add some flair to your replays!

-   **Delay**: Introduce a delay in milliseconds before and between stdout/stderr output.
    ```bash
    ./src/index.js --replay --delay 500 # 500ms delay
    ```
-   **Character Shift**: Randomly shift some alphanumeric characters.
    ```bash
    ./src/index.js --replay --distort shift
    ```
-   **Ghost Echo**: Append a subtle, ghostly message.
    ```bash
    ./src/index.js --replay --distort ghost
    ```
-   **Combine**:
    ```bash
    ./src/index.js --replay --file my-ls-echo.json --delay 200 --distort shift
    ```

## Development & Testing

To run the tests, you'll need `jest`.

1.  **Install dependencies**:
    ```bash
    npm init -y
    npm install --save-dev jest
    ```
2.  **Run tests**:
    ```bash
    npx jest tests/index.test.js
    ```

## Example `chrono-echo.json`

```json
{
  "command": "echo Hello, Chrononauts!",
  "timestamp": "2023-10-27T10:30:00.000Z",
  "stdout": "Hello, Chrononauts!\n",
  "stderr": "",
  "exitCode": 0
}
```
