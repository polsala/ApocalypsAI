# Nightly Link Stabilizer

## 🌌 Whimsical Purpose: Quantum Entanglement Link Stabilizer

In the chaotic dance of the ApocalypsAI repository, links can decay, much like quantum particles losing their entanglement. The Nightly Link Stabilizer acts as a cosmic beacon, scanning your project's documentation and code to ensure all references remain perfectly entangled and functional. It's like a digital chiropractor for your codebase, aligning every link to its true destination.

## 🛠️ Practical Utility

This utility scans a specified directory for Markdown files (`.md`) and extracts both external HTTP/HTTPS links and internal file-system links. It then verifies their reachability and existence, reporting any broken connections. This helps maintain high-quality documentation, prevents dead ends for users, and ensures code references are always valid.

### Features:

*   **External Link Validation**: Checks if HTTP/HTTPS URLs return a successful status code (2xx/3xx).
*   **Internal Link Validation**: Verifies if relative or absolute file paths within Markdown files point to existing files.
*   **Recursive Scanning**: Traverses subdirectories to find all relevant files.
*   **Clear Reporting**: Outputs a summary of broken links with their source files.

## 🚀 Usage

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-link-stabilizer/src
    ```
2.  **Run the script with the target directory:**
    ```bash
    python link_stabilizer.py --path /path/to/your/repository/root
    ```

    Replace `/path/to/your/repository/root` with the actual path to the directory you want to scan. For example, to scan the current repository:
    ```bash
    python link_stabilizer.py --path ../../
    ```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start scanning for Markdown files.

## 📝 Example Output

```
Scanning directory: /path/to/your/repository/root

--- Checking links in: docs/guide.md ---
  ✅ External: https://github.com/polsala/ApocalypsAI
  ❌ External: https://broken-link.example.com (Status: 404 Not Found)
  ❌ Internal: ../non-existent-file.md (File not found)
  ✅ Internal: ../README.md

--- Checking links in: src/agent_notes.md ---
  ✅ External: https://docs.python.org/3/

--- Scan Complete ---
Found 2 broken links across 2 files:

File: docs/guide.md
  - Broken External: https://broken-link.example.com (Status: 404 Not Found)
  - Broken Internal: ../non-existent-file.md (File not found)

No issues found in src/agent_notes.md
```
