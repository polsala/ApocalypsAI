# Nightly Digital Dust Bunny Sweeper

## 🐰 Sweep Away Digital Clutter with Whimsical Efficiency!

`nightly-digital-dust-bunny-sweeper` is a blazing-fast Rust CLI utility designed to help you identify and manage those forgotten, old files that accumulate over time – your 'digital dust bunnies'. It scans specified directories, highlights files that haven't been touched in a while, and offers options to 'cuddle' (archive), 'release' (delete), or interactively manage them.

### ✨ Features

*   **High Performance**: Built with Rust for rapid file system traversal and processing.
*   **Configurable Age**: Define what constitutes an 'old' file by specifying an age threshold in days.
*   **Flexible Actions**: Choose to list, archive, delete, or interactively manage identified files.
*   **Safety First**: Deletion requires explicit confirmation to prevent accidental data loss.
*   **Whimsical Interface**: Friendly output to make digital hygiene a little more fun.

### 🚀 Installation

To install the `nightly-digital-dust-bunny-sweeper`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-digital-dust-bunny-sweeper
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny-sweeper
cargo build --release
# The executable will be in target/release/nightly-digital-dust-bunny-sweeper
```

### 💡 Usage

```bash
dust-bunny-sweeper [OPTIONS]
```

**Arguments:**

*   `-p`, `--path <PATH>`: Path to scan for dust bunnies. Defaults to the current directory (`.`).
*   `-a`, `--age-days <DAYS>`: Files older than this many days are considered dust bunnies. Defaults to `30`.

**Actions (choose one or use interactive mode):**

*   `-i`, `--interactive`: Enable interactive mode to choose an action for each dust bunny individually.
*   `--cuddle-to <DIRECTORY>`: Move all found dust bunnies to the specified archive directory. Overrides interactive mode.
*   `--release-all`: Delete all found dust bunnies. **Requires `--confirm-release` for safety.** Overrides interactive mode.
*   `--confirm-release`: Confirm deletion when using `--release-all`.

If no action flag (`--interactive`, `--cuddle-to`, `--release-all`) is provided, the tool will simply **list** the identified dust bunnies.

### Examples

1.  **List all files in the current directory older than 60 days:**

    ```bash
dust-bunny-sweeper -a 60
    ```

2.  **Interactively manage files in your `~/Downloads` folder older than 7 days:**

    ```bash
dust-bunny-sweeper -p ~/Downloads -a 7 --interactive
    ```

    *When in interactive mode, you'll be prompted for each file:* 
    ```
    👉 Dust Bunny: /home/user/Downloads/old_report.pdf
      Modified: 2023-01-15 10:30:00 (320 days ago)
      Size: 123456 bytes
    What to do with this dust bunny? [Cuddle (Move to archive), Release (Delete), Ignore]
    ```

3.  **Cuddle (archive) all files in `/var/log` older than 90 days to `~/log_archive`:**

    ```bash
dust-bunny-sweeper -p /var/log -a 90 --cuddle-to ~/log_archive
    ```

4.  **Release (delete) all files in `~/temp` older than 1 day (use with caution!):**

    ```bash
dust-bunny-sweeper -p ~/temp -a 1 --release-all --confirm-release
    ```

### ⚠️ Safety Warning

Using `--release-all` will permanently delete files. Always double-check your arguments and consider using `--interactive` or `--cuddle-to` for safer management of your digital space.
