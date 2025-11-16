# ApocalypsAI Nightly Resource Scavenger

## 📦 Utility: `nightly-resource-scavenger`

The digital wasteland is vast and full of forgotten data. The Nightly Resource Scavenger is your trusty companion for sifting through the rubble, identifying valuable text-based resources, and compiling them into a concise report. Whether you're looking for lost logs, forgotten notes, or critical configuration files, this utility will help you gather your digital supplies.

### 🌟 Features

*   **Targeted Scavenging**: Specify a list of file extensions to focus your search.
*   **Directory Traversal**: Recursively scans through subdirectories to uncover hidden gems.
*   **Content Snippets**: Extracts and includes a configurable number of lines from text files directly into the report.
*   **Binary File Handling**: Gracefully skips content extraction for binary files, noting their presence.
*   **Consolidated Report**: Generates a single, easy-to-read text file summarizing all found resources.

### 🛠️ How to Use

This utility is a Python 3.11 script and can be run directly from the command line.

#### Prerequisites

*   Python 3.11 or higher

#### Running the Scavenger

Navigate to the `utils/nightly-resource-scavenger/src` directory and execute `scavenger.py`:

```bash
python scavenger.py <directory_to_scavenge> [OPTIONS]
```

**Arguments:**

*   `<directory_to_scavenge>`: The root directory where the scavenger will begin its search.

**Options:**

*   `-e`, `--extensions`: A space-separated list of file extensions to look for (e.g., `.txt .md .log`).
    *   *Default*: `.txt .md .log .json .yaml .yml`
*   `-o`, `--output`: The path to the output report file.
    *   *Default*: `scavenger_report.txt` (will be created in the current working directory)
*   `-l`, `--lines`: Maximum number of content lines to include per text file in the report.
    *   *Default*: `5`

#### Examples

1.  **Scavenge current directory for default file types:**
    ```bash
    python scavenger.py .
    ```

2.  **Scavenge a specific directory for `.txt` and `.csv` files, saving report to `my_findings.txt`:**
    ```bash
    python scavenger.py /path/to/my/data -e .txt .csv -o my_findings.txt
    ```

3.  **Scavenge with more content lines from each file:**
    ```bash
    python scavenger.py /path/to/project -e .py .js -l 10
    ```

### 🧪 Testing

To ensure the Nightly Resource Scavenger is always ready for deployment, run its self-contained tests.

Navigate to the `utils/nightly-resource-scavenger/tests` directory and execute `test_scavenger.py`:

```bash
python -m unittest test_scavenger.py
```

The tests are designed to be deterministic and run offline, using mocks for all file system interactions.
