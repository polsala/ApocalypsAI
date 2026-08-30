# nightly-reality-ripple-check

A high-performance CLI tool written in Rust that recursively compares file contents across multiple directories, reporting discrepancies as "reality ripples" to ensure data harmony.

## 🌀 What are Reality Ripples?

In the ApocalypsAI universe, "reality ripples" are subtle inconsistencies in data across different temporal or spatial instances. This tool helps you detect these ripples in your file systems, ensuring that your critical configurations, codebases, or survival logs are perfectly synchronized across all your mirrored bunkers or distributed nodes.

## ✨ Features

*   **High Performance**: Built with Rust for speed and efficiency, especially when dealing with large file sets.
*   **Recursive Comparison**: Traverses subdirectories to compare files at all levels.
*   **Content-Based Hashing**: Uses SHA256 hashing to detect even the slightest content differences.
*   **Missing File Detection**: Identifies files present in some directories but absent in others.
*   **Clear Reporting**: Provides concise output detailing where ripples are found.

## 🚀 Installation

To install `nightly-reality-ripple-check`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (or download the utility folder):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-reality-ripple-check
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-reality-ripple-check`.**
    You can add it to your system's PATH for easier access:
    ```bash
    # Example for Linux/macOS
    sudo cp target/release/nightly-reality-ripple-check /usr/local/bin/
    ```

## 💡 Usage

Run the tool by providing at least two directory paths you wish to compare:

```bash
nightly-reality-ripple-check <directory1> <directory2> [directory3 ...]
```

### Examples:

**1. Comparing two identical directories:**

```bash
# Assuming dir_a and dir_b have the same files with same content
nightly-reality-ripple-check ./dir_a ./dir_b
```
Output:
```
✨ All realities are in harmony! No ripples detected.
```

**2. Detecting a content difference:**

```bash
# If 'config.txt' in dir_a is different from 'config.txt' in dir_b
nightly-reality-ripple-check ./dir_a ./dir_b
```
Output:
```
💥 RIPPLE DETECTED: File 'config.txt' has different content across directories:
  - /path/to/dir_a: <hash_a>
  - /path/to/dir_b: <hash_b>
```

**3. Detecting a missing file:**

```bash
# If 'report.log' exists in dir_a but not in dir_b
nightly-reality-ripple-check ./dir_a ./dir_b
```
Output:
```
🌀 RIPPLE DETECTED: File 'report.log' is missing in: /path/to/dir_b
```

**4. Comparing multiple directories:**

```bash
nightly-reality-ripple-check /bunker/alpha /bunker/beta /bunker/gamma
```

## 🧪 Testing

To run the automated tests for this utility:

```bash
cd ApocalypsAI/rust-utils/nightly-reality-ripple-check
cargo test
```
The tests use temporary directories and files to ensure determinism and isolation from your actual file system.
