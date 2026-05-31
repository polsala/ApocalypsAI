# Nightly Temporal Ration Rot Reporter (NTRRR)

The apocalypse is tough, but spoiled food doesn't have to be part of the challenge! The Nightly Temporal Ration Rot Reporter is a whimsical-yet-useful command-line utility designed to help you keep track of your perishable survival rations. Add items with their expiration dates, and NTRRR will tell you their "rot level" – from "Fresh as a Daisy" to "Biohazard!" – so you can prioritize consumption and avoid unnecessary waste.

## Features

*   **Add Rations**: Easily add new perishable items with their name, quantity, and expiration date.
*   **Rot Level Reporting**: Get a clear, color-coded report of all your rations, indicating their freshness.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  Ensure you have Node.js and npm (or yarn) installed.
2.  Navigate to the `typescript-utils/nightly-temporal-ration-rot-report` directory.
3.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the utility using `node dist/index.js` followed by commands.

### Add a Ration

```bash
node dist/index.js add <name> <expiry-date> <quantity>
```

*   `<name>`: The name of the ration (e.g., "Canned Peaches", "MRE Pack").
*   `<expiry-date>`: The expiration date in `YYYY-MM-DD` format.
*   `<quantity>`: The number of units of this ration.

**Example:**
```bash
node dist/index.js add "Survival Biscuits" "2024-12-31" 10
node dist/index.js add "Dehydrated Veggies" "2025-01-15" 5
```

### Report on Rations

```bash
node dist/index.js report
```

This command will list all stored rations and their current "rot level".

**Example Output:**
```
--- Ration Rot Report (Current Date: 2024-07-20) ---
[Fresh as a Daisy] Survival Biscuits (x10) - Expires: 2024-12-31 (164 days left)
[Slightly Wilted] Dehydrated Veggies (x5) - Expires: 2025-01-15 (179 days left)
[Impending Doom!] Mystery Meat Can (x2) - Expires: 2024-07-25 (5 days left)
[Biohazard!] Ancient Fruit Roll-up (x1) - Expires: 2024-07-19 (EXPIRED!)
```

## Development

To run tests:
```bash
npm test
# or yarn test
```
