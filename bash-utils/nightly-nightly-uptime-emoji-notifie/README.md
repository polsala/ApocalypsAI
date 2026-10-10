# nightly-uptime-emoji-notifier

**What it does**

A tiny Bash utility that reads the system's uptime and prints a single emoji that visualises how long the machine has been running:

- `🌱` – less than 1 hour (a fresh sprout)
- `🌿` – between 1 hour and 1 day (a growing leaf)
- `🌳` – between 1 day and 1 week (a sturdy tree)
- `🌲` – more than a week (a seasoned forest)

**Why it’s useful**

Instead of staring at a raw number of seconds, you get an instant, human‑friendly visual cue—great for terminal prompts, dashboards, or just a daily sanity check.

**Installation**

```bash
# Clone the repository (or copy the script) into your $PATH
mkdir -p ~/bin
cp src/uptime-emoji.sh ~/bin/uptime-emoji
chmod +x ~/bin/uptime-emoji
```

**Usage**

```bash
# Default: reads the actual system uptime
uptime-emoji

# For testing or scripting, supply a custom uptime in seconds
uptime-emoji 4500   # => 🌿
```

**Running the tests**

The utility ships with a self‑contained Bash test suite. From the repository root:

```bash
bash tests/test_uptime_emoji.sh
```

You should see `All tests passed.` if everything is working.

**License**

MIT – feel free to fork, tweak, and share!
