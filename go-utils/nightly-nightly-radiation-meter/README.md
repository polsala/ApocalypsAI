# Nightly Radiation Meter

A whimsical CLI tool that reports a deterministic "radiation level" for any given location. Useful for post‑apocalyptic role‑playing games or just for fun.

## Installation

```sh
go build -o radiation-meter ./src
```

## Usage

```sh
./radiation-meter "Chernobyl"
# Output: Radiation level at Chernobyl: 433 mSv
```

## How it works

The tool sums the Unicode code points of the input string (case‑sensitive) and takes the result modulo 501 to produce a value between 0 and 500 mSv.

## Testing

```sh
go test ./...
```
