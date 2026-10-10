# nightly-temporal-task-aligner

A whimsical CLI tool that helps prioritize tasks by assigning "temporal alignment" scores, aiding in decision-making. Ever felt stuck between tasks, wondering which one the cosmos truly favors? This utility consults the "Temporal Alignment Matrix" to give you a playfully prioritized list, blending practical considerations with a dash of cosmic randomness.

## Features

*   **Whimsical Prioritization:** Combines task urgency, energy cost, and a "cosmic alignment" factor to generate a unique score.
*   **Decision Aid:** Helps break analysis paralysis by suggesting a clear, albeit whimsically influenced, task order.
*   **Type-Safe:** Built with TypeScript for robust and predictable behavior.
*   **CLI Interface:** Easily run from your terminal with a JSON input file.

## Installation

1.  **Node.js and npm/yarn:** Ensure you have Node.js (v18+) and npm (or yarn) installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-temporal-task-aligner
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build the project (optional, for production use):**
    ```bash
    npm run build
    ```

## Usage

The `nightly-temporal-task-aligner` expects a JSON file containing an array of tasks as input. Each task should have an `id` (string), `name` (string), `urgency` (number from 1-5), and `energyCost` (number from 1-5).

### Task Structure

```json
[
  {
    "id": "task1",
    "name": "Defuse temporal anomaly",
    "urgency": 5,
    "energyCost": 4
  },
  {
    "id": "task2",
    "name": "Gather cosmic dust for flux capacitor",
    "urgency": 2,
    "energyCost": 1
  },
  {
    "id": "task3",
    "name": "Re-calibrate chronometer",
    "urgency": 4,
    "energyCost": 2
  },
  {
    "id": "task4",
    "name": "Contemplate the void",
    "urgency": 1,
    "energyCost": 1
  }
]
```

### Running the Aligner

1.  **Create a `tasks.json` file** (e.g., in the root of the utility folder) with your tasks.
2.  **Run the utility:**
    ```bash
    npm start tasks.json
    # or using ts-node directly:
    # ts-node src/index.ts tasks.json
    ```

### Example Output

```
--- Original Tasks ---
- Defuse temporal anomaly (Urgency: 5, Energy: 4)
- Gather cosmic dust for flux capacitor (Urgency: 2, Energy: 1)
- Re-calibrate chronometer (Urgency: 4, Energy: 2)
- Contemplate the void (Urgency: 1, Energy: 1)

Consulting the Temporal Alignment Matrix...

--- Aligned Tasks (Recommended Order) ---
1. Gather cosmic dust for flux capacitor (Urgency: 2, Energy: 1, Temporal Alignment: 31.02)
2. Re-calibrate chronometer (Urgency: 4, Energy: 2, Temporal Alignment: 29.56)
3. Defuse temporal anomaly (Urgency: 5, Energy: 4, Temporal Alignment: 26.34)
4. Contemplate the void (Urgency: 1, Energy: 1, Temporal Alignment: 19.87)
```
*(Note: Temporal Alignment scores will vary slightly due to the cosmic randomness factor.)*

## Development

### Running Tests

```bash
npm test
# or yarn test
```

### Linting

```bash
npm run lint
# or yarn lint
```

## Contributing

Feel free to open issues or submit pull requests to enhance the cosmic alignment!

## License

This project is licensed under the MIT License.
