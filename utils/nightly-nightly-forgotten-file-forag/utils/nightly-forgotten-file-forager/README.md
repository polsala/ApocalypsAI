# Nightly Forgotten File Forager

## 🧹 Unearthing Digital Dust Bunnies 🧹

The Nightly Forgotten File Forager is your trusty digital archaeologist, designed to scour your repository for files that have long been neglected, gathering digital dust. It helps you identify and optionally remove old, temporary, or build-related files that might be silently hogging space or slowing down your workflows.

Think of it as a friendly digital janitor, ensuring your project stays spick and span, ready for whatever the apocalypse throws its way.

## Usage

Run the forager from your terminal. It requires a target path and an age threshold in days. By default, it will only report files it finds. To actually delete them, you must provide the `--delete` flag.

```bash
python3 src/forager.py --path /path/to/your/repo --age 30
```

### Options

*   `--path <directory>` (required): The root directory to start foraging from.
*   `--age <days>` (required): Files older than this many days will be considered 'forgotten'.
*   `--patterns <pattern1,pattern2,...>` (optional): Comma-separated list of glob patterns (e.g., `*.log`, `__pycache__/*`, `*.tmp`) to filter files. If not provided, all files older than the age threshold are considered.
*   `--delete` (optional): If present, the forager will actually delete the identified forgotten files. **Use with caution!**
*   `--verbose` (optional): Print detailed information about files being processed.

## Examples

### 1. Find all files older than 90 days in the current directory (report only):

```bash
python3 src/forager.py --path . --age 90
```

### 2. Find and delete all `.log` and `.tmp` files older than 7 days in a specific build directory:

```bash
python3 src/forager.py --path ./build --age 7 --patterns "*.log,*.tmp" --delete
```

### 3. Find and report old Python cache directories (`__pycache__`) across the entire project:

```bash
python3 src/forager.py --path . --age 365 --patterns "__pycache__/*" --verbose
```
