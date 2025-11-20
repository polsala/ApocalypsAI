# ApocalypsAI Nightly Chronicle Keeper

## 📜 Overview

In the chaotic aftermath, every observation, every discovery, every critical event needs to be recorded. The ApocalypsAI Nightly Chronicle Keeper is your trusty digital quill, allowing you to log timestamped entries into a central 'chronicle' file. Whether you're tracking resource depletion, documenting strange anomalies, or simply noting your daily progress, this utility ensures your records are organized and easily reviewable.

It's a simple, self-contained command-line tool designed for quick logging and retrieval of vital information.

## ✨ Features

*   **Timestamped Entries**: Every log entry is automatically prefixed with a precise date and time.
*   **Append-Only**: Ensures the integrity of your chronicle by only adding new entries.
*   **Customizable Chronicle File**: Specify any file path for your chronicle, allowing for multiple logs.
*   **View Last Entries**: Quickly review the most recent entries in your chronicle.
*   **Lightweight & Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 Installation

This utility is self-contained. Simply copy the `chronicle_keeper.py` file into your desired location, or run it directly from its `src/` directory.

```bash
# Navigate to the utility's directory
cd utils/nightly-chronicle-keeper

# You can then run it directly
python3 src/chronicle_keeper.py --help
```

## 🛠️ Usage

The `chronicle_keeper.py` script supports two main commands: `append` and `view`.

### Appending an Entry

To add a new entry to your chronicle:

```bash
python3 src/chronicle_keeper.py append "Discovered a new cache of canned beans near sector 7G."
```

By default, entries are saved to `chronicle.log` in the current directory. To specify a different chronicle file:

```bash
python3 src/chronicle_keeper.py -f logs/my_personal_log.txt append "The sky turned an unusual shade of green today."
```

### Viewing Entries

To view the last 10 entries (default) from your chronicle:

```bash
python3 src/chronicle_keeper.py view
```

To view a specific number of last entries (e.g., the last 5):

```bash
python3 src/chronicle_keeper.py view -n 5
```

To view entries from a specific chronicle file:

```bash
python3 src/chronicle_keeper.py -f logs/my_personal_log.txt view -n 3
```

## 🧪 Testing

To run the automated tests for this utility, navigate to the `utils/nightly-chronicle-keeper` directory and execute:

```bash
python3 -m unittest tests/test_chronicle_keeper.py
```

All tests are deterministic and offline, using mocks to simulate file system operations and time.

## 🤝 Contributing

Feel free to suggest improvements or report issues. Contributions are welcome, provided they adhere to the ApocalypsAI philosophy of self-contained, tested, and documented utilities.
