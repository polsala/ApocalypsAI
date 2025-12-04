# Nightly Scavenger's Manifest Generator

## Description
In the digital wasteland, data can be scattered and forgotten. The `nightly-scavenger-manifest-generator` is your trusty tool for quickly inventorying the digital debris you stumble upon. It scans a specified directory, identifies files, and compiles a neat markdown manifest listing each file's relative path, size, and last modification timestamp. Perfect for keeping track of your salvaged data caches!

## Usage

### Prerequisites
*   Python 3.11+

### Running the Utility

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-scavenger-manifest-generator/src
    ```

2.  **Generate a manifest for a directory:**
    ```bash
    python manifest_generator.py /path/to/your/data/cache -o my_cache_manifest.md
    ```
    This will create `my_cache_manifest.md` in the current directory, detailing all files found in `/path/to/your/data/cache`.

3.  **Filter by file extensions:**
    You can specify which file types to include in your manifest.
    ```bash
    python manifest_generator.py /path/to/your/logs -o log_manifest.md -e .log .txt
    ```
    This command will only include files ending with `.log` or `.txt`. You can omit the leading dot, and it will be added automatically (e.g., `-e log txt`).

### Arguments

*   `directory` (positional): The path to the directory you want to scan.
*   `-o`, `--output` (optional): The name of the output markdown file. Defaults to `scavenger_manifest.md`.
*   `-e`, `--extensions` (optional): A space-separated list of file extensions to include (e.g., `.txt .json`). If not provided, all files will be included.

## Example Output (`scavenger_manifest.md`)

```markdown
# Scavenger's Manifest for 'my_data_cache'
Generated on: 2023-10-27T08:30:00.123456

| File Path | Size | Last Modified |
|---|---|---|
| `documents/report.txt` | 1.23 KB | 2023-10-25T14:15:22 |
| `images/logo.png` | 256.78 KB | 2023-09-10T09:00:00 |
| `logs/server.log` | 4.50 MB | 2023-10-27T08:29:55 |
| `data/archive.zip` | 1.50 GB | 2023-08-01T18:00:00 |
```
