# Nightly Temporal Debt Ledger

A whimsical CLI utility to track your 'temporal debts' – time you've borrowed from future tasks and committed to repaying later.

## ✨ Concept

Ever feel like you're borrowing time from your future self? This tool helps you formalize that! Declare a 'temporal debt' when you need extra hours for a task, specifying when you intend to repay it. Then, mark it as repaid when you've balanced your timeline. Keep your temporal balance in check!

## 🚀 Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Clone the repository (or download the utility folder)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-temporal-debt-ledger
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Make the CLI executable (optional, but recommended for easy access)**:
    ```bash
    npm link
    ```
    Now you can run `temporal-debt` from anywhere in your terminal.

## 💡 Usage

The utility stores your temporal debts in a JSON file located at `~/.temporal-ledger.json` (or `%USERPROFILE%/.temporal-ledger.json` on Windows).

### Commands:

*   `temporal-debt add <task> <hours> <repaymentDate>`: Add a new temporal debt.
    *   `<task>`: A description of the task you're borrowing time for (e.g., "Fix critical bug").
    *   `<hours>`: The number of hours you are borrowing.
    *   `<repaymentDate>`: The target date for repayment in `YYYY-MM-DD` format (e.g., `2024-08-01`).

*   `temporal-debt repay <id>`: Mark an existing temporal debt as repaid.
    *   `<id>`: The unique ID of the debt (obtained from `list` command).

*   `temporal-debt list`: List all recorded temporal debts, both outstanding and repaid.

*   `temporal-debt balance`: Show your current temporal balance (total borrowed vs. total repaid).

### Examples:

1.  **Borrow 3 hours for a "Deep dive into void whispers" due to be repaid by August 1st, 2024:**
    ```bash
    temporal-debt add "Deep dive into void whispers" 3 2024-08-01
    ```

2.  **List all your temporal debts:**
    ```bash
    temporal-debt list
    ```
    (This will output a list including the ID of the debt you just added, e.g., `debt-1`)

3.  **Repay the debt with ID `debt-1`:**
    ```bash
    temporal-debt repay debt-1
    ```

4.  **Check your temporal balance:**
    ```bash
    temporal-debt balance
    ```

## 🧪 Testing

To run the automated tests for this utility:

```bash
npm test
```

Tests are deterministic and offline, using mocks for file system operations to ensure reliability.
