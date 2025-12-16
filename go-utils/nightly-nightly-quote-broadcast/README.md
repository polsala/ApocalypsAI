# nightly-quote-broadcast

A whimsical Go utility that periodically broadcasts random quotes over UDP and listens for incoming quotes from other instances, printing them to the console. Perfect for spreading inspiration across a LAN.

## Features

- Reads quotes from a text file (one per line) or uses a built‑in list.
- Broadcasts a random quote every *N* seconds.
- Listens on the same UDP port for quotes from peers and prints them.
- Fully concurrent: broadcasting and listening run in separate goroutines.

## Installation

```sh
go build -o nightly-quote-broadcast ./src
```

## Usage

```sh
./nightly-quote-broadcast -port 9999 -interval 5 -quotes-file quotes.txt
```

- `-port` – UDP port to use (default 9999).
- `-interval` – seconds between broadcasts (default 10).
- `-quotes-file` – optional path to a file containing quotes, one per line.

## Example

```sh
$ ./nightly-quote-broadcast -port 9999 -interval 3
[2025-12-16T12:00:00Z] Received: "The only limit to our realization of tomorrow is our doubts of today."
[2025-12-16T12:00:03Z] Sent: "Life is what happens when you're busy making other plans."
...
```

## License

MIT
