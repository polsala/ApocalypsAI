# Digital Dust Bunny Sweeper

## Whimsical Purpose
Even the most pristine digital repositories can accumulate 'digital dust bunnies' – those pesky, often forgotten, empty directories, temporary files, and miscellaneous junk that clutter up your project. The Digital Dust Bunny Sweeper is here to help you identify these digital nuisances, ensuring your codebase remains as clean and efficient as a freshly swept server room.

## Genuinely Useful Functionality
This utility scans a specified directory (and its subdirectories) for common types of digital clutter, including:
- **Empty directories**: Directories that contain no files or subdirectories.
- **Temporary/Log files**: Files matching patterns like `*.log`, `*.tmp`, `*.bak`, `*.pyc`.
- **System-generated junk files**: Files like `.DS_Store`, `Thumbs.db`.
- **System-generated junk directories**: Directories like `__pycache__`, `.pytest_cache`, `.ipynb_checkpoints`.

The sweeper will output a report listing all identified 'dust bunnies', allowing you to review and manually clean them up, keeping your repository lean and tidy.

## How to Use

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```

2.  **Run the sweeper with the target directory**:
    Provide the path to the directory you want to scan. This can be a relative or absolute path.
    ```bash
    python dust_bunny_sweeper.py /path/to/your/project
    # Or, to scan the current directory:
    python dust_bunny_sweeper.py .
    ```

## Example Output

```
Scanning directory: /path/to/your/project

Found 7 Digital Dust Bunnies:

Empty Directories:
  - /path/to/your/project/empty_folder_1
  - /path/to/your/project/src/another_empty_dir

Junk Files:
  - /path/to/your/project/logs/app.log
  - /path/to/your/project/temp/data.tmp
  - /path/to/your/project/src/module.pyc

Junk Directories:
  - /path/to/your/project/__pycache__
  - /path/to/your/project/.pytest_cache

Sweep complete! Review the list above for potential cleanup.
```
