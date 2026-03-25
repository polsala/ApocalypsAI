# Nightly Chrono-Snooze Scheduler

A whimsical-yet-useful CLI tool for scheduling optimal short 'chrono-snooze' cycles (power naps) to recharge your temporal energies. It calculates your wake-up time and provides a unique, encouraging message to help you re-enter the current timeline refreshed.

## Features

*   **Optimal Nap Durations**: Choose from predefined 'power', 'light', or 'full' snooze cycles.
*   **Custom Durations**: Specify your own snooze length in minutes.
*   **Whimsical Wake-Up Messages**: Get a unique, apocalypse-themed message to greet you back to reality.
*   **Cross-Platform**: Runs wherever Node.js is supported.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Clone the repository or download the utility:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-chrono-snooze-sched
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  (Optional) Make it globally accessible:
    ```bash
    npm link
    # Or add an alias to your shell config (e.g., ~/.bashrc, ~/.zshrc)
    # alias snooze="node /path/to/ApocalypsAI/node-utils/nightly-chrono-snooze-sched/src/index.js"
    ```

## Usage

Run the utility from your terminal. It will output your calculated wake-up time and a message. You'll need to set a separate alarm on your device for the actual wake-up.

```bash
node src/index.js [options]
```

### Options

*   `--type <cycle>`: Specify a predefined snooze cycle. Valid types: `power` (20-25 min), `light` (45-50 min), `full` (90-100 min). Default is `power`.
*   `--duration <minutes>`: Specify a custom snooze duration in minutes. Overrides `--type`.

### Examples

*   **Default power nap (20 minutes):**
    ```bash
    node src/index.js
    # Output: Initiating a Power Chrono-Snooze...
    #          Current time: 2023-10-27 10:00:00
    #          Wake-up time: 2023-10-27 10:20:00
    #          Message: The temporal currents have been recalibrated. Rise, survivor, and seize the fleeting present!
    ```

*   **Light snooze (45 minutes):**
    ```bash
    node src/index.js --type light
    # Output: Initiating a Light Chrono-Snooze...
    #          Current time: 2023-10-27 10:00:00
    #          Wake-up time: 2023-10-27 10:45:00
    #          Message: A brief journey through the ether concludes. Your mind is now a sharper blade against the encroaching void.
    ```

*   **Custom 30-minute snooze:**
    ```bash
    node src/index.js --duration 30
    # Output: Initiating a Custom Chrono-Snooze (30 minutes)...
    #          Current time: 2023-10-27 10:00:00
    #          Wake-up time: 2023-10-27 10:30:00
    #          Message: The fabric of time bends to your will. Awaken, for destiny awaits your refreshed gaze.
    ```

## Development

To run tests:

```bash
npm test
```
