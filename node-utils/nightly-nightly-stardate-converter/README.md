# Nightly Stardate Converter

Converts Earth dates to a whimsical "Stardate" format based on a customizable epoch. Perfect for role-playing, creative writing, or just adding a touch of cosmic flair to your logs and projects.

## Features

*   Convert any valid Earth date string to a Stardate.
*   Customize the epoch (the Earth date corresponding to Stardate 0.0).
*   Customize the base Stardate (the starting Stardate value at the epoch).
*   Simple CLI interface.

## Installation

1.  **Navigate to the `node-utils` directory:**
    ```bash
    cd node-utils/nightly-stardate-converter
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Make the utility executable (optional, for global access):**
    ```bash
    npm link
    # Now you can run `stardate-converter` from anywhere
    ```

## Usage

The utility can be run directly using `node` or via the `stardate-converter` command if linked.

```bash
# Basic conversion using default epoch (2000-01-01) and base (40000.0)
node src/index.js "2024-07-21"
# Or if linked:
stardate-converter "2024-07-21"

# Example Output:
# Earth Date: 2024-07-21
# Stardate: 49023.00
```

### Options

*   `-e, --epoch <date>`: Specify a custom epoch date (e.g., "1966-09-08" for Star Trek's original air date). Defaults to "2000-01-01".
*   `-b, --base <number>`: Specify a custom base Stardate. Defaults to 40000.0.

```bash
# Convert a date using a custom epoch and base Stardate
stardate-converter "2024-07-21" --epoch "1966-09-08" --base 10000.0

# Example Output:
# Earth Date: 2024-07-21
# Stardate: 21107.00
```

### Supported Date Formats

The utility uses JavaScript's `Date` object parsing, which generally supports:
*   `YYYY-MM-DD` (e.g., "2024-07-21")
*   `MM/DD/YYYY` (e.g., "07/21/2024")
*   `Month Day, Year` (e.g., "July 21, 2024")
*   And other ISO 8601 compatible strings.

## Development

### Running Tests

```bash
npm test
# Or directly:
node tests/index.test.js
```

## License

This project is licensed under the MIT License.
