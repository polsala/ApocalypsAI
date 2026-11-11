# Nightly Cosmic Calendar Converter

This utility transforms standard Earth dates (YYYY-MM-DD) into a whimsical 'Cosmic Calendar' format. It assigns each date a unique combination of a Stellar Cycle, Lunar Phase, and Galactic Era, offering a fresh, imaginative perspective on time.

## Features

*   **Stellar Cycles**: Represents the larger cosmic influences based on the Earth year.
*   **Lunar Phases**: Maps the day of the year to a specific lunar phase, adding a celestial rhythm.
*   **Galactic Eras**: Categorizes centuries into grand cosmic epochs.
*   **Type-Safe**: Built with TypeScript for robust date handling and predictable output.

## Installation

To use this utility, you need Node.js (which includes npm) and TypeScript installed.

1.  Navigate to the utility's directory:
    ```bash
    cd nightly-cosmic-calendar-conv
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the utility from your terminal, providing an Earth date in `YYYY-MM-DD` format:

```bash
npm start <YYYY-MM-DD>
```

### Examples

Convert today's date (e.g., 2023-10-27):
```bash
npm start 2023-10-27
```

Output:
```
🔭 Celestial Alignment, 🌖 Waning Gibbous's Reflection, Cosmic Day 300 (Day 300 of the Celestial Alignment), within the Era of the Great Silence.
```

Convert a date in a different year:
```bash
npm start 2024-03-10
```

Output:
```
✨ Nebula's Embrace, 🌒 Waxing Crescent's Hope, Cosmic Day 70 (Day 70 of the Nebula's Embrace), within the Era of the Great Silence.
```

Convert a date far in the future:
```bash
npm start 2250-07-15
```

Output:
```
✨ Nebula's Embrace, 🌕 Full Moon's Radiance, Cosmic Day 196 (Day 196 of the Nebula's Embrace), within the Era of the Void's Awakening.
```

## Development

### Running Tests

```bash
npm test
```

### Building the Project

```bash
npm run build
```
