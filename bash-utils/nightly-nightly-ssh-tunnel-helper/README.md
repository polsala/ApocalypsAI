Nightly SSH Tunnel Helper
========================

This utility creates a temporary SSH tunnel to a remote host, prints a whimsical confirmation, and automatically tears it down when finished.

Usage
-----

```bash
./src/main.sh -h <host> -l <local_port> -r <remote_port> [-c <command>] [-t <timeout>]
```

Options
-------

- `-h HOST`   Remote host to connect to.
- `-l PORT`   Local port to forward.
- `-r PORT`   Remote port to expose.
- `-c CMD`    Optional command to run while the tunnel is active.
- `-t SECS`   Optional timeout in seconds; the tunnel will be closed after this period.

Examples
--------

```bash
# Simple tunnel
./src/main.sh -h example.com -l 2222 -r 22

# Tunnel and run a command
./src/main.sh -h example.com -l 2222 -r 22 -c "echo 'Hello'"

# Tunnel with timeout
./src/main.sh -h example.com -l 2222 -r 22 -t 60
```

The script prints a whimsical message like:

```
🛡️ Tunnel established to example.com on local port 2222
```

When the command finishes or the timeout expires, the tunnel is closed automatically.

License
-------

MIT
