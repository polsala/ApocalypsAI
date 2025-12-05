# Nightly Digital Garden Monitor

## 🌷 Cultivate Your Digital Landscape 🍂

The `nightly-digital-garden-monitor` is a whimsical utility designed to help you understand the "freshness" and activity within your project directories. Like a diligent gardener, it surveys your files and categorizes them based on their last modification date, giving you a quick overview of what's blooming, thriving, wilting, or sadly, fossilized.

Keep your digital garden vibrant and free of forgotten relics!

## Usage

Run the script with the path to the directory you wish to monitor:

```bash
python src/garden_monitor.py --path /path/to/your/project
```

### Options

*   `--path <directory>`: The root directory to scan. (Required)
*   `--verbose`: (Optional) Show individual files in the report, not just summaries.

## Output Example

```
Digital Garden Report for /path/to/your/project:

🌷 Blooming (last 7 days): 5 files
🌱 Thriving (last 30 days): 12 files
🍂 Wilting (last 90 days): 8 files
💀 Fossilized (over 90 days): 25 files

Total files scanned: 50
```

With `--verbose`:

```
Digital Garden Report for /path/to/your/project:

🌷 Blooming (last 7 days):
  - src/main.py (2 days ago)
  - docs/README.md (5 days ago)
  - ...
🌱 Thriving (last 30 days):
  - lib/utils.py (15 days ago)
  - tests/test_feature.py (28 days ago)
  - ...
🍂 Wilting (last 90 days):
  - old_feature.py (60 days ago)
  - config/default.ini (85 days ago)
  - ...
💀 Fossilized (over 90 days):
  - legacy/archive.zip (150 days ago)
  - forgotten_script.sh (300 days ago)
  - ...

Total files scanned: 50
```

## Categories

*   **🌷 Blooming**: Files modified within the last 7 days. These are actively being worked on!
*   **🌱 Thriving**: Files modified within the last 30 days. Healthy and regularly maintained.
*   **🍂 Wilting**: Files modified within the last 90 days. Might need a check-up or pruning soon.
*   **💀 Fossilized**: Files modified more than 90 days ago. These are the digital dust bunnies, potentially forgotten or obsolete. Consider archiving or deleting them.

## Development

This utility is written in Python 3.11 and uses only standard library modules.

To run tests:

```bash
python -m unittest tests/test_garden_monitor.py
```
