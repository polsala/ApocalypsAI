# nightly-radiation-exposure-calculator

Calculate cumulative radiation dose from a list of exposure events.

## Usage

```sh
# Pipe CSV data via stdin
cat exposures.csv | cargo run --quiet

# Or pass a file path as the first argument
cargo run -- exposures.csv
```

**CSV format** (no header, each line):
```
<duration_minutes>,<intensity_mSv_per_h>
```
- `duration_minutes`: length of the exposure event in minutes.
- `intensity_mSv_per_h`: radiation intensity in millisieverts per hour.

The program prints the total dose in mSv and emits a warning if the dose exceeds the safe threshold of **100 mSv**.

## Build

```sh
cargo build --release
```

## Tests

```sh
cargo test
```

## Example

```text
# exposures.csv
30,2.5
45,1.8
120,0.9
```

Running the tool:
```
$ cargo run -- exposures.csv
Total dose: 3.150 mSv
```
