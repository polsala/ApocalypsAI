# Nightly Radiation Exposure Estimator

Estimates cumulative radiation dose (in millisieverts) from a list of activities. Input is a CSV with three columns:

1. **activity** – a short description (ignored by the calculator)
2. **minutes** – duration of the activity
3. **radiation_mSv_per_hour** – radiation level for that activity

The tool sums the dose for each line using the formula:

```
 dose = (minutes / 60) * radiation_mSv_per_hour
```

## Installation

```sh
# Clone the repository (or copy the utility folder) and build with Cargo
cargo build --release
```

## Usage

You can pipe CSV data into the program or provide a file path as the first argument.

```sh
# Pipe from stdin
cat activities.csv | cargo run --quiet

# Or pass a file name
cargo run --quiet -- activities.csv
```

### Example CSV

```
Scavenging,120,0.5
Radioactive-Repair,30,2.0
```

### Expected Output

```
Total radiation dose: 1.50 mSv
```

## Testing

Run the test suite with:

```sh
cargo test
```

The tests cover basic parsing, handling of malformed lines, and dose calculation.
