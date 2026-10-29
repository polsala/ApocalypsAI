# nightly-digital-dust-bunny-sweeper

## 🧹 Digital Dust Bunny Sweeper 🧹

Are your digital spaces feeling a bit cluttered? Do forgotten files and directories lurk in the dark corners of your filesystem, gathering virtual dust? Fear not, for the `nightly-digital-dust-bunny-sweeper` is here to help!

This whimsical utility identifies old, unused files and directories (your "digital dust bunnies") based on their last modification time. It then presents them to you with gentle suggestions for "composting," "rehoming," or simply "dusting" them off.

### ✨ Features

*   **Identifies Digital Dust Bunnies**: Scans a specified directory for files and folders older than a given age.
*   **Whimsical Suggestions**: Provides playful recommendations for managing your digital clutter.
*   **Safe & Non-Destructive**: By default, it only *lists* and *suggests* actions. It won't delete or move anything without explicit future enhancements (not in this version!).
*   **Bash-Powered**: A lightweight, self-contained shell script for easy integration into your nightly routines.

### 🚀 Usage

To run the sweeper, simply execute the `dust_bunny_sweeper.sh` script.

```bash
./src/dust_bunny_sweeper.sh [options]
```

#### Options:

*   `-d <directory>`: The directory to sweep for digital dust bunnies.
    *   *Default*: The current working directory (`.`).
*   `-a <age_in_days>`: Files and directories older than this many days will be considered "dust bunnies."
    *   *Default*: `90` days.
*   `-h`: Display the help message and exit.

#### Examples:

1.  **Sweep the current directory for items older than 90 days (default):**
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

2.  **Sweep your `/home/user/downloads` directory for items older than 30 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /home/user/downloads -a 30
    ```

3.  **Check your entire `/var/log` directory for logs older than a year (365 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /var/log -a 365
    ```

### 🧪 Testing

To run the automated tests, execute the `test_dust_bunny_sweeper.sh` script:

```bash
./tests/test_dust_bunny_sweeper.sh
```

The tests use a mocked `find` command to ensure determinism and avoid actual filesystem modifications. This allows for reliable and fast testing without needing to create temporary files with specific timestamps.

### 💖 Contributing

Feel free to suggest new whimsical actions, additional filtering options, or even a "digital vacuum cleaner" mode (with appropriate safety warnings, of course!).
