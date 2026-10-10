# nightly-cosmic-chore-chooser

A whimsical CLI tool that uses "cosmic alignment" (seeded randomness) to suggest a task from a list, aiding decision-making. Perfect for when the post-apocalyptic chaos makes choosing your next step feel overwhelming.

## Installation

1.  Ensure you have Node.js (v18+) and npm installed.
2.  Install globally:
    ```bash
npm install -g nightly-cosmic-chore-chooser
    ```

## Usage

Run the command with your list of potential tasks:

```bash
cosmic-chore-chooser "Scavenge for parts" "Repair the comms array" "Fortify the perimeter"
```

You can also provide a numeric seed for deterministic "cosmic alignment":

```bash
cosmic-chore-chooser "Read ancient texts" "Meditate on the void" --seed 42
```

### Example Output

```
✨ Cosmic Chore Suggestion ✨
-----------------------------
Task: Repair the comms array
Rationale: A faint shimmer in the astral plane points to this as your next endeavor.
Cosmic Alignment Score: 0.7341
-----------------------------
```

## Development

1.  Clone the repository.
2.  Navigate to the `nightly-cosmic-chore-chooser` directory.
3.  Install dependencies: `npm install`
4.  Build the project: `npm run build`
5.  Run tests: `npm test`
6.  Run in development mode: `npm run dev "Task 1" "Task 2"`
