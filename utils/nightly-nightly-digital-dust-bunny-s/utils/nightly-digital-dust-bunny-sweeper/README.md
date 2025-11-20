# ApocalypsAI Nightly Digital Dust Bunny Sweeper

![Dust Bunny Sweeper Logo](https://raw.githubusercontent.com/polsala/ApocalypsAI/main/docs/assets/dust_bunny_sweeper.png)
*(Image is illustrative, not actually generated)*

## 🧹 What is it?

The Nightly Digital Dust Bunny Sweeper is a whimsical yet practical utility designed to help you maintain a pristine filesystem. It recursively scans a specified directory and removes any empty folders, metaphorically sweeping away the 'digital dust bunnies' that accumulate over time from forgotten projects, build artifacts, or refactoring efforts.

Keeping your directories free of empty clutter can improve navigation, reduce cognitive load, and ensure your repository remains as lean as possible, ready for the next apocalyptic challenge.

## ✨ Features

*   **Recursive Cleaning**: Scans deeply into nested directories.
*   **Safe Operation**: Only removes truly empty directories.
*   **Dry Run Mode**: Preview which directories *would* be removed without actually deleting anything.
*   **Self-contained**: Written in Python, requiring no external dependencies beyond standard library modules.

## 🚀 How to Use

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-sweeper
    ```

2.  **Run (Dry Run Mode)**: To see which directories would be removed without making any changes:
    ```bash
    python src/sweeper.py /path/to/your/target/directory --dry-run
    ```
    Replace `/path/to/your/target/directory` with the actual path you want to clean.

3.  **Run (Actual Cleaning)**: To permanently remove empty directories:
    ```bash
    python src/sweeper.py /path/to/your/target/directory
    ```
    **Caution**: Always use `--dry-run` first to ensure you understand what will be deleted. This tool will not delete directories containing files.

### Example:

Let's say you have the following structure:

```
my_project/
├── src/
│   └── main.py
├── build/
│   └── temp/
│       └── (empty)
├── docs/
│   └── (empty)
└── old_features/
    └── feature_x/
        └── (empty)
```

Running `python src/sweeper.py my_project` would result in:

```
my_project/
├── src/
│   └── main.py
├── build/
└── old_features/
```

`build/temp`, `docs`, and `old_features/feature_x` would be removed because they were empty. `old_features` would also be removed if `feature_x` was its only content and it became empty after `feature_x`'s removal.

## 🧪 Development & Testing

To run the tests for this utility:

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-sweeper
    ```

2.  **Run Tests**:
    ```bash
    python -m unittest tests/test_sweeper.py
    ```

Tests are self-contained and use temporary directories to ensure no actual filesystem changes occur during testing.
