# Digital Dust Bunny Sweeper

## 🧹 What is it?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you keep your digital workspace tidy. It scans specified directories for two types of 'dust bunnies':

1.  **Empty Directories**: Folders that contain no files or subdirectories.
2.  **Stale Files**: Files older than a configurable number of days.

It can operate in a 'scan-only' mode to show you what it *would* clean, or in a 'clean' mode to actually remove the identified clutter.

## ✨ Why use it?

Over time, development environments, build artifacts, and temporary files can accumulate, leading to cluttered directories and wasted disk space. This tool provides a simple, automated way to identify and remove such digital detritus, promoting a cleaner, more organized repository or project space.

## 🚀 How to use it

1.  **Navigate**: Change into the `utils/digital-dust-bunny-sweeper` directory.
2.  **Run**: Execute the `sweeper.py` script with the desired arguments.

```bash
python src/sweeper.py --path /path/to/scan --stale-days 30 --dry-run
```

### Arguments:

*   `--path <directory>`: (Required) The root directory to scan from. Can be specified multiple times.
*   `--stale-days <int>`: (Optional) Files older than this many days will be considered stale. Default is `30`.
*   `--dry-run`: (Optional) If present, the utility will only report what it *would* clean, without making any changes. This is the default behavior if `--clean` is not specified.
*   `--clean`: (Optional) If present, the utility will actually delete empty directories and stale files. **Use with caution!**

## 💡 Examples

*   **Scan for empty directories and files older than 60 days in your current directory (dry run):**
    ```bash
    python src/sweeper.py --path . --stale-days 60 --dry-run
    ```
*   **Clean up temporary build artifacts in a specific folder:**
    ```bash
    python src/sweeper.py --path /var/tmp/build-cache --stale-days 7 --clean
    ```
*   **Scan multiple paths:**
    ```bash
    python src/sweeper.py --path ~/Downloads --path /tmp --dry-run
    ```
