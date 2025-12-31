## Temporal Sync Agent

This utility ensures your local system clock is synchronized with a reliable Network Time Protocol (NTP) server. In the chaotic aftermath, maintaining accurate time is crucial for coordinating efforts, logging events, and ensuring the smooth operation of any remaining infrastructure.

### Features

*   **NTP Synchronization**: Connects to a specified NTP server to fetch accurate time.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **Configurable**: Allows specifying the NTP server and update interval.
*   **Error Handling**: Gracefully handles network issues and NTP server unavailability.

### Installation

1.  Ensure you have Node.js and npm/yarn installed.
2.  Clone this repository or download the utility files.
3.  Navigate to the `utils/nightly-temporal-sync-agent` directory.
4.  Run `npm install` or `yarn install` to install dependencies.

### Usage

Run the agent from your terminal:

```bash
npx ts-node src/main.ts
```

**Configuration**: The agent can be configured via environment variables or a `config.json` file (if you choose to implement that). By default, it uses `pool.ntp.org` and updates every hour.

**Example with environment variables**:

```bash
NTP_SERVER=time.google.com UPDATE_INTERVAL_MS=3600000 node src/main.ts
```

### Development & Testing

*   **Dependencies**: `typescript`, `ts-node`, `@types/node`, `ntp-client` (or a similar NTP library).
*   **Running Tests**: `npm test` or `yarn test`.

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
