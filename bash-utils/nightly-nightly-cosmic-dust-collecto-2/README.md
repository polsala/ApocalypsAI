# Nightly Cosmic Dust Collector

## 🌌 Sweep Away Digital Detritus with Cosmic Grace 🌌

The digital universe, much like its celestial counterpart, accumulates its fair share of "cosmic dust" – forgotten temporary files, ancient logs, and desolate empty directories. The `Nightly Cosmic Dust Collector` is your whimsical yet powerful assistant, designed to gracefully sweep away this digital detritus, ensuring your system remains pristine and efficient.

It's not just cleanup; it's a cosmic tidying ritual!

## ✨ Features

*   **Whimsical Cleanup**: Transforms mundane file deletion into a celestial event.
*   **Targeted Sweeping**: Specify directories to cleanse of digital dust.
*   **Age-Based Filtration**: Only target files and directories older than a specified number of "cosmic cycles" (days).
*   **Dry Run Mode**: Preview the cosmic sweep before committing to the void, ensuring no vital stardust is accidentally collected.
*   **Empty Directory Vanishing**: Automatically identifies and removes empty directories, reclaiming digital space.

## 🚀 Usage

```bash
./src/cosmic_dust_collector.sh [OPTIONS] --target <directory>
```

### Options:

*   `-t, --target <directory>`: **Required.** The directory path to scan for cosmic dust. Can be specified multiple times.
*   `-a, --age <days>`: Collects files and empty directories older than `<days>` (default: 7 days).
*   `-d, --dry-run`: Perform a dry run. Show what *would* be collected without actually deleting anything.
*   `-h, --help`: Display this help message.

### Examples:

1.  **Dry run in your home directory for dust older than 30 days:**
    ```bash
    ./src/cosmic_dust_collector.sh --dry-run --age 30 --target ~/
    ```

2.  **Collect dust in `/tmp` and `/var/log` older than 14 days:**
    ```bash
    ./src/cosmic_dust_collector.sh --age 14 --target /tmp --target /var/log
    ```

3.  **Simply remove all empty directories in the current path:**
    ```bash
    ./src/cosmic_dust_collector.sh --age 0 --target .
    ```

## ⚠️ Cosmic Caution

Always use `--dry-run` first, especially when targeting critical directories. The ApocalypsAI is not responsible for accidental cosmic voiding of essential data. Use with wisdom!

## 🛠️ Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
./tests/test_cosmic_dust_collector.sh
```
