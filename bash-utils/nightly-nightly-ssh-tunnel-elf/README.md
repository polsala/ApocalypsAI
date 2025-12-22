# nightly-ssh-tunnel-elf

**What it does**

`nightly-ssh-tunnel-elf` is a tiny Bash utility that helps you spin up a persistent SSH tunnel (dynamic SOCKS proxy) with automatic reconnection on failure.  It stores the tunnel PID in a lock file, can stop the tunnel, and shows a whimsical status screen featuring an ASCII‑elf.

**Why the elf?**

Because every tunnel needs a guardian, and elves are great at watching over hidden passages.

**Installation**

```bash
# Clone the utility into your preferred bin directory
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/nightly-ssh-tunnel-elf/src/main.sh /usr/local/bin/ssh-tunnel-elf
chmod +x /usr/local/bin/ssh-tunnel-elf
```

**Usage**

```bash
# Start a tunnel to remote host example.com on port 22
ssh-tunnel-elf start user@example.com 1080

# Check status (shows ASCII elf)
ssh-tunnel-elf status

# Stop the tunnel
ssh-tunnel-elf stop
```

**Options**

- `start <user@host> <local_port>` – creates a dynamic SOCKS tunnel on `<local_port>`.
- `stop` – terminates the running tunnel.
- `status` – prints whether a tunnel is active and shows the elf.

**Configuration**

You can override the SSH binary used by setting the environment variable `SSH_TUNNEL_ELF_SSH_CMD` to a custom command (useful for testing).

**Testing**

Run the bundled tests with:

```bash
cd utils/nightly-ssh-tunnel-elf/tests
bash test_main.sh
```

All tests should pass offline.
