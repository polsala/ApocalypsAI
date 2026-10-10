# Nightly Temporal Snack Stash

A type-safe CLI tool for the discerning temporal traveler or apocalypse survivor to manage their vital snack reserves. Track expiration dates, prevent temporal spoilage, and get smart suggestions on which delicious morsel to consume next to optimize your survival pantry.

## Features

*   **Add Snacks**: Register new snacks with their name, quantity, and expiration date.
*   **List Stash**: View all your snacks, sorted by how soon they'll expire.
*   **Eat Snacks**: Mark snacks as consumed, partially or fully.
*   **Suggest Consumption**: Get recommendations for which snacks are most urgent to eat.
*   **Type-Safe**: Built with TypeScript for robust data handling.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm/yarn installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-temporal-snack-stash
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build the project**:
    ```bash
    npm run build
    ```

## Usage

Run the utility using `npm start <command> [arguments]`.

### Add a snack

```bash
npm start add <name> <quantity> <expiration-date>
# Example: npm start add "Cosmic Crisps" 5 "2024-12-31"
# Expiration date format: YYYY-MM-DD
```

### List all snacks

```bash
npm start list
```

### Eat a snack

You'll need the snack's ID, which is shown when you `list` them.

```bash
npm start eat <snack-id> <quantity-to-eat>
# Example: npm start eat 123e4567-e89b-12d3-a456-426614174000 2
```

### Get consumption suggestions

This will list snacks ordered by their expiration date, suggesting the most urgent ones first.

```bash
npm start suggest
```

## Development

### Running Tests

```bash
npm test
```

### Building

```bash
npm run build
```
