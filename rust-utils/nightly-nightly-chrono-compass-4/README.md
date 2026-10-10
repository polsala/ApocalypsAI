# Nightly Chrono-Compass

A high-performance CLI tool crafted in Rust to measure the 'temporal distance' between two specified timestamps. Beyond standard days, hours, and minutes, it quantifies this distance in 'Flickers of Eternity', offering a whimsical yet precise perspective on time.

## Features

*   **Precise Temporal Measurement**: Calculate duration between two points in time.
*   **Whimsical Units**: Expresses time in 'Flickers of Eternity' (where 1 Flicker = 1 minute).
*   **Flexible Input**: Accepts various ISO 8601 and common `YYYY-MM-DD HH:MM:SS` timestamp formats.
*   **Error Handling**: Provides clear messages for invalid inputs or temporal paradoxes (end time before start time).

## Installation

To use the Nightly Chrono-Compass, you'll need [Rust](https://www.rust-lang.org/tools/install) installed.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-compass
    ```

2.  **Build the utility:**
    ```bash
    cargo build --release
    ```

3.  **The executable will be located at `target/release/nightly-chrono-compass`.**

## Usage

Run the utility from the command line, providing the start and end timestamps using the `-s` or `--start-time` and `-e` or `--end-time` flags.

```bash
./target/release/nightly-chrono-compass --start-time "YYYY-MM-DDTHH:MM:SSZ" --end-time "YYYY-MM-DDTHH:MM:SSZ"
```

### Examples

1.  **Calculate the distance between two ISO 8601 timestamps:**
    ```bash
    ./target/release/nightly-chrono-compass -s "2023-01-01T10:00:00Z" -e "2023-01-02T11:30:00Z"
    ```
    **Expected Output:**
    ```
    Temporal Distance: 1 days, 1 hours, 30 minutes
    Which is approximately 1530 Flickers of Eternity (1 Flicker = 1 minute)
    ```

2.  **Using space-separated UTC timestamps:**
    ```bash
    ./target/release/nightly-chrono-compass -s "2023-01-01 10:00:00 UTC" -e "2023-01-01 12:00:00 UTC"
    ```
    **Expected Output:**
    ```
    Temporal Distance: 0 days, 2 hours, 0 minutes
    Which is approximately 120 Flickers of Eternity (1 Flicker = 1 minute)
    ```

3.  **Using timestamps without explicit timezone (assumed UTC):**
    ```bash
    ./target/release/nightly-chrono-compass -s "2023-01-01 10:00:00" -e "2023-01-01 10:05:00"
    ```
    **Expected Output:**
    ```
    Temporal Distance: 0 days, 0 hours, 5 minutes
    Which is approximately 5 Flickers of Eternity (1 Flicker = 1 minute)
    ```

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
cargo test
```

### Dependencies

*   `clap`: For robust command-line argument parsing.
*   `chrono`: For powerful and accurate date and time manipulation.
