# Nightly Digital Dust Bunny Sweeper

🧹✨ **Sweep Away Digital Clutter with Whimsical Flair!** ✨🧹

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet highly practical Bash utility designed to help you maintain a pristine digital environment. It metaphorically sweeps away "digital dust bunnies" – old, forgotten files and directories that accumulate over time, consuming precious disk space and contributing to system clutter.

By default, it performs a dry run, listing all the digital detritus it finds. With a simple `--clean` flag, it transforms into a powerful cleaning agent, banishing those pesky dust bunnies from your system.

## Features

*   **Whimsical Output:** Enjoy charming messages as your system gets a digital spring cleaning.
*   **Configurable Age:** Define what constitutes a "dust bunny" by specifying how many days old a file or directory must be.
*   **Dry Run by Default:** Safely preview what will be removed before committing to any changes.
*   **Recursive Scanning:** Scans the specified directory and all its subdirectories for old items.
*   **Simple Bash Script:** Easy to understand, modify, and integrate into your daily routines or CI/CD pipelines.

## Usage

```bash
./src/dust_bunny_sweeper.sh <path> [--age <days>] [--clean] [--help]
```

### Arguments

*   `<path>`: The root directory where the sweep should begin. This is a mandatory argument.

### Options

*   `--age <days>`: Specifies the age threshold in days. Any file or directory with a last modification time older than this many days will be considered a "dust bunny."
    *   Default: `7` days.
*   `--clean`: **Use with caution!** This flag instructs the utility to actually remove the identified files and directories. Without this flag, the script will only list the items it would remove (dry run).
*   `--help`: Displays the usage information and exits.

### Examples

**1. Dry run in your logs directory for items older than 30 days:**

```bash
./src/dust_bunny_sweeper.sh /var/log --age 30
```

**2. Actually clean up old downloads (older than 7 days by default):**

```bash
./src/dust_bunny_sweeper.sh ~/Downloads --clean
```

**3. Check for any dust bunnies in your home directory (dry run, default 7 days):**

```bash
./src/dust_bunny_sweeper.sh ~
```

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system (which is standard on most Linux/macOS environments).

1.  Clone the `polsala/ApocalypsAI` repository.
2.  Navigate to the `bash-utils/nightly-digital-dust-bunny-sweeper` directory.
3.  Make the script executable:
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```
4.  Run it!

## Development & Testing

To run the automated tests:

```bash
./tests/test_dust_bunny_sweeper.sh
```

The tests use Bash function overriding to mock the `find` and `rm` commands, ensuring they are deterministic and do not modify your actual filesystem. This allows for safe and repeatable testing of the script's logic.

## Contributing

Feel free to contribute by opening issues or pull requests. Suggestions for more whimsical messages are always welcome!
