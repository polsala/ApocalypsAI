# nightly‑ascii‑clock

**What it does**

`nightly-ascii-clock` is a tiny, self‑contained Python utility that prints the current local time in big, readable ASCII‑art digits. It can be used in terminal dashboards, live‑stream overlays, or simply as a quirky way to check the time without leaving the console.

**Features**

- Zero external dependencies (only the Python standard library).
- Deterministic, offline unit tests that mock the system clock.
- Simple CLI: `python -m src.clock` prints the time, or import `get_ascii_time` for programmatic use.

**Installation**

The utility lives under `utils/nightly-ascii-clock/`. No installation step is required – just run the module directly:

```bash
python -m utils/nightly-ascii-clock/src/clock
```

**Example output** (for 14:35):

```
  _   _       _   _ 
 | | | |  _  | | | |
 |_| |_| |_| |_| |_| 
```

**Running the tests**

```bash
python -m unittest discover -s utils/nightly-ascii-clock/tests
```

---

*Created by the ApocalypsAI Nightly Integrator agent.*
