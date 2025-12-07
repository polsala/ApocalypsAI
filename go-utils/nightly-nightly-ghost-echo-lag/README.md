Nightly Ghost Echo Lag
======================

A whimsical Go CLI that measures and reports the round‑trip time to a host, echoing the latency like a ghostly echo.

Features
--------

* Connects to a TCP host and measures RTT.
* Prints RTT in milliseconds with a playful message.
* Simple flags: `-host`, `-port`.

Installation
------------

```bash
go install github.com/polsala/ApocalypsAI/utils/nightly-ghost-echo-lag@latest
```

Usage
-----

```bash
# Measure RTT to localhost on port 80
nightly-ghost-echo-lag -host localhost -port 80

# Measure RTT to example.com on port 443
nightly-ghost-echo-lag -host example.com -port 443
```

Output
------

```
Ghostly echo: RTT = 12 ms
```

Testing
-------

Run the tests with:

```bash
go test ./...
```

License
-------

MIT
