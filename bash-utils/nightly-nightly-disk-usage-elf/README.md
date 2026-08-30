# nightly-disk-usage-elf

**What it does**

`nightly-disk-usage-elf` scans the system's disk usage (using `df`) and prints a concise report for each mounted filesystem:

- ✅  when usage is below the warning threshold (default 80%).
- ⚠️  when usage meets or exceeds the threshold, followed by a tiny ASCII elf that reminds you to clean up.

The utility is pure Bash, has no external dependencies, and can be dropped into any Unix‑like environment.

---

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-disk-usage-elf

# Make the script executable
chmod +x src/main.sh
```

Optionally add the `src` directory to your `PATH` or create a symlink:

```bash
ln -s $(pwd)/src/main.sh /usr/local/bin/disk-elf
```

---

## Usage

```bash
# Use default threshold (80%)
./src/main.sh

# Specify a custom threshold (e.g., 90%) via environment variable
THRESHOLD=90 ./src/main.sh
```

Sample output:

```
✅  /home is at 12%
⚠️  / is at 95%
   /\
  /  \
 /____\
 |    |
 |____|
 (\_/)
 ( •_•)
 / >🍎  Time to clean up!
```

---

## Testing

Run the bundled tests with Bash:

```bash
cd tests
bash test_main.sh
```

All tests should pass on any POSIX‑compatible shell.
