# Nightly Desk Plant Pal

A whimsical CLI utility to remind you to water your digital (or real) desk plant, tracking its well-being. Give your plant a name, set its watering frequency, and watch it thrive (or wilt!).

## Features

*   **Initialize a new plant**: Give it a name and set how often it needs water.
*   **Check plant status**: See when it was last watered, how many days it's been, and its current "mood."
*   **Water your plant**: Update its last watered date, making it happy again.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-desk-plant-pal
    ```
2.  **Install dependencies**:
    This utility has one development dependency (`jest`) for testing. For running, it has no external dependencies beyond Node.js itself.
    ```bash
    npm install
    ```

## Usage

Run the utility using `node src/index.js` followed by a command, or use `npm start <command>`.

### 1. Initialize your plant

If you don't have a plant yet, create one!

```bash
node src/index.js init <plant_name> [watering_frequency_days]
# or
npm start init <plant_name> [watering_frequency_days]
```

*   `<plant_name>`: (Optional) The name for your plant. Defaults to "Leafy".
*   `[watering_frequency_days]`: (Optional) How often (in days) your plant needs water. Defaults to 3 days.

**Example:**
```bash
node src/index.js init "Fernie" 4
# Output:
# 🌿 Welcome Fernie, your new desk plant pal!
# Remember to water it every 4 days.
```

### 2. Check your plant's status

See how your plant is doing.

```bash
node src/index.js check
# or
npm start check
```

**Example (Happy Plant):**
```bash
node src/index.js check
# Output:
# --- Fernie's Status ---
# Last watered: 2023-10-26 (1 days ago)
# Watering frequency: Every 4 days
# Current mood: Happy
# Message: Your plant is thriving! Keep up the good work.
# 
# ✨ Fernie is doing great!
```

**Example (Thirsty Plant):**
```bash
# (Imagine it's now 2023-10-31, 5 days since last watered)
node src/index.js check
# Output:
# --- Fernie's Status ---
# Last watered: 2023-10-26 (5 days ago)
# Watering frequency: Every 4 days
# Current mood: Thirsty
# Message: Your plant looks a bit parched. Maybe a drink soon?
# 
# 💧 It's time to water Fernie!
```

### 3. Water your plant

Give your plant a drink! This updates its "last watered" date.

```bash
node src/index.js water
# or
npm start water
```

**Example:**
```bash
node src/index.js water
# Output:
# 💦 You watered Fernie! It looks much happier now.
# 
# --- Fernie's Status ---
# Last watered: 2023-10-31 (0 days ago)
# Watering frequency: Every 4 days
# Current mood: Happy
# Message: Your plant is thriving! Keep up the good work.
# 
# ✨ Fernie is doing great!
```

## Development

### Running Tests

To run the tests, ensure you have `jest` installed (it's a dev dependency, so `npm install` should cover it).

```bash
npm test
# or
jest tests/index.test.js
```
