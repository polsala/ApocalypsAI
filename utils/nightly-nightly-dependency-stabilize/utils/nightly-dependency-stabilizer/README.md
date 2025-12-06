# Nightly Dependency Stabilizer

## 🌌 Shoring Up the Temporal Integrity of Your Project's Dependencies 🌌

The quantum fabric of your project is constantly under threat from entropy and outdated dependencies. The Nightly Dependency Stabilizer is here to help! This utility scans your `requirements.txt` file, queries the PyPI cosmic archives for the latest available versions, and reports any temporal fluctuations (i.e., outdated pinned dependencies) that could lead to a quantum quake.

Keep your project's timeline stable and secure by staying up-to-date!

### How to Use

1.  **Navigate to your project directory**:
    ```bash
    cd /path/to/your/project
    ```
2.  **Run the stabilizer**:
    ```bash
    python src/stabilizer.py
    ```
    (Or specify a path if not in the project root)
    ```bash
    python src/stabilizer.py --project-path /path/to/another/project
    ```

### Example Output

```
Scanning /path/to/your/project/requirements.txt for quantum fluctuations...
Warning: Could not fetch info for non-existent-package from PyPI: 404 Client Error: Not Found for url: ...

--- Quantum Fluctuation Report ---
🚨 requests: Pinned to 2.28.1, but 2.29.0 is available! Consider `pip install requests==2.29.0`
✅ flask: Pinned to 1.1.0, which is the latest available (1.1.0).
✨ rich: Not pinned, latest available is 13.7.0.
❓ non-existent-package: Could not determine status. PyPI information unavailable.

Temporal integrity compromised! Consider applying the suggested updates to stabilize the project.
```

### Supported Dependency Files

Currently, this utility focuses on `requirements.txt` files. Ensure your project's Python dependencies are listed there for the stabilizer to work its magic.
