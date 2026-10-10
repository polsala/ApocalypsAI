# Nightly Chrono-Compass

A whimsical CLI tool that offers a "temporal direction" and a small, themed activity based on the current time and day. In the ever-shifting sands of the apocalypse, sometimes a little guidance on *when* to focus can make all the difference.

## Features

*   **Temporal Guidance**: Get a suggestion to focus on the Past, Present, or Future.
*   **Themed Activities**: Receive a small, context-appropriate task or thought.
*   **Time-Aware**: Suggestions adapt based on the hour of the day and day of the week.
*   **Cross-Platform**: Built with Node.js, runs anywhere Node is installed.

## Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-chrono-compass
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Make it globally accessible (optional)**:
    ```bash
    npm link
    ```
    Now you can run `chrono-compass` from any directory.

## Usage

Simply run the command:

```bash
chrono-compass
```

The output will be a temporal direction and an activity, for example:

```
🧭 Nightly Chrono-Compass 🧭

It's a Tuesday afternoon.
Your temporal direction: Live in the Present.
Suggested activity: Tend to your immediate surroundings.
```

### Options (for testing and future expansion)

*   `--hour <HH>`: Specify an hour (0-23) to get a suggestion for a different time.
*   `--day <day_name>`: Specify a day (e.g., "Monday", "Sunday") to get a suggestion for a different day.

## Development

To run tests:

```bash
npm test
```

## Contributing

Feel free to open issues or submit pull requests. Temporal anomalies are always welcome for discussion.

## License

MIT
