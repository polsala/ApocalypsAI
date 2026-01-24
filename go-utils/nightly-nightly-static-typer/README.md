# Nightly Static Typer

**Nightly Static Typer** is a tiny Go command‑line utility that reads lines from standard input and sprinkles a handful of “static” characters (like ~, *, #, %) into each line.  It does the work with a configurable pool of goroutine workers, demonstrating Go’s lightweight concurrency while keeping the output delightfully noisy.

## Features

- **Concurrent processing** – lines are handled by a worker pool (default 4 workers).
- **Deterministic mode** – supply a `-seed` flag to get repeatable output (useful for testing).
- **Customizable workers** – change the number of workers with `-workers`.
- **Zero external dependencies** – pure Go standard library.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/your-org/ApocalypsAI.git
cd utils/nightly-static-typer
go build -o static-typer ./src/main.go
```

## Usage

```bash
# Pipe text into the program
cat myfile.txt | ./static-typer -workers 6 -seed 42
```

If you omit `-seed`, the program uses a non‑deterministic seed based on the current time.

## Example

```text
Input:  hello world
Output: he~llo w#orld
```

The exact static characters and their positions vary (or are repeatable when a seed is provided).

## Testing

Run the test suite with:

```bash
go test ./tests
```

The tests verify that the original characters are preserved and that the length of each line grows by `len(line)/5` static characters.

---

*Created by the ApocalypsAI Nightly Integrator agent.*
