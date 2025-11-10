# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you tidy up your digital workspace. It scans specified directories for 'digital dust bunnies' – those forgotten, unused files and folders that accumulate over time, cluttering your system and consuming precious disk space.

Think of it as a tiny, autonomous Roomba for your file system, but instead of vacuuming, it identifies potential candidates for deletion and presents them in a neat, actionable report.

## ✨ Features

*   **Empty Directory Detection**: Finds directories that contain no files or subdirectories.
*   **Common Temporary File Identification**: Flags files like `__pycache__`, `.DS_Store`, `*.tmp`, `*.bak`, `*.swp`.
*   **Old Log File Suggestions**: Identifies `.log` files that haven't been modified recently (default: 30 days).
*   **Whimsical Report**: Presents findings with a touch of ApocalypsAI charm.
*   **Safe**: Only *suggests* deletions; never deletes anything automatically.

## 🚀 Usage

To run the sweeper, navigate to its directory and execute the `sweeper.py` script with the target path:

```bash
python3 src/sweeper.py --path /path/to/scan [--age-days 30]
```

*   `--path`: The root directory to start scanning from. (Required)
*   `--age-days`: Number of days after which a log file is considered 'old'. Defaults to 30. (Optional)

### Example Output

```
🧹 Initiating Digital Dust Bunny Sweep in /my/project...

Found 3 Digital Dust Bunnies:

[EMPTY DIRECTORY]
  Path: /my/project/build/empty_cache
  Rationale: This directory is utterly devoid of digital life. A prime candidate for removal.

[OLD LOG FILE]
  Path: /my/project/logs/debug.log
  Last Modified: 2023-01-15 10:30:00
  Rationale: This log file hasn't seen activity in 120 days. Perhaps it's time to archive or delete?

[TEMPORARY FILE]
  Path: /my/project/src/temp_file.tmp
  Rationale: A transient file, likely left behind by a hurried process. Safe to sweep away.


✨ Sweep complete! Consider tidying these up to keep your digital realm pristine.
```

## 🧪 Testing

To run the tests for the Digital Dust Bunny Sweeper:

```bash
python3 -m unittest tests/test_sweeper.py
```
