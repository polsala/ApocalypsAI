# Digital Dust Bunny Sweeper

## 🧹 Cleanse Your Digital Lair!

In the vast, ever-expanding cosmos of your repository, digital dust bunnies accumulate. These are the forgotten files, the ancient logs, the temporary artifacts that linger long past their usefulness, silently consuming precious disk space and cluttering your pristine project.

Fear not, for the ApocalypsAI Nightly Integrator presents the **Digital Dust Bunny Sweeper**! This utility will meticulously scan a specified directory, identify these digital detritus based on their age, and present you with a curated list of files ripe for removal. Keep your workspace sparkling clean and ready for the next cosmic event!

## ✨ Features

*   **Age-based Detection**: Pinpoints files older than a configurable number of days.
*   **Recursive Scanning**: Dives deep into subdirectories to find every last dust bunny.
*   **Safe Suggestions**: Only suggests files for deletion; never deletes anything without explicit user action.
*   **Whimsical Reporting**: Presents findings with a touch of apocalyptic charm.

## 🚀 Usage

To unleash the sweeper, navigate to its directory and run the Python script with the target path and desired age threshold (in days):

```bash
python src/dust_bunny_sweeper.py --path /path/to/your/repo --age 30
```

**Arguments:**

*   `--path <directory>`: The root directory to scan for digital dust bunnies. (Required)
*   `--age <days>`: The minimum age (in days) for a file to be considered a 'dust bunny'. Files older than this will be flagged. (Default: 30)

## 📋 Example Output

```
Scanning /path/to/your/repo for digital dust bunnies older than 30 days...

Found 3 digital dust bunnies:

- 🗑️ /path/to/your/repo/old_logs/archive_2022.log (Modified: 42 days ago, Size: 1.2 MB)
- 🗑️ /path/to/your/repo/temp/temp_file_xyz.tmp (Modified: 35 days ago, Size: 50 KB)
- 🗑️ /path/to/your/repo/misc/forgotten_script.sh (Modified: 60 days ago, Size: 10 KB)

Consider these files for manual cleanup to maintain optimal repository hygiene!
```
