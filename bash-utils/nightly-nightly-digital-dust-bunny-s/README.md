# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet practical bash utility designed to help you declutter your digital spaces. It scours specified directories for "digital dust bunnies" – files that haven't been accessed or modified in a long time – and provides options to report, archive, or even gently evict them. Keep your file systems sparkling clean and free from ancient, forgotten bits!

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] <directory>
```

### Options:

*   `-a <days>`, `--age <days>`: Files older than this many days will be considered dust bunnies. Default is 90 days.
*   `-m <mode>`, `--mode <mode>`:
    *   `report` (default): Just list the identified dust bunnies.
    *   `archive`: Move identified files to a `.dust_bunnies_archive` subdirectory within their parent directory.
    *   `delete`: Permanently remove identified files. **Use with caution!**
*   `-d`, `--dry-run`: Show what *would* happen without performing any actions. Highly recommended before `archive` or `delete` modes.
*   `-h`, `--help`: Display this help message.

### Examples:

1.  **Report all dust bunnies older than 120 days in your home directory (dry-run):**
    ```bash
    ./src/dust_bunny_sweeper.sh --age 120 --dry-run ~/my_documents/
    ```

2.  **Archive dust bunnies older than 30 days in a specific project folder:**
    ```bash
    ./src/dust_bunny_sweeper.sh --age 30 --mode archive ~/projects/old-project/
    ```

3.  **Permanently delete dust bunnies older than 365 days in a temporary directory (use with extreme caution!):**
    ```bash
    ./src/dust_bunny_sweeper.sh --age 365 --mode delete --dry-run /tmp/ancient-logs/
    ```

## How it Works

The script uses the `find` command to locate files based on their last modification time (`-mtime`).
- In `report` mode, it simply prints the paths.
- In `archive` mode, it creates a `.dust_bunnies_archive` directory (if it doesn't exist) in the parent directory of each dust bunny and moves the file there.
- In `delete` mode, it removes the files.
All actions are confirmed with the user unless `--dry-run` is specified.

## Installation

Simply clone the repository and navigate to the `bash-utils/nightly-digital-dust-bunny-sweeper` directory. The script is self-contained.

## Contributing

Feel free to sweep in with improvements or new features!
