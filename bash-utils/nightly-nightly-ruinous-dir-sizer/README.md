# nightly-ruinous-dir-sizer

**What it does**

`nightly-ruinous-dir-sizer` scans a directory (default: current working directory) and prints the *N* largest entries (files or immediate sub‑directories) sorted by size.  It’s handy for quickly spotting what’s eating up disk space – a vital skill when supplies are scarce.

**Why the name?**

In the apocalyptic wasteland, every megabyte counts.  This script helps you prioritize what to delete, archive, or sacrifice to the void.

**Installation**

```bash
# Clone the repository (or copy the script) into your PATH
mkdir -p ~/bin && cp src/main.sh ~/bin/ruinous-dir-sizer
chmod +x ~/bin/ruinous-dir-sizer
```

**Usage**

```bash
# Show the top 10 largest entries in the current directory
ruinous-dir-sizer

# Show the top 5 largest entries in /var/log
ruinous-dir-sizer -n 5 /var/log

# Show all entries (no limit)
ruinous-dir-sizer -n 0 /home/user
```

**Options**

- `-n <number>` – Number of entries to display. `0` means *no limit* (show everything). Default is `10`.
- `-h` – Show help and exit.

**Exit codes**

- `0` – Success.
- `1` – Invalid arguments or an error while scanning.

**Testing**

Run the bundled test suite with:

```bash
cd tests && bash test_main.sh
```

The tests create a temporary directory with known file sizes and verify that the script reports them correctly.
