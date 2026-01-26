# Nightly Byte-Broom

A whimsical CLI tool to sweep away digital dust bunnies (large or old files) from your file system.

## ✨ What it Does ✨

`nightly-byte-broom` helps you identify files that are taking up significant space or have been untouched for a long time, presenting them as 'digital dust bunnies'. It's a fun way to keep your digital environment tidy and reclaim precious disk space.

## 🧹 Features

*   **Size-based filtering**: Find files larger than a specified threshold (e.g., 10MB, 1GB).
*   **Age-based filtering**: Discover files older than a certain duration (e.g., 30 days, 1 year).
*   **Recursive scanning**: Sweeps through directories and their subdirectories.
*   **Whimsical output**: Reports findings with a touch of charm.

## 🚀 Installation

To install `nightly-byte-broom`, you'll need [Rust](https://www.rust-lang.org/tools/install) installed on your system.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-byte-broom
    ```

2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-byte-broom` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## 💡 Usage

Run `nightly-byte-broom` from your terminal. You can specify the directory to sweep, minimum size, and minimum age.

```bash
nightly-byte-broom [OPTIONS] [PATH]
```

### Arguments:

*   `<PATH>`: The directory to sweep. Defaults to the current directory (`.`).

### Options:

*   `-s, --min-size <MIN_SIZE>`: Minimum size for a file to be considered a dust bunny. Accepts units like `KB`, `MB`, `GB`, `TB` (case-insensitive). Examples: `10MB`, `1GB`, `500k`. Default: `10MB`.
*   `-a, --min-age <MIN_AGE>`: Minimum age for a file to be considered a dust bunny. Accepts units like `d` (days), `w` (weeks), `m` (months, approx. 30 days), `y` (years, approx. 365 days). Examples: `30d`, `1y`, `2w`. Default: `30d`.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples:

1.  **Sweep the current directory for files larger than 50MB and older than 60 days:**
    ```bash
    nightly-byte-broom -s 50MB -a 60d
    ```

2.  **Sweep a specific directory (`~/Downloads`) for files larger than 1GB and older than 1 year:**
    ```bash
    nightly-byte-broom ~/Downloads -s 1GB -a 1y
    ```

3.  **Find any file older than 90 days, regardless of size (by setting a very small size threshold):**
    ```bash
    nightly-byte-broom -s 1KB -a 90d
    ```

## 🌟 Example Output

```
Sweeping for digital dust bunnies in '/home/user/documents/'...
  (Looking for files >= 10.00 MB and >= 30d old)

🧹 Found some digital dust bunnies lurking around:
  - A forgotten relic: /home/user/documents/old_project_backup.zip (25.50 MB, 120 days old)
  - A forgotten relic: /home/user/documents/archive/ancient_logs.tar.gz (150.20 MB, 365 days old)

Consider giving these digital dust bunnies a new home (the recycle bin) or a good scrub!
```

```
Sweeping for digital dust bunnies in '.'...
  (Looking for files >= 10.00 MB and >= 30d old)

✨ The digital realm is sparkling clean! No dust bunnies found. ✨
```
