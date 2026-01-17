# Nightly Water Purifier

**Nightly Water Purifier** is a tiny Go command‑line utility that helps post‑apocalypse survivors decide how to treat a water source.

## Features

- Accepts three common water‑quality metrics: pH, turbidity (NTU), and coliform count (CFU/100 mL).
- Returns a concise list of recommended purification steps (filter, boil, chemical, UV).
- Zero external dependencies – just the Go standard library.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-water-purifier

# Build the binary
go build -o water-purifier ./src/main.go
```

## Usage

```bash
./water-purifier -ph=7.2 -turbidity=12 -coliform=5
```

The program will output something like:

```
Recommended purification steps:
- Filter (remove particulates)
- Boil (kill microbes)
```

## Flags

- `-ph` (float, required) – measured pH of the water.
- `-turbidity` (float, required) – turbidity in NTU (nephelometric turbidity units).
- `-coliform` (int, required) – coliform bacteria count per 100 mL.

## Testing

Run the unit tests with:

```bash
go test ./tests/...
```

## License

MIT © ApocalypsAI
