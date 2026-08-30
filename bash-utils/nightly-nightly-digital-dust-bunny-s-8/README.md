# nightly-digital-dust-bunny-sweeper

## 🧹 The Nightly Digital Dust Bunny Sweeper 🧹

Are your digital spaces feeling a bit cluttered? Do forgotten files lurk in the dark corners of your directories, gathering virtual dust? Fear not, for the Nightly Digital Dust Bunny Sweeper is here to help! This whimsical Bash utility will seek out those ancient, unused files – your "digital dust bunnies" – and, with your permission, sweep them away, leaving your directories sparkling clean.

## ✨ Features

-   **Whimsical Interface**: Enjoy charming messages as your system gets tidied.
-   **Targeted Sweeping**: Specify which directories to clean.
-   **Age-Based Detection**: Define how old a file must be to be considered a "dust bunny".
-   **Dry-Run Mode (Default)**: See what would be swept away before any actual deletion occurs.
-   **Interactive Confirmation**: Get a chance to review and confirm deletions.
-   **Force Mode**: Skip confirmations for automated cleanups (use with caution!).

## 🚀 Usage

First, make sure the script is executable:
```bash
chmod +x src/dust_bunny_sweeper.sh
```

### Basic Dry-Run (Default)

Scan `/tmp` and `/var/log` for files older than 30 days, without deleting anything:
```bash
./src/dust_bunny_sweeper.sh /tmp /var/log
```

### Clean Up Files Older Than 7 Days

Scan `/home/user/downloads` for files older than 7 days and prompt for deletion:
```bash
./src/dust_bunny_sweeper.sh -a 7 -c /home/user/downloads
```

### Force Clean Up (No Prompt)

Sweep away all digital dust bunnies older than 60 days in `/var/cache` without asking for confirmation:
```bash
bash src/dust_bunny_sweeper.sh --age 60 --clean --force /var/cache
```

### Get Help

```bash
./src/dust_bunny_sweeper.sh --help
```

## ⚙️ Options

-   `-a <DAYS>`, `--age <DAYS>`: Files older than `<DAYS>` will be considered dust bunnies. Default: `30` days.
-   `-c`, `--clean`: Perform actual deletion. By default, the script runs in dry-run mode.
-   `-f`, `--force`: Automatically confirm deletion without a prompt. **Use with extreme caution!**
-   `-h`, `--help`: Display the help message and exit.

## ⚠️ Important Notes

-   This script uses the `find` command. Ensure you have appropriate permissions for the directories you are scanning.
-   The `--force` option bypasses all confirmation prompts. Double-check your target directories and age settings before using it in automated scripts.
-   Only regular files (`-type f`) are considered dust bunnies. Directories themselves are not targeted for deletion by this utility.

## 🧪 Testing

To run the automated tests:

```bash
chmod +x tests/test_dust_bunny_sweeper.sh
./tests/test_dust_bunny_sweeper.sh
```

The tests use mock functions for `find` and `rm` to ensure determinism and prevent actual file system modifications during testing.
