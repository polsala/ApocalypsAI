# Digital Dust Bunny Duster

## 🧹 Description

Before the grand reset, let's ensure our digital spaces are pristine! The `Digital Dust Bunny Duster` is a whimsical yet practical utility designed to help you clean up your project directories. It scans a specified path to identify two types of 'dust bunnies':

1.  **Empty Directories**: Directories that contain no files or subdirectories.
2.  **Old, Small Files**: Files that are older than a specified age, smaller than a certain size, and match a given set of file extensions (e.g., `.log`, `.tmp`, `.bak`).

This tool can perform a dry run to show you what it would clean, or proceed with actual deletion, helping to free up disk space and maintain a tidy repository.

## 🚀 Usage

To run the duster, navigate to the utility's directory or call it directly with `python`:

```bash
python3 utils/nightly-digital-dust-bunny-duster/src/duster.py --path <directory_to_scan> [options]
```

### Arguments:

*   `--path <directory>`: (Optional) The root directory to scan for dust bunnies. Defaults to the current directory (`.`).
*   `--dry-run`: (Optional) If present, the duster will only list the items it would delete without actually removing them. Highly recommended for a first run!
*   `--age <days>`: (Optional) The minimum age in days for files to be considered 'old'. Files older than this will be targeted. Defaults to `30` days.
*   `--size <kb>`: (Optional) The maximum size in kilobytes for files to be considered 'small'. Files smaller than this will be targeted. Defaults to `1` KB.
*   `--patterns <ext1,ext2,...>`: (Optional) A comma-separated list of file extensions (without the leading dot) to target. Only files matching these extensions will be considered. Defaults to `log,tmp,bak`.

### Examples:

1.  **Dry run in the current directory, default settings:**
    ```bash
    python3 src/duster.py --dry-run
    ```

2.  **Clean up a specific 'build' directory, targeting `.temp` and `.cache` files older than 7 days and smaller than 5KB:**
    ```bash
    python3 src/duster.py --path ./build --age 7 --size 5 --patterns temp,cache
    ```

3.  **Perform actual deletion of all identified dust bunnies in the current directory:**
    ```bash
    python3 src/duster.py
    ```

## 🧪 Testing

To run the tests for the Digital Dust Bunny Duster, navigate to the utility's directory and execute the test file:

```bash
python3 utils/nightly-digital-dust-bunny-duster/tests/test_duster.py
```
