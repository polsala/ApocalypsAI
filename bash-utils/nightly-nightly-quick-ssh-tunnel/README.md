Nightly Quick SSH Tunnel
========================

A quick Bash helper to set up a local SSH tunnel with a single command.

Usage
-----

```bash
./src/main.sh -h <remote_host> -p <remote_port> -l <local_port> [-u <user>] [-k <key_file>] [-n <name>]
```

Options
-------

- `-h` Remote host (required)
- `-p` Remote port (required)
- `-l` Local port (required)
- `-u` SSH user (default: current user)
- `-k` SSH private key file (optional)
- `-n` Tunnel name for logging (optional)

Example
-------

```bash
./src/main.sh -h example.com -p 22 -l 8080 -u alice -k ~/.ssh/id_rsa -n "webproxy"
```

This will start an SSH tunnel that forwards local port 8080 to port 22 on example.com as user alice.

Whimsical Note
--------------

If the tunnel starts successfully, the script will print a tiny ASCII art of a rocket launching.
