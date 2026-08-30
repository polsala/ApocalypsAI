# nightly-quantum-port-scanner

A whimsical concurrent port scanner that reports open ports with emoji flair.

## Usage
```sh
go run . -host <hostname> -ports <p1,p2,...>
```
Example:
```sh
go run . -host localhost -ports 22,80,443
```
The tool scans the supplied ports concurrently and prints a line for each, using ✅ for open and ❌ for closed ports.

## Build
```sh
go build -o port-scanner
```
Run the binary:
```sh
./port-scanner -host example.com -ports 80,443
```

## Testing
```sh
go test ./...
```
