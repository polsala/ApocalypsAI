# Apocalypse Snack Sorter

## 🍪 Your Last-Minute Munchie Manager 🍫

In the face of impending doom (or just a really busy week), don't let your precious emergency snacks go to waste! The Apocalypse Snack Sorter is a whimsical-yet-vital CLI utility designed to help you manage your survival provisions, track expiry dates, and ensure optimal munchie consumption before the cosmic clock runs out.

Because even during the apocalypse, nobody wants stale crackers.

### Features

*   **Add Snacks**: Easily log new snacks with their name, quantity, and crucial expiry date.
*   **List Stash**: View your entire snack inventory, sorted by expiry.
*   **Urgent Munchies**: Get recommendations on which snacks to devour first to beat the expiry clock.
*   **Persistent Storage**: Your snack data is saved locally, so your stash is always remembered.
*   **Apocalyptic Humor**: A dash of dark humor to keep your spirits up while you sort your sustenance.

### Installation

This utility requires Python 3.8+ (tested with 3.11).

1.  Navigate to the `utils/apocalypse-snack-sorter` directory.
2.  (Optional, but recommended) Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  No external dependencies are required beyond Python's standard library.

### Usage

Run the `snack_sorter.py` script directly:

```bash
python3 src/snack_sorter.py --help
```

#### Commands:

*   **`add`**: Add a new snack to your inventory.
    ```bash
    python3 src/snack_sorter.py add --name "Cosmic Crisps" --quantity 5 --expiry "2024-12-31"
    ```
    *   `--name`: Name of the snack (e.g., "Survival S'mores").
    *   `--quantity`: Number of units (e.g., 3).
    *   `--expiry`: Expiry date in YYYY-MM-DD format (e.g., "2025-06-15").

*   **`list`**: Display all snacks, sorted by expiry date.
    ```bash
    python3 src/snack_sorter.py list
    ```

*   **`urgent`**: Show snacks that are expiring soonest.
    ```bash
    python3 src/snack_sorter.py urgent
    ```

### Example Workflow

```bash
# Add some vital provisions
python3 src/snack_sorter.py add --name "Apocalypse Almonds" --quantity 2 --expiry "2025-01-15"
python3 src/snack_sorter.py add --name "Doomsday Donuts (freeze-dried)" --quantity 1 --expiry "2024-11-01"
python3 src/snack_sorter.py add --name "Prepper Pretzels" --quantity 4 --expiry "2025-03-20"

# See what's in the stash
python3 src/snack_sorter.py list

# Oh no, what's expiring soonest?
python3 src/snack_sorter.py urgent
```

### Development & Testing

To run the tests:

```bash
python3 -m unittest tests/test_snack_sorter.py
```
