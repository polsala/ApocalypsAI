# Nightly Log Mood Ring

## 🔮 Purpose

The Nightly Log Mood Ring is a whimsical-yet-useful utility designed to give you a quick, at-a-glance sentiment analysis of your system's log files. Instead of sifting through endless lines, get a "mood" summary indicating overall system health based on log entries.

## ✨ How It Works

This utility scans specified log directories for `.log` files. For each file, it counts occurrences of keywords like `ERROR`, `WARNING`, `SUCCESS`, `INFO`, and `CRITICAL`. Based on these counts, it calculates a weighted "mood score" and assigns a corresponding emoji and descriptive sentiment.

## 🚀 Usage

To run the Log Mood Ring, simply execute the `log_analyzer.py` script. By default, it will scan the current directory and its subdirectories for `.log` files.

```bash
python3 src/log_analyzer.py
```

You can specify a different directory to scan:

```bash
python3 src/log_analyzer.py --path /var/log/my_app
```

### Output Example

```
Nightly Log Mood Ring Report (2023-10-27)

Scanning logs in: .

--- app.log ---
Mood: 😬 (Anxious)
  CRITICAL: 0
  ERROR:    1
  WARNING:  3
  INFO:     10
  SUCCESS:  5

--- sys.log ---
Mood: ✅ (Serene)
  CRITICAL: 0
  ERROR:    0
  WARNING:  0
  INFO:     25
  SUCCESS:  12

--- Overall System Mood ---
Mood: 💬 (Neutral)
  Total CRITICAL: 0
  Total ERROR:    1
  Total WARNING:  3
  Total INFO:     35
  Total SUCCESS:  17
```

## ⚙️ Configuration

The utility currently uses hardcoded keywords and weights. Future versions might allow for custom configuration via a `config.ini` or similar.

## 🧪 Development

The `log_analyzer.py` script is written in Python 3.11 and has no external dependencies beyond the standard library. Tests are located in `tests/test_log_analyzer.py`.
