# nightly-dusty-disk-detective

**What it does**

`nightly-dusty-disk-detective` is a tiny Bash script that checks the disk usage of the root (`/`) filesystem.  If the usage percentage exceeds a configurable threshold (default **80 %**), it prints a flamboyant ASCII‑art warning and a helpful message.  Otherwise it reports that everything is under control.

**Why it’s useful**

* Prevent surprise “disk full” crashes on servers or workstations.
* Gives you a fun, visual cue instead of a bland numeric log line.
* Fully self‑contained – no external dependencies beyond standard Unix tools.

**Installation**

```bash
# Clone the repository (or copy the folder into your utils tree)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-dusty-disk-detective
chmod +x src/main.sh
```

**Usage**

```bash
# Use the default 80% threshold
./src/main.sh

# Specify a custom threshold (e.g., 70%)
./src/main.sh 70
```

**Testing**

The utility ships with deterministic, offline tests that mock `df`.  Run them with:

```bash
cd utils/nightly-dusty-disk-detective
tests/test_main.sh
```

If everything is green you’ll see `All tests passed`.
