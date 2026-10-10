# Nightly Digital Dust Bunny Sweeper

## 🧹 What is this?

In the digital realm, just like in your cozy abode, tiny, forgotten files accumulate in the nooks and crannies of your filesystem. We call them "Digital Dust Bunnies"! They're harmless, but they can clutter up your system and take up precious space. The `nightly-dust-bunny-sweeper` is your trusty automated broom, designed to gently (or not so gently, if you prefer!) sweep these digital fluff balls into the void.

It's a whimsical-yet-useful Bash script that identifies and optionally removes files older than a specified age from designated directories.

## ✨ Features

*   **Configurable Scan Paths**: Specify which directories to sweep.
*   **Adjustable Age Threshold**: Define how old a file must be to be considered a "dust bunny".
*   **Dry Run Mode**: See what would be swept without actually deleting anything.
*   **Interactive Confirmation**: Get a chance to review and confirm before the sweep begins.
*   **Whimsical Output**: Enjoy a bit of fun while keeping your system tidy.

## 🚀 Installation

Simply copy the `dust_bunny_sweeper.sh` script to a directory in your `PATH` (e.g., `/usr/local/bin`) and make it executable:

```bash
# Assuming you are in the directory containing the script
mkdir -p ~/.local/bin
cp src/dust_bunny_sweeper.sh ~/.local/bin/
chmod +x ~/.local/bin/dust_bunny_sweeper.sh

# Add ~/.local/bin to your PATH if it's not already there
# echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
# source ~/.bashrc
```

## 📖 Usage

```bash
nightly-dust-bunny-sweeper [OPTIONS]
```

### Options:

*   `-c <config_file>`: Specify a custom configuration file path. Defaults to `~/.config/dust_bunny_sweeper.conf`.
*   `-d <directory>`: Add a directory to scan. Can be used multiple times. Overrides directories specified in the config file if used.
*   `-a <days>`: Set the age threshold in days. Files older than this will be considered dust bunnies. Defaults to 7 days.
*   `-n`: No dry run. Perform the actual sweep (requires confirmation).
*   `-h`: Display help message.

### Examples:

1.  **Perform a dry run (default behavior) in default directories with default age (7 days):**
    ```bash
    nightly-dust-bunny-sweeper
    ```

2.  **Perform a dry run in `/var/log` for files older than 30 days:**
    ```bash
    nightly-dust-bunny-sweeper -d /var/log -a 30
    ```

3.  **Actually sweep files older than 14 days from `/tmp` and `~/Downloads` (with confirmation):**
    ```bash
    nightly-dust-bunny-sweeper -d /tmp -d ~/Downloads -a 14 -n
    ```

4.  **Use a custom configuration file:**
    ```bash
    nightly-dust-bunny-sweeper -c /etc/dust_bunny_sweeper.conf
    ```

## ⚙️ Configuration File

The sweeper looks for a configuration file at `~/.config/dust_bunny_sweeper.conf` by default. You can override this with the `-c` option. The file should contain Bash variable assignments:

```bash
# Example: ~/.config/dust_bunny_sweeper.conf

# Directories to scan (space-separated)
SCAN_DIRS="/tmp /var/log/old_logs"

# Age threshold in days
AGE_DAYS=30
```

**Note**: Command-line arguments (`-d`, `-a`) will always override settings from the configuration file.

## ⚠️ Safety First!

Always run a dry run first to see what files will be affected. The script will ask for confirmation before deleting files when `-n` is used. Use with caution, as deleted files are generally unrecoverable.
