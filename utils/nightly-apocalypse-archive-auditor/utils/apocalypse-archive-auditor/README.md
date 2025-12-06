# Apocalypse Archive Auditor

## 📜 Overview

In the face of impending digital oblivion, the Apocalypse Archive Auditor is your last line of defense against data chaos! This whimsical-yet-useful utility scans your designated directories, providing a swift and insightful summary of your digital hoard. Know exactly what files you have, how much space they consume, and which ones are the true behemoths, so you can prioritize what to save, share, or simply marvel at before the servers inevitably melt.

It's like a digital pre-apocalyptic inventory check, ensuring your most vital cat videos and survival guides are accounted for.

## ✨ Features

*   **File Type Breakdown**: Get a count and total size for each file extension found.
*   **Top N Largest Files**: Quickly identify the biggest files hogging your precious storage.
*   **Directory Scan**: Recursively scans subdirectories to give you a complete picture.
*   **Customizable Depth**: Control how deep the auditor digs into your directory structure.

## 🚀 Usage

### Prerequisites

*   Python 3.8+

### Running the Auditor

1.  Navigate to the `apocalypse-archive-auditor` directory.
2.  Run the `auditor.py` script with the target directory:

    ```bash
    python src/auditor.py --path /path/to/your/archive [--depth <int>] [--top-n <int>]
    ```

    *   `--path`: (Required) The path to the directory you want to audit.
    *   `--depth`: (Optional) Maximum recursion depth. `0` for current directory only, `1` for current + immediate subdirectories, etc. Default is `None` (unlimited).
    *   `--top-n`: (Optional) Number of largest files to list. Default is `5`.

### Example

```bash
python src/auditor.py --path ~/my_precious_data --depth 2 --top-n 10
```

This will scan `~/my_precious_data` and its subdirectories up to 2 levels deep, listing the 10 largest files found.

## 🧪 Testing

To run the tests, navigate to the `apocalypse-archive-auditor` directory and execute:

```bash
python -m unittest tests/test_auditor.py
```

The tests use mock file systems to ensure deterministic and offline execution.
