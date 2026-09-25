# nightly-waste-decay

CLI tool that calculates remaining radioactive material after a given time using half‑life decay.

## Install

```sh
go build -o waste-decay ./src/main.go
```

## Usage

```sh
./waste-decay -initial 100 -half 10 -days 15
Remaining amount: 35.35533905932738 grams
```

## Flags

- `-initial` (float): initial amount in grams.
- `-half` (float): half‑life in days.
- `-days` (float): elapsed time in days.

## How it works

Uses the exponential decay formula:

```
remaining = initial * e^{-(ln 2) * days / half}
```
