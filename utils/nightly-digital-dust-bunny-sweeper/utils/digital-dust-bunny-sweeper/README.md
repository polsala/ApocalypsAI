# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is your trusty sidekick in the never-ending battle against digital clutter! It's a whimsical-yet-useful utility designed to sniff out and report those pesky "digital dust bunnies" that accumulate in your file system. Think of it as a tiny, automated Roomba for your directories, identifying forgotten empty folders, ancient log files, zero-byte files, and other digital detritus that just takes up space and mental bandwidth.

It won't delete anything (we're not *that* chaotic), but it will give you a clear report so you can decide what to sweep away.

## ✨ Features

*   **Empty Directory Detection**: Finds directories that are completely devoid of files and subfolders.
*   **Zero-Byte File Spotting**: Identifies files that exist but contain absolutely no data.
*   **Old Log File Alert**: Flags `.log` files that haven't been touched in over 30 days.
*   **System Junk Identifier**: Points out common system-generated clutter like `.DS_Store` (macOS), `Thumbs.db` (Windows), and `desktop.ini` (Windows).

## 🚀 Usage

To unleash the Dust Bunny Sweeper, simply run the `dust_sweeper.py` script with the path you want to scan.

```bash
python src/dust_sweeper.py /path/to/your/directory
```

### Example Output

```
Scanning /home/user/my_project...

🧹 Digital Dust Bunny Report for /home/user/my_project 🧹

[EMPTY DIRECTORY] /home/user/my_project/old_temp_folder
[EMPTY DIRECTORY] /home/user/my_project/empty_logs
[ZERO-BYTE FILE] /home/user/my_project/data/corrupt.txt (0 bytes)
[OLD LOG FILE] /home/user/my_project/logs/app.log (Last modified: 2023-01-15 10:00:00)
[SYSTEM JUNK] /home/user/my_project/.DS_Store
[SYSTEM JUNK] /home/user/my_project/images/Thumbs.db

Found 6 digital dust bunnies. Time to tidy up!
```

## 🛠️ Development

The utility is written in Python 3.11 and uses only standard library modules, making it highly portable. Tests are self-contained and use `unittest.mock` for deterministic, offline execution.
