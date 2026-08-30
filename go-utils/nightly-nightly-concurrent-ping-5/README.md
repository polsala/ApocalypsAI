Nightly Concurrent Ping Utility

Overview:
A tiny Go command-line tool that pings multiple hosts concurrently and reports the latency in milliseconds. Useful for quick network health checks in a post‑apocalyptic bunker.

Usage:
  nightly-concurrent-ping host1 host2 ...

The tool prints each host with its measured latency or an error.

Implementation notes:
- Uses goroutines and a WaitGroup.
- Real ping uses TCP connection to port 80 with a timeout.
- In tests, the ping function is mocked for deterministic results.
