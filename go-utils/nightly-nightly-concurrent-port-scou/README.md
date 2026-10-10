# Nightly Concurrent Port Scout

**Overview**

`nightly-concurrent-port-scout` is a tiny Go utility that scans a range of TCP ports on a given host using massive concurrency.  It reports any open ports with a touch of apocalyptic flair – perfect for sysadmins, pen‑testers, or anyone who enjoys watching ports *rise from the ashes*.

**Features**

- Fully concurrent scanning (user‑configurable goroutine limit)
- Adjustable timeout per connection
- Simple command‑line interface
- Deterministic output suitable for piping into other tools

**Installation**

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-concurrent-port-scout
go build -o port-scout ./src/main.go
```

**Usage**

```bash
./port-scout -host=example.com -start=1 -end=1024 -concurrency=200 -timeout=200
```

- `-host`      : Target hostname or IP address.
- `-start`     : Starting port number (inclusive).
- `-end`       : Ending port number (inclusive).
- `-concurrency`: Maximum number of simultaneous connection attempts.
- `-timeout`   : Connection timeout in milliseconds.

**Example Output**

```
Scanning 1‑1024 on example.com with up to 200 workers…
🔥 Port 22 is open! (SSH)
🔥 Port 80 is open! (HTTP)
🔥 Port 443 is open! (HTTPS)
Scanning complete. 3 open ports found.
```

**Testing**

Run the bundled tests with:

```bash
go test ./tests
```

The tests spin up temporary listeners to verify that open ports are detected and closed ports are ignored.
