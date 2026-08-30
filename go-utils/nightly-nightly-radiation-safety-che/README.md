# Nightly Radiation Safety Checker

A whimsical command‑line utility that tells you whether the ambient radiation level is safe for post‑apocalyptic wanderers. It accepts a radiation level in microsieverts per hour (µSv/h) and returns a friendly verdict.

## Build

```sh
go build -o radiation-checker ./src/main.go
```

## Usage

```sh
./radiation-checker 0.3
# Output: 🌿 Radiation level 0.3 µSv/h: Safe. The glow is gentle.
```

If no argument is provided, the tool reads from standard input.

## Safety thresholds

- **Safe**: < 0.5 µSv/h
- **Caution**: 0.5 – 2.0 µSv/h
- **Dangerous**: > 2.0 µSv/h

## License

MIT
