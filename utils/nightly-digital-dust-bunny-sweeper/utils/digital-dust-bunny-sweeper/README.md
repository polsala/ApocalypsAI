# Digital Dust Bunny Sweeper

## 🧹 Purpose

This whimsical utility helps you tidy up your project directories by identifying and listing 'digital dust bunnies' – those forgotten, unused files, empty directories, and common temporary artifacts that accumulate over time. Think of it as a digital vacuum cleaner that tells you where to sweep, without actually doing the sweeping for you (safety first!).

Keeping your your repository clean improves clarity, reduces build times, and makes your project feel loved.

## ✨ Features

-   **Empty Directory Detection**: Finds and lists directories that contain no files or subdirectories.
-   **Common Junk File Identification**: Scans for well-known temporary files, build artifacts, and OS-specific clutter (e.g., `.DS_Store`, `*.log`, `__pycache__`).
-   **Smart Filtering**: Avoids listing individual files if their parent directory is already identified as a 'dust bunny' (e.g., lists `node_modules` once, not every file within it).
-   **Safe Operation**: Only lists potential 'dust bunnies'; it never deletes anything.

## 🚀 Usage

To run the sweeper, navigate to your project's root directory (or specify a path) and execute the Python script:

```bash
python src/sweeper.py [path_to_clean]
```

If `path_to_clean` is omitted, it will default to the current working directory.

### Example Output

```
Digital Dust Bunny Sweeper Report:

Potential Dust Bunnies Found:

Empty Directories:
- ./temp_empty_dir

Junk Files/Directories:
- ./.DS_Store
- ./build
- ./logs/app.log
- ./src/__pycache__
- ./temp.tmp

Consider reviewing and removing these files/directories to keep your project sparkling clean!
```

## 🛠️ Development

The utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.
