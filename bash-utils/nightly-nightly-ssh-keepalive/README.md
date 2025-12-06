# nightly-ssh-keepalive

Utility to keep SSH connections alive by periodically probing target hosts.

## Overview

Long‑running SSH sessions can be dropped by intermediate firewalls or NAT devices after a period of inactivity. This script sends a quick TCP probe to the SSH port (22) of each specified host, preventing idle‑timeout mechanisms from closing the connection.

## Usage

```sh
./src/main.sh -i 300 host1.example.com host2.example.com
```

- `-i INTERVAL` – seconds between probes (default 300). Use with a scheduler like `cron` for continuous operation.
- `-p PORT` – SSH port to probe (default 22).
- `-f FILE` – file containing one host per line (hosts listed on the command line are also accepted).

The script exits after a single round of probes; schedule it repeatedly for continuous keep‑alive.

## Exit Codes

- `0` – all probes succeeded.
- `1` – one or more probes failed.

## Testing

Run the bundled test suite:

```sh
cd tests && ./test_main.sh
```

The tests use a mock `nc` binary to simulate network behavior.
