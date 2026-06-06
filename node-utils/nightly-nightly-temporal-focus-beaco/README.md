# Nightly Temporal Focus Beacon

## Overview

The `nightly-temporal-focus-beacon` is a whimsical, CLI-based Pomodoro timer designed to help survivors maintain focus amidst the digital chaos of the apocalypse. It guides you through work and break intervals with encouraging, themed messages, ensuring your neural pathways remain optimized for survival tasks.

## Features

*   **Configurable Timers**: Set custom durations for work and break sessions.
*   **Whimsical Messages**: Enjoy unique, apocalypse-themed prompts for each phase.
*   **Simple CLI Interface**: Easy to use and integrate into your daily workflow.

## Installation

1.  Navigate to the `node-utils/nightly-temporal-focus-beacon` directory.
2.  This utility is dependency-free, so no `npm install` is strictly required for its core functionality. However, for development and testing, you might use `npm test`.

## Usage

Run the utility from your terminal using Node.js:

```bash
node src/index.js [options]
```

### Options:

*   `-w, --work <minutes>`: Duration of the work session in minutes (default: 25).
*   `-b, --break <minutes>`: Duration of the short break session in minutes (default: 5).
*   `-l, --long-break <minutes>`: Duration of the long break session in minutes (default: 15).
*   `-c, --cycles <number>`: Number of work/short-break cycles before a long break (default: 4).
*   `-h, --help`: Display help information.

### Examples:

Start with default settings (25 min work, 5 min break, 4 cycles):

```bash
node src/index.js
```

Start with custom durations (40 min work, 10 min break):

```bash
node src/index.js --work 40 --break 10
```

Start with 2 cycles before a long break:

```bash
node src/index.js -c 2
```

## Whimsical Messages

Here are some examples of the messages you might encounter:

*   **Work Start**: "The void demands your attention! Focus, survivor!"
*   **Work End**: "Your temporal focus has stabilized. Time for a brief respite from the data storms."
*   **Break Start**: "Seek solace in the quiet hum of the server racks. Recharge your neural pathways."
*   **Break End**: "The temporal currents shift. Return to your duties, for the digital wasteland awaits."
*   **Long Break Start**: "A longer temporal distortion detected. Indulge in extended recalibration, survivor."

## Development

To run tests (using the self-contained test runner):

```bash
node tests/index.test.js
```

## License

MIT
