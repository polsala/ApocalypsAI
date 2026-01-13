Nightly Port Scanner

A whimsical concurrent TCP port scanner written in Go. It scans a range of ports on a target host using goroutines and reports any open ports. Perfect for postâapocalyptic network reconnaissance.

Usage:
  go run . -host <target> -start <port> -end <port> [-timeout <ms>]

Example:
  go run . -host localhost -start 80 -end 85

The tool limits concurrency to 100 workers to avoid overwhelming the system.

