# Digital Dust Bunny Sweeper

## 🧹 What is this?

In the vast digital expanse of our repositories, forgotten files accumulate like dust bunnies under a server rack. The `Digital Dust Bunny Sweeper` is a whimsical yet practical utility designed to help you identify and clear out these digital relics: old, large, and potentially unused files that are silently consuming precious storage and cognitive load.

Think of it as your personal post-apocalyptic digital janitor, ensuring your data bunkers are lean, mean, and ready for the next epoch.

## ✨ Features

*   **Age-based Detection**: Flags files older than a specified number of days.
*   **Size-based Filtering**: Ignores tiny files, focusing on those that actually matter.
*   **Whimsical Suggestions**: Presents findings with a touch of ApocalypsAI charm.
*   **Self-contained**: A single Python script, no external dependencies beyond standard library.

## 🚀 How to Use

1.  Navigate to the `utils/digital-dust-bunny-sweeper/` directory.
2.  Run the script with the target directory and optional parameters:

    ```bash
    python src/sweeper.py --path /path/to/your/project --age 365 --min-size 1024
    ```

### Arguments:

*   `--path <directory>` (required): The directory to scan for digital dust bunnies.
*   `--age <days>` (optional, default: 365): Files older than this many days will be flagged.
*   `--min-size <kilobytes>` (optional, default: 1024): Files smaller than this size (in KB) will be ignored.

## 💡 Example Output

```
Scanning /path/to/your/project for digital dust bunnies...

Found 3 potential digital dust bunnies:

*   [2021-03-15] 5.2 MB - /path/to/your/project/old_backup.zip
    -> "A relic from a forgotten era. Perhaps it's time for this digital fossil to return to the byte-dust it came from?"

*   [2022-01-20] 1.8 MB - /path/to/your/project/temp/large_log.txt
    -> "This digital tumbleweed has been rolling around for a while. Is it still serving a purpose, or just collecting virtual lint?"

*   [2021-11-01] 2.1 MB - /path/to/your/project/unused_asset.png
    -> "A spectral image from the past. Does it still spark joy, or just occupy space in your digital catacombs?"

Cleanup suggested for 3 files. Proceed with caution, and may your storage be ever lean!
```
