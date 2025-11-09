# Digital Dust Bunny Sweeper

## Purpose
This utility helps you keep your project directories tidy by identifying and listing 'digital dust bunnies' – old, unused, or redundant files and directories that accumulate over time. By sweeping these away, you can declutter your repository, potentially speed up build processes, and improve overall project hygiene.

## Usage
Run the `sweeper.py` script from your terminal, providing the path to the directory you wish to clean.

```bash
python src/sweeper.py <path_to_project_root> [--age <days>] [--ignore-patterns <glob1,glob2,...>]
```

### Arguments:
*   `<path_to_project_root>`: The absolute or relative path to the directory you want to scan.
*   `--age <days>` (optional): Files and directories older than this many days will be considered 'dust bunnies'. Defaults to `30` days.
*   `--ignore-patterns <glob1,glob2,...>` (optional): A comma-separated list of glob patterns (e.g., `*.log`, `temp_*`, `node_modules/`) to exclude from the scan. Items matching these patterns will not be suggested for deletion, regardless of age. Defaults to common build/temp files like `*.pyc, __pycache__, .git, .DS_Store, *.tmp, *.bak, .venv, env, node_modules`.

## Example

```bash
python src/sweeper.py . --age 60 --ignore-patterns "*.log,build/"
```
This command will scan the current directory, looking for files and folders older than 60 days, while ignoring any `.log` files or anything inside a `build/` directory.

## Output
The utility will print a list of paths that are suggested for deletion. It does **not** delete files itself; it only provides recommendations. Review the list carefully before taking any action.
