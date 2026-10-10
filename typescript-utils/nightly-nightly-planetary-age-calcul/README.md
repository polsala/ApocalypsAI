# nightly-planetary-age-calculator

A tiny TypeScript CLI that tells you how old you would be on every planet in the Solar System (including Pluto).  It prints the ages in years with two‑decimal precision and adds a fun emoji for each world.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install dependencies
npm install
```

> The utility has **no external runtime dependencies** beyond Node.js (v14+) and the built‑in `fs`/`path` modules.

## Usage

```bash
# Run the CLI with a birthdate (ISO format: YYYY-MM-DD)
node src/index.js 1990-04-15
```

Example output:

```
🌍 Earth:   33.45 years
☿ Mercury: 138.86 years
♀ Venus:    54.38 years
♂ Mars:     17.78 years
♃ Jupiter:  2.82 years
♄ Saturn:   1.14 years
⛢ Uranus:   0.40 years
♆ Neptune:  0.20 years
♇ Pluto:    0.13 years
```

## How it works

The script parses the supplied birthdate, computes the elapsed seconds up to the current moment (or an optional `--as-of` date), and divides by each planet’s orbital period expressed in Earth years.  The orbital periods are taken from NASA data and are hard‑coded for simplicity.

## Testing

Run the bundled tests with:

```bash
npm test
```

The test suite checks the core calculation function against a known reference date.

## License

MIT – feel free to fork, tweak, and share your interplanetary birthdays!
