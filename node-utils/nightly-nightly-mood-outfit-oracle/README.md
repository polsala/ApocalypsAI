# Nightly Mood-Matching Outfit Oracle

A whimsical utility for the discerning post-apocalyptic survivor, helping you choose your daily ensemble based on your desired mood and the ever-unpredictable wasteland weather. No more fashion faux pas when facing irradiated drizzle or a solar flare advisory!

## Features

*   **Mood-Based Styling**: Select from moods like `resilient`, `mysterious`, `optimistic`, `daring`, or `calm`.
*   **Weather-Adjusted Attire**: Get recommendations tailored to `ashfall`, `irradiated drizzle`, `solar flare advisory`, `whispering winds`, or `clear skies`.
*   **CLI Interface**: Quick and easy to use from your terminal.

## Installation

1.  Navigate to the `node-utils/nightly-mood-outfit-oracle` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal, providing a mood and a weather condition:

```bash
node src/index.js <mood> <weather>
```

### Examples:

To project an aura of resilience during an ashfall:
```bash
node src/index.js resilient ashfall
```

To embrace your mysterious side during an irradiated drizzle:
```bash
node src/index.js mysterious "irradiated drizzle"
```

To stay optimistic under clear skies:
```bash
node src/index.js optimistic "clear skies"
```

### Available Moods:

*   `resilient`
*   `mysterious`
*   `optimistic`
*   `daring`
*   `calm`

### Available Weather Conditions:

*   `ashfall`
*   `irradiated drizzle`
*   `solar flare advisory`
*   `whispering winds`
*   `clear skies`

## Development & Testing

To run the tests:

```bash
npm test
```
