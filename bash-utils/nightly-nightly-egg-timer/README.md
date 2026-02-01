# nightly-egg-timer

Convert human‑friendly duration strings (e.g. `1h30m`, `45s`) into total seconds. Optionally display a celebratory ASCII egg cracking when the timer would finish.

## Usage

```sh
./egg-timer.sh 1h30m
# => 5400

./egg-timer.sh --egg 10s
# => 10
# (egg art)
```

## Options

- `--egg` Show egg art after printing the total seconds.

## Supported units

- `h` – hours
- `m` – minutes
- `s` – seconds

The script ignores any characters that are not part of a `<number><unit>` pair, allowing inputs like `2h15m30s` or `1h 20m`.
