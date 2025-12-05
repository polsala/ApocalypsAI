# Nightly Echo Chamber Resonator

## 🌌 Resonate with Clarity: Unmasking Digital Echoes 🌌

The Nightly Echo Chamber Resonator is a whimsical-yet-useful utility designed to help you declutter your digital space by identifying and reporting duplicate files within a specified directory. Just as an echo chamber amplifies sounds, your file system can inadvertently amplify redundant data, consuming precious storage and obscuring unique information. This tool helps you find those echoes!

### ✨ Features

*   **Duplicate Detection**: Scans a target directory and its subdirectories for files with identical content.
*   **Hashing Algorithms**: Supports MD5, SHA1 (SHA1), and SHA256 for robust content comparison.
*   **Clear Reporting**: Presents a list of duplicate file sets, grouped by their content hash.
*   **Self-Contained**: Written in Python 3.11, requiring only standard library modules.

### 🚀 Usage

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-echo-chamber-resonator
    ```

2.  **Run the resonator**:
    Specify the directory you wish to scan.

    ```bash
    python src/resonator.py /path/to/your/directory
    ```

    **Example**:
    ```bash
    python src/resonator.py ~/Documents/MyProject
    ```

3.  **Choose a hashing algorithm (optional)**:
    By default, `md5` is used. You can specify `sha1` or `sha256` for potentially stronger collision resistance (though `md5` is generally sufficient for duplicate file detection).

    ```bash
    python src/resonator.py /path/to/your/directory --hash-algo sha256
    ```

### 🧪 Testing

To ensure the Nightly Echo Chamber Resonator is functioning correctly, you can run its self-contained tests:

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-echo-chamber-resonator
    ```

2.  **Run the tests**:
    ```bash
    python -m unittest tests/test_resonator.py
    ```

    All tests are deterministic and offline, using Python's `unittest.mock` to simulate file system operations and content without touching your actual disk.

### 📜 Philosophy

In the spirit of ApocalypsAI, this utility embodies "Anarchy with discipline." It's a standalone, focused tool that provides a clear, testable function for community benefit, helping to maintain order amidst potential digital chaos.
