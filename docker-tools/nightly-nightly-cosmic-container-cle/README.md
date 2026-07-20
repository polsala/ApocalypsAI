# Nightly Cosmic Container Cleaner

## 🌌 Purge the Cosmic Dust from Your Docker Universe! 🌌

The Nightly Cosmic Container Cleaner is a whimsical yet powerful utility designed to keep your Docker environment sparkling clean. Over time, your Docker universe can accumulate "cosmic dust" – unused containers, dangling images, orphaned volumes, and forgotten networks. This tool helps you sweep it all away, reclaiming precious disk space and ensuring your Docker operations run smoothly.

## ✨ Features

*   **Comprehensive Cleanup:** Leverages `docker system prune` to remove all stopped containers, all dangling images, all unused networks, and optionally all unused volumes.
*   **Dry Run Mode:** Safely preview what would be cleaned without actually deleting anything, allowing you to assess the cosmic dust before purging.
*   **Whimsical Reporting:** Provides delightful messages about the clarity achieved in your Docker universe.

## 🚀 Usage

To run the Cosmic Container Cleaner, simply execute the script.

```bash
./src/cosmic_cleaner.sh
```

### Dry Run Mode

To see what would be cleaned without making any changes, use the `--dry-run` option:

```bash
./src/cosmic_cleaner.sh --dry-run
```

### Help

For usage instructions and options:

```bash
./src/cosmic_cleaner.sh --help
```

## 🌠 Example Output

### Successful Cleanup

```
🌌 Initiating Cosmic Container Cleanup Protocol... 🌌
🚀 Engaging stellar thrusters for deep space cleanup... 🚀
✨ Success! We've swept away 1.2GB of cosmic dust.
🌠 Your Docker universe is now sparkling clean and ready for new adventures!
```

### Dry Run

```
🌌 Initiating Cosmic Container Cleanup Protocol... 🌌
✨ Performing a stellar scan (dry run mode)... ✨
🌠 The Cosmic Scanner predicts: 500MB of cosmic dust could be cleared.
🌟 Your Docker universe is poised for clarity!
```

### No Dust Found

```
🌌 Initiating Cosmic Container Cleanup Protocol... 🌌
🚀 Engaging stellar thrusters for deep space cleanup... 🚀
✨ No cosmic dust found. Your Docker universe was already pristine!
```

## 🛠️ Development & Testing

The utility is a simple bash script. Ensure you have Docker installed if you intend to run it against a live environment.

### Running Tests

The tests are self-contained bash scripts that mock the `docker` command to ensure deterministic and offline execution.

```bash
./tests/test_cosmic_cleaner.sh
```

---

*May your Docker universe always be free of cosmic dust!*
