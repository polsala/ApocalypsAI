# Nightly Cosmic Calendar Converter

A whimsical utility for the ApocalypsAI community that converts Earth dates into a unique "Cosmic Calendar" format and vice-versa. Track your days not by mundane Gregorian cycles, but by the grand celestial events and cosmic phenomena that truly matter in a post-apocalyptic existence!

## 🌌 The Cosmic Calendar System

The Cosmic Calendar operates on a fixed cycle, independent of Earth's irregular leap years, providing a stable temporal anchor in an unstable reality.

*   **Cosmic Epoch:** The calendar begins on Earth's **January 1, 2000 UTC**.
*   **Cosmic Year:** Consists of exactly **365 Earth days**.
*   **Cosmic Phases:** Each Cosmic Year is divided into 13 distinct phases, each with a specific duration:
    1.  **Phase of the Nebula Bloom** (30 days)
    2.  **Phase of the Void Gaze** (30 days)
    3.  **Phase of the Stellar Drift** (30 days)
    4.  **Phase of the Comet's Kiss** (30 days)
    5.  **Phase of the Dark Matter Harvest** (30 days)
    6.  **Phase of the Galactic Whisper** (30 days)
    7.  **Phase of the Quantum Ripple** (30 days)
    8.  **Phase of the Echoing Singularity** (30 days)
    9.  **Phase of the Celestial Alignment** (30 days)
    10. **Phase of the Cosmic Dustfall** (30 days)
    11. **Phase of the Event Horizon** (30 days)
    12. **Phase of the Astral Rebirth** (30 days)
    13. **Interstellar Drift** (5 days) - The final, short phase of contemplation before the next Cosmic Year.

## ✨ Features

*   **Earth to Cosmic Conversion:** Input a standard `YYYY-MM-DD` Earth date and receive its Cosmic Year, Phase, and Cycle.
*   **Cosmic to Earth Conversion:** Input a Cosmic Year, Phase name, and Cycle to get the corresponding Earth date.
*   **Type-Safe:** Built with TypeScript for robust and predictable date handling.

## 🚀 Installation

1.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-cosmic-calendar
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    # or
    yarn build
    ```

## 🛠️ Usage

The utility can be run directly using `ts-node` or after building with `node`. For convenience, you can use the `npm start` script or the `cosmic-calendar` binary after building.

### Convert Earth Date to Cosmic Date

```bash
# Using npm start (requires ts-node)
npm start earth-to-cosmic <YYYY-MM-DD>

# Or using the built binary
./dist/cli.js earth-to-cosmic <YYYY-MM-DD>
```

**Example:**
```bash
npm start earth-to-cosmic 2024-04-23
# Output:
# Earth Date: 2024-04-23
# Cosmic Date: Cosmic Year 25, Phase of the Nebula Bloom, Cycle 13
```

### Convert Cosmic Date to Earth Date

```bash
# Using npm start (requires ts-node)
npm start cosmic-to-earth <cosmicYear> <phaseName> <cycle>

# Or using the built binary
./dist/cli.js cosmic-to-earth <cosmicYear> <phaseName> <cycle>
```

**Example:**
```bash
npm start cosmic-to-earth 25 "Nebula Bloom" 13
# Output:
# Cosmic Date: Cosmic Year 25, Phase of the Nebula Bloom, Cycle 13
# Earth Date: 2024-04-23
```

**Available Cosmic Phase Names (case-insensitive):**
*   `Nebula Bloom`
*   `Void Gaze`
*   `Stellar Drift`
*   `Comet's Kiss`
*   `Dark Matter Harvest`
*   `Galactic Whisper`
*   `Quantum Ripple`
*   `Echoing Singularity`
*   `Celestial Alignment`
*   `Cosmic Dustfall`
*   `Event Horizon`
*   `Astral Rebirth`
*   `Interstellar Drift`

## 🧪 Testing

To run the automated tests:

```bash
npm test
# or
yarn test
```

The tests are deterministic and self-contained, ensuring the conversion logic works as expected without external dependencies or network calls.
