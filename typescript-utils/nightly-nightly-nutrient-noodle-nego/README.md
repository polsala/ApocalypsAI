# Nightly Nutrient Noodle Negotiator

## 🍜 Your Daily Dose of Post-Apocalyptic Palate Planning!

In the desolate future, variety is not just the spice of life – it's a strategic imperative for mental well-being. The `nightly-nutrient-noodle-negotiator` is a whimsical-yet-essential CLI utility designed to bring a semblance of order (and surprise!) to your daily nutrient paste consumption. No more agonizing over which bland, grey tube to open next!

This tool helps you:
- **Rotate Flavors**: Ensures you cycle through your available nutrient paste flavors, preventing "flavor fatigue" (and potential scurvy from lack of diverse synthetic nutrients).
- **Mood-Based Suggestions**: Feeling 'sweet'? Craving something 'savory'? The negotiator can try to find a paste that matches your current emotional state, avoiding recently consumed options.
- **Simple Persistence**: Remembers your last consumed paste to maintain the rotation across sessions.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v18 or higher) and npm installed.
2.  **Clone the repository**: If you're viewing this as part of the ApocalypsAI repository, you're already there! Otherwise, navigate to the `typescript-utils/nightly-nutrient-noodle-negotiator` directory.
    ```bash
    # Example if cloning the whole repo
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-nutrient-noodle-negotiator
    ```
3.  **Install dependencies and build**: 
    ```bash
    npm install
    npm run build
    ```
4.  **Link the CLI tool (optional, for global access)**:
    ```bash
    npm link
    ```
    Now you can run `noodle-negotiator` from anywhere. Otherwise, run using `npm start` from the utility's directory.

## Usage

### Basic Suggestion

To get your next nutrient paste suggestion based on the rotational schedule:

```bash
# If linked globally:
noodle-negotiator

# Or, if running from the utility's directory:
npm start
```

Example Output:
```
🍜 Your next nutrient paste suggestion: Algae & Soy Blend
Tags: umami, earthy, nutritious
```

### Mood-Influenced Suggestion

Feeling a certain way? Tell the negotiator your mood, and it will try to find a matching paste that hasn't been consumed recently.

```bash
# Request a 'sweet' paste:
noodle-negotiator --mood sweet

# Or:
npm start -- --mood savory
```

Example Output:
```
🍜 Your next nutrient paste suggestion: Synthetic Berry Burst
(Influenced by your 'sweet' mood)
Tags: sweet, fruity, energizing
```

Available mood tags (from `src/data.ts`):
`umami`, `earthy`, `nutritious`, `sweet`, `fruity`, `energizing`, `savory`, `dense`, `sustaining`, `bland`, `essential`, `desperate`, `fresh`, `light`.

### How it Works

The utility maintains a `.nutrient_noodle_record.json` file in the directory where it's executed. This file stores the `lastConsumedId` and a `history` of recently consumed pastes to inform future suggestions.

## Development

To run tests:

```bash
npm test
```

## Contributing

Feel free to suggest new nutrient paste flavors, mood tags, or negotiation strategies!
