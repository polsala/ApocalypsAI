# Nightly Nourishment Nudger

## 🍽️ Purpose

In the relentless pursuit of digital survival, even the most hardened ApocalypsAI agents need a moment to refuel and recharge. The **Nightly Nourishment Nudger** is a whimsical-yet-vital utility designed to gently remind you (or your fellow survivors) to take a break, hydrate, or grab a snack. Because a well-nourished mind is a resilient mind, even when the world is ending.

This utility is perfect for integrating into nightly cron jobs, CI/CD pipelines, or simply running manually when you feel the digital dust settling too heavily.

## ✨ Features

*   **Whimsical Nudges**: Generates fun, apocalypse-themed messages for hydration, snacking, or taking a break.
*   **Category Selection**: Choose specific types of nudges (`hydrate`, `snack`, `break`) or let it pick randomly.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.
*   **CLI Friendly**: Easy to run from your terminal or integrate into scripts.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Nudger

Navigate to the `src` directory within `nightly-nourishment-nudger` and run the `nudger.py` script:

```bash
cd utils/nightly-nourishment-nudger/src
python nudger.py --category hydrate
```

#### Examples:

1.  **Get a random nourishment nudge:**
    ```bash
    python nudger.py
    # Or explicitly:
    python nudger.py --category random
    ```
    _Example Output:_
    `[2023-10-27 10:30:00] Nudge: Your organic systems require liquid sustenance. Drink water!`

2.  **Get a hydration reminder:**
    ```bash
    python nudger.py --category hydrate
    ```
    _Example Output:_
    `[2023-10-27 10:31:05] Nudge: Hydration Protocol Initiated: Remember to refuel your internal reservoirs!`

3.  **Get a snack suggestion:**
    ```bash
    python nudger.py --category snack
    ```
    _Example Output:_
    `[2023-10-27 10:32:10] Nudge: Energy Reserves Low: Seek out a delicious, non-radioactive snack!`

4.  **Get a break recommendation:**
    ```bash
    python nudger.py --category break
    ```
    _Example Output:_
    `[2023-10-27 10:33:15] Nudge: System Overload Imminent: Initiate short break protocol!`

## 🧪 Testing

To run the tests, navigate to the `tests` directory and execute `pytest` (if installed) or `unittest`:

```bash
cd utils/nightly-nourishment-nudger/tests
python -m unittest test_nudger.py
```

All tests are self-contained and use mocks to ensure determinism and offline execution.

## 🤝 Contribution

Feel free to expand the message list, add new categories, or suggest improvements!
