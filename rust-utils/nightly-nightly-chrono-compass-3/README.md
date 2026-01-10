# Nightly Chrono-Compass

A high-performance CLI tool for calculating temporal differences and tracking apocalyptic deadlines with whimsical flair. For survivors, by survivors.

## 🧭 Overview

In the fractured timelines of the apocalypse, precise temporal tracking is paramount. The `nightly-chrono-compass` helps you navigate the temporal distortions, calculate crucial durations, and countdown to vital events. Whether it's tracking resource respawns, patrol timings, or the next Great Glitch, this compass will keep your temporal bearings true.

## ✨ Features

*   **`until`**: Calculate the time remaining until a specified future date/time.
*   **`since`**: Determine the time elapsed since a specified past date/time.
*   **`between`**: Measure the duration between two arbitrary date/time points.
*   **`countdown`**: Track pre-defined apocalyptic events with themed messages.
*   **Flexible Date/Time Parsing**: Supports RFC3339 (e.g., `2024-12-31T23:59:59Z`), local `YYYY-MM-DD HH:MM:SS`, and `YYYY-MM-DD` formats.
*   **Whimsical Output**: Themed messages to keep spirits high (or appropriately grim) in the face of temporal anomalies.

## 🚀 Installation

### From Crates.io (Recommended)

```bash
cargo install nightly-chrono-compass
```

### From Source

1.  **Clone the repository:**
    ```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chrono-compass
    ```
2.  **Build the project:**
    ```bash
cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-chrono-compass`.** You can move it to a directory in your `PATH` for easy access:
    ```bash
sudo cp target/release/nightly-chrono-compass /usr/local/bin/
    ```

## 💡 Usage

All commands assume UTC for RFC3339 inputs. For `YYYY-MM-DD HH:MM:SS` and `YYYY-MM-DD` formats, your local timezone is used for parsing, then converted to UTC for calculations.

```bash
nightly-chrono-compass --help
```

### Examples:

#### 1. Time Until a Future Event

"How long until the next temporal anomaly?"

```bash
nightly-chrono-compass until "2024-12-31T23:59:59Z"
# Example output (if run on 2024-07-15 12:00:00 UTC):
# Only 5 months, 16 days, 11 hours, 59 minutes, 59 seconds until the next temporal anomaly! Stay vigilant!
```

Using a local time format:
```bash
nightly-chrono-compass until "2024-07-16 00:00:00"
# Example output (if run on 2024-07-15 12:00:00 UTC, assuming local timezone is UTC):
# Only 12 hours until the next temporal anomaly! Stay vigilant!
```

#### 2. Time Since a Past Event

"How long has it been since the Great Glitch?"

```bash
nightly-chrono-compass since "2024-01-01T00:00:00Z"
# Example output (if run on 2024-07-15 12:00:00 UTC):
# It has been 6 months, 14 days, 12 hours since that moment. Time flies, even in the apocalypse.
```

#### 3. Duration Between Two Points

"What's the temporal span between the last supply drop and the next?"

```bash
nightly-chrono-compass between "2024-07-01T00:00:00Z" "2024-07-31T23:59:59Z"
# Example output:
# The temporal span between those points is 30 days, 23 hours, 59 minutes, 59 seconds. A blink in the void.
```

#### 4. Countdown to Apocalyptic Events

"How long until the Resource Resupply?"

```bash
nightly-chrono-compass countdown ResourceResupply
# Example output (if run on 2024-07-15 12:00:00 UTC):
# Countdown to ResourceResupply: 4 days, 20 hours remaining! Prepare for the inevitable.
```

"What about an event that already happened?"
```bash
nightly-chrono-compass countdown FirstAnomaly
# Example output (if run on 2024-07-15 12:00:00 UTC):
# The 'FirstAnomaly' event has already transpired, traveler. It was 5 days, 12 hours ago.
```

"What if I ask about an unknown event?"
```bash
nightly-chrono-compass countdown UnknownRift
# Example output:
# Unknown apocalyptic event: 'UnknownRift'. Perhaps it's a secret timeline?
```

## 🧪 Testing

To run the tests, navigate to the utility's directory and execute:

```bash
cargo test
```

The tests are designed to be deterministic and offline, using a fixed "current" time (2024-07-15 12:00:00 UTC) for all calculations. This ensures consistent results regardless of when the tests are run.

## 🤝 Contributing

Feel free to open issues or submit pull requests if you have ideas for new temporal calculations, whimsical messages, or performance enhancements!
