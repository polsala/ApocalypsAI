# Nightly Scavenged Stash Sorter

A whimsical-yet-useful type-safe CLI tool to help you organize your latest haul of scavenged items from the wasteland. Categorize and prioritize your findings based on peculiar survival criteria, ensuring no shiny bauble or crunchy sustenance goes unnoticed!

## Features

*   **Type-Safe Categorization**: Assigns items to predefined whimsical categories like "Crunchy Sustenance", "Shiny Baubles", "Mysterious Gadgets", and "Essential Oddities".
*   **Whimsical Prioritization**: Ranks items within categories based on their perceived "survival utility" (e.g., crunchiness, sparkle factor, potential for bartering with squirrels).
*   **CLI Interface**: Easily sort items directly from your terminal.
*   **Extensible Rules**: The categorization and prioritization logic can be easily modified or extended to suit your unique post-apocalyptic needs.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-scavenged-stash-sorter
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the utility with a list of items:

```bash
npm start -- "rusty wrench" "glowing mushroom" "half-eaten granola bar" "shiny bottle cap" "tattered blanket" "unlabeled vial" "duct tape" "ancient scroll"
```

Or, if you prefer to run directly with `ts-node`:

```bash
npx ts-node src/index.ts "rusty wrench" "glowing mushroom" "half-eaten granola bar" "shiny bottle cap" "tattered blanket" "unlabeled vial" "duct tape" "ancient scroll"
```

**Example Output**:

```
--- Scavenged Stash Report ---

Category: Crunchy Sustenance (Priority: High)
  1. half-eaten granola bar (Crunchiness: 8, Whimsy: 5)

Category: Essential Oddities (Priority: Medium)
  1. duct tape (Utility: 9, Whimsy: 3)
  2. rusty wrench (Utility: 7, Whimsy: 2)

Category: Shiny Baubles (Priority: Low)
  1. shiny bottle cap (Sparkle: 7, Whimsy: 8)

Category: Mysterious Gadgets (Priority: Very High)
  1. glowing mushroom (Danger: 9, Whimsy: 10)
  2. unlabeled vial (Danger: 8, Whimsy: 9)
  3. ancient scroll (Mystery: 7, Whimsy: 7)

Category: Textiles (Priority: Low)
  1. tattered blanket (Warmth: 6, Whimsy: 4)

--- End Report ---
```

## Development

### Running Tests

```bash
npm test
```

### Building for Production (Optional)

```bash
npm run build
```

This will compile the TypeScript code to JavaScript in the `dist/` directory. You can then run the compiled version:

```bash
node dist/index.js "item1" "item2"
```
