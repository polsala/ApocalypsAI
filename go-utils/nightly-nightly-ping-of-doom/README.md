Nightly Ping of Doom
A whimsical concurrent ping utility that measures TCP latency to multiple hosts and reports min/avg/max.

Usage:
  ping-of-doom host1 host2 ...

The tool attempts a TCP connection to port 80 with a 2 second timeout.
Results are printed in milliseconds.

It runs pings concurrently, making it fast even for many hosts.
