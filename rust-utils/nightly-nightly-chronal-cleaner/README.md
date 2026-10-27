# nightly-chronal-cleaner

A high-performance Rust CLI tool designed to detect and purge "temporal echoes" (stale or unaccessed files) from your filesystem, preventing chronal drift and maintaining digital stability in the post-apocalyptic data-scape.

## 🌌 The Whimsical Lore

In the chaotic aftermath, data itself can become unstable. Files, once vibrant with purpose, can linger as "temporal echoes" – forgotten, unaccessed, or simply too ancient to be relevant. These echoes consume precious storage and, if left unchecked, can lead to "chronal drift," where your filesystem's timeline becomes distorted and unreliable.

The `nightly-chronal-cleaner` is your trusty chronometer and broom, meticulously scanning for these digital specters and offering to sweep them away, restoring temporal coherence to your data caches.

## ✨ Features

*   **Temporal Echo Detection**: Identify files based on their last modification, creation, or access times.
*   **Configurable Thresholds**: Define what constitutes an "echo" by specifying age in days.
*   **Dry Run Mode**: Safely preview which files would be affected before any deletion occurs.
*   **Interactive Purge**: Confirm deletions to prevent accidental data loss.
*   **High Performance**: Built with Rust for speed and efficiency, even on large filesystems.

## 🚀 Installation

To build and run this utility, you'll need [Rust](https://www.rust-lang.org/tools/install) installed.

1.  **Clone the repository:**
    ```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chronal-cleaner
    ```
2.  **Build the project:**
    ```bash
cargo build --release
    ```
3.  **The executable will be located at:** `./target/release/nightly-chronal-cleaner`

## 🛠️ Usage

```bash
nightly-chronal-cleaner --help
```

### Examples:

1.  **Dry run: Find files in `/tmp/data` modified or created more than 30 days ago:**
    ```bash
./target/release/nightly-chronal-cleaner --path /tmp/data --older-than 30
    ```
    (This will only list files, no deletion will occur.)

2.  **Dry run: Find files in `/var/log` not accessed in the last 90 days:**
    ```bash
./target/release/nightly-chronal-cleaner --path /var/log --not-accessed-in 90
    ```

3.  **Purge: Delete files in `/tmp/cache` older than 7 days (requires confirmation):**
    ```bash
./target/release/nightly-chronal-cleaner --path /tmp/cache --older-than 7 --delete
    ```
    You will be prompted to confirm the deletion.

4.  **Purge: Delete files in `/home/user/downloads` not accessed in 180 days, with verbose output:**
    ```bash
./target/release/nightly-chronal-cleaner --path /home/user/downloads --not-accessed-in 180 --delete --verbose
    ```

### Arguments:

*   `-p, --path <DIR>`: **Required.** Path to the directory to scan for temporal echoes.
*   `--older-than <DAYS>`: Detects files whose last modification or creation time is more than `N` days ago.
*   `--not-accessed-in <DAYS>`: Detects files that have not been accessed in `N` days.
*   `-d, --dry-run`: (Default: `true`) Perform a dry run, only report files, do not delete.
*   `-D, --delete`: (Default: `false`) Actually delete the detected files. **Requires `--older-than` or `--not-accessed-in` to be specified.** Cannot be used with `--dry-run`.
*   `-v, --verbose`: Show more detailed output, including individual file purge messages.

## 🧪 Testing

To run the automated tests:

```bash
cargo test
```
