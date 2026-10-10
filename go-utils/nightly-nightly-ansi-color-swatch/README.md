# nightly-ansi-color-swatch

Utility that prints a visual swatch of all 256 ANSI background colors in your terminal. Helpful for developers to pick colors for terminal applications.

## Usage

```sh
go run src/main.go
```

Or build and run:

```sh
go build -o ansi-swatch src/main.go
./ansi-swatch
```

The output displays each color code with a colored block.

## How it works

The program iterates over color codes 0‑255 and prints each code with its background set using the ANSI escape sequence `\x1b[48;5;<code>m`. After each line, it resets formatting.

## License

MIT
