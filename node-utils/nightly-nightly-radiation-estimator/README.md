# nightly-radiation-estimator

A whimsical CLI utility that helps post‑apocalyptic wanderers estimate their cumulative radiation exposure.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js --distance <km> --time <hours> --rate <µSv/h>
```

- `--distance` distance traveled (km) – currently for flavor only.
- `--time` time spent in the radiation zone (hours).
- `--rate` ambient radiation rate in microsieverts per hour.

The tool prints the total dose and warns if it exceeds the daily safe limit of 100 µSv.

## Example

```sh
node src/index.js --distance 12 --time 3 --rate 0.8
```

Output:

```
Total dose: 2.4 µSv
Status: Safe (below 100 µSv)
```

## License

MIT
