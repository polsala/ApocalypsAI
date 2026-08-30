# Nightly Chrono-Compass Calibrator

A high-performance CLI tool written in Rust to help synchronize your temporal devices (clocks, chronometers, time-travel stabilizers) by calculating the average temporal drift based on a series of observed anomalies. In a world where time itself can waver, this utility provides a crucial anchor.

## 🧭 Usage

The `nightly-chrono-compass-calibrator` expects a stream of observations, either from a file or standard input. Each line should represent a single observation in the following comma-separated format:

`ISO8601_TIMESTAMP,OBSERVED_OFFSET_SECONDS`

Where:
*   `ISO8601_TIMESTAMP`: The UTC timestamp when the observation was made (e.g., `2023-10-27T10:00:00Z`).
*   `OBSERVED_OFFSET_SECONDS`: The observed difference between true time and your local clock at that timestamp. A positive value means your local clock is *behind* true time (needs to be advanced), and a negative value means it's *ahead* (needs to be retarded).

### Examples

**1. Calibrating from standard input:**

```bash
echo "2023-10-27T10:00:00Z,15.0\n2023-10-27T11:00:00Z,16.0\n2023-10-27T12:00:00Z,14.5" | nightly-chrono-compass-calibrator
```

**2. Calibrating from a file:**

Create a file named `observations.csv`:
```
2023-10-27T10:00:00Z,15.0
2023-10-27T11:00:00Z,16.0
2023-10-27T12:00:00Z,14.5
```

Then run:
```bash
nightly-chrono-compass-calibrator --file observations.csv
```

## ⚙️ Build and Run

To build this utility, you need Rust installed.

```bash
# Clone the repository (if not already done)
# git clone https://github.com/polsala/ApocalypsAI.git
# cd ApocalypsAI/rust-utils/nightly-chrono-compass-calibrator

# Build the project
cargo build --release

# Run the compiled binary (example using stdin)
echo "2023-10-27T10:00:00Z,15.0" | ./target/release/nightly-chrono-compass-calibrator
```

## 🧪 Tests

To run the tests:

```bash
# From the utility's root directory
cargo test
```

## 🌟 Whimsical Lore

The Chrono-Compass Calibrator is an essential tool for any survivor navigating the fractured timelines of the post-apocalyptic world. Celestial alignments are no longer reliable, and even the hum of the void can subtly shift the local temporal flow. By feeding it observations from ancient atomic clocks, quantum entanglement readings, or even the precise decay rates of exotic isotopes, this compass helps you keep your personal timeline aligned with the universe's true, albeit often chaotic, rhythm. Misalignments can lead to anything from a missed scavenging opportunity to accidentally phasing into a dimension populated entirely by sentient dust bunnies. Stay calibrated, stay safe!
