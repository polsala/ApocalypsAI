# Nightly Digital Dust Bunny Hunter

## 🧹 Overview

The `nightly-digital-dust-bunny-hunt` is a whimsical-yet-useful utility designed to help you keep your digital environment tidy. It scans specified directories for files that are older than a certain threshold (defaulting to 90 days) and generates a charming report on these 'digital dust bunnies'. It identifies common file types like logs, temporary files, and archives, giving you a clear picture of where your digital clutter resides.

**Important:** This utility is a reporter, not a cleaner. It will **never** delete or modify any files. Its sole purpose is to inform you about potential areas for manual cleanup.

## ✨ Features

*   **Whimsical Reporting:** Presents findings in a fun, engaging format.
*   **Age-Based Scanning:** Focuses on files older than a configurable number of days.
*   **File Type Categorization:** Groups findings by common file types (logs, temporary, archives, etc.).
*   **Directory Flexibility:** Scan default system locations or provide your own custom paths.
*   **Safe & Non-Destructive:** Only reports, never deletes.

## 🚀 Usage

To run the Digital Dust Bunny Hunter, simply execute the script. You can provide one or more directories as arguments. If no directories are specified, it will scan a set of default locations.

```bash
# Scan default directories (e.g., /tmp, ~/.cache, ~/.local/share/Trash/files)
./src/dust_bunny_hunt.sh

# Scan a specific directory
./src/dust_bunny_hunt.sh /var/log

# Scan multiple directories
./src/dust_bunny_hunt.sh /tmp /home/user/downloads /opt/old_projects

# Display help message
./src/dust_bunny_hunt.sh --help
```

### Example Output

```
🧹 ApocalypsAI Digital Dust Bunny Hunter 🧹
Scanning for digital dust bunnies older than 90 days...
Target directories: /tmp /home/user/downloads
---------------------------------------------------

Searching in: /tmp
  - Found a Temporary File bunny: old_temp.tmp
  - Found a Log/Text File bunny: debug.log

Searching in: /home/user/downloads
  - Found an Archive bunny: old_software.tar.gz

---------------------------------------------------
✨ Digital Dust Bunny Hunt Report ✨
Total ancient digital dust bunnies found: 3
Breakdown by type:
  - Temporary File: 1
  - Log/Text File: 1
  - Archive: 1

Recommendation: Consider sweeping these digital corners! (No files were deleted.)
```

## 🛠️ Development

### Prerequisites

*   Bash (version 4.0+ recommended for associative arrays)
*   `find` utility

### Script Structure

*   `src/dust_bunny_hunt.sh`: The main bash script containing the logic for scanning and reporting.
*   `tests/test_dust_bunny_hunt.sh`: A bash script for automated testing of the utility.

## 🧪 Testing

The utility includes a self-contained test script that uses mock commands to ensure deterministic and offline testing. To run the tests:

```bash
./tests/test_dust_bunny_hunt.sh
```

The tests will create a temporary environment, mock the `find` command to simulate different filesystem states, and then verify the output of the `dust_bunny_hunt.sh` script.
