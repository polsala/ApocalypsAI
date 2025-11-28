# Nightly Apocalypse Snack Scheduler

## 📦 Overview

The Nightly Apocalypse Snack Scheduler is a whimsical yet crucial utility designed to help you manage your vital "apocalypse snack" reserves. In the face of impending doom (or just a busy week), it's easy to forget about those canned goods and MREs tucked away. This tool ensures your survival rations are rotated before they expire, preventing waste and keeping your pantry apocalypse-ready.

It reads a simple YAML configuration file detailing your snacks, their quantities, and their expiry dates, then provides a clear report on what needs attention soon.

## ✨ Features

*   **Expiry Tracking**: Monitors expiry dates for all listed snacks.
*   **Proactive Reminders**: Highlights snacks expiring within a configurable warning period.
*   **Simple Configuration**: Easy-to-edit YAML file for managing your inventory.
*   **Self-Contained**: Runs as a standalone Python script with minimal dependencies.

## 🚀 Usage

1.  **Create your `snacks.yaml` file**:
    Copy `snacks.example.yaml` to `snacks.yaml` and populate it with your actual snack inventory.
    Each entry should have `name`, `quantity`, and `expiry_date` (in `YYYY-MM-DD` format).

    Example `snacks.yaml`:
    ```yaml
    - name: Canned Beans
      quantity: 12
      expiry_date: 2024-12-31
    - name: MRE - Chicken Stew
      quantity: 5
      expiry_date: 2025-06-15
    - name: Emergency Water Rations
      quantity: 20
      expiry_date: 2023-10-01 # Oh no, this one's expired!
    ```

2.  **Run the scheduler**:
    ```bash
    python src/scheduler.py --config snacks.yaml --warning-days 60
    ```

    *   `--config`: Path to your `snacks.yaml` file (defaults to `snacks.yaml` in the current directory).
    *   `--warning-days`: Number of days before expiry to issue a warning (defaults to 90).

## 🛠️ Development

### Dependencies

This utility requires `PyYAML`. Install it using pip:
```bash
pip install PyYAML
```

### Running Tests

Tests are located in the `tests/` directory. They are designed to be deterministic and offline.
```bash
python -m unittest discover tests
```

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
