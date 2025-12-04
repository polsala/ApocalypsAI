# Nightly Config Fossil Cleaner

## ⛏️ Unearthing Pristine Configurations from the Digital Strata ⛏️

The `Nightly Config Fossil Cleaner` is a whimsical yet essential utility designed to help you maintain clean, readable, and efficient configuration files. Over time, config files can accumulate 'digital fossils' – ancient comments, empty lines, and deprecated settings that clutter the landscape and obscure the active directives. This tool acts as your personal archaeological assistant, meticulously excavating and purifying your configurations.

### ✨ Features

*   **Comment Excavation**: Removes full-line comments (lines starting with common comment characters like `#` or `;`). Inline comments are preserved.
*   **Empty Line Purge**: Eliminates superfluous empty lines, compacting your configuration.
*   **Optional Backup**: Creates a `.bak` file before modifying the original, ensuring your historical data is safe.
*   **Configurable Comment Characters**: Easily extendable to recognize other comment prefixes.

### 🚀 How to Use

Run the script from your terminal, providing the path to the configuration file you wish to clean.

```bash
python src/fossil_cleaner.py <input_file_path> [--output <output_file_path>] [--backup] [--comment-chars <char1> <char2> ...]
```

**Arguments:**

*   `<input_file_path>`: The path to the configuration file to be cleaned.
*   `--output <output_file_path>`: (Optional) Specify an output file path. If not provided, the input file will be overwritten (with `--backup` if specified).
*   `--backup`: (Optional) If provided, a backup of the original file will be created with a `.bak` extension before cleaning.
*   `--comment-chars <char1> <char2> ...`: (Optional) A space-separated list of characters to treat as comment prefixes. Defaults to `#` and `;`.

### 💡 Examples

1.  **Clean a file and overwrite it with a backup:**
    ```bash
    python src/fossil_cleaner.py my_app.conf --backup
    ```

2.  **Clean a file and save to a new file:**
    ```bash
    python src/fossil_cleaner.py old_settings.ini --output new_settings.ini
    ```

3.  **Clean a file, recognizing `//` as a comment character:**
    ```bash
    python src/fossil_cleaner.py config.jsonc --comment-chars # ; //
    ```

### 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_fossil_cleaner.py
```
