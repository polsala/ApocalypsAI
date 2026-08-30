# Nightly Radio Chatter Simulator

Generates whimsical simulated radio chatter logs for post‑apocalypse role‑play or tabletop games.

## Usage

```sh
go run ./src -n 5
```

Outputs something like:

```
[12:34] ALPHA: All units, report status.
[12:35] BRAVO: Water purification complete.
...
```

## Options

- `-n` – number of messages (default 5)

## Testing

Run `go test ./...` to execute the deterministic unit test.
