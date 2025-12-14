# Nightly Relic Rarity Radar

## Summary

The Nightly Relic Rarity Radar is a whimsical-yet-useful React web application designed for survivors of the apocalypse to catalog and visualize their scavenged items. Simply input the name of a found item, and the radar will assign it a unique rarity level (Common Scavenge, Uncommon Find, Rare Relic, Legendary Artifact, or Mythic Echo) along with a descriptive icon and color. It helps bring a sense of order and wonder to the chaotic task of inventory management in the wasteland.

## Features

*   **Whimsical Rarity Assignment**: Deterministically assigns rarity based on the item's name.
*   **Interactive UI**: Easily add new items and see their rarity instantly.
*   **Visual Feedback**: Each rarity level has a distinct color and emoji icon.
*   **Item List**: Keeps a running list of all analyzed relics.

## How to Run

This utility is a React application. To run it locally, you'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-relic-rarity-radar
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    # or yarn start
    ```

    This will typically open the application in your browser at `http://localhost:3000`.

## How to Test

Tests are written using Jest and React Testing Library.

1.  **Ensure dependencies are installed** (as per 'How to Run' section).

2.  **Run the tests:**
    ```bash
    npm test
    # or yarn test
    ```

## Rarity Logic Explained

The `assignRarity` function (found in `src/utils/rarityLogic.js`) determines an item's rarity based on a scoring system:

*   **Item Name Length**: Longer names generally contribute to higher rarity.
*   **Keywords**: Specific keywords (e.g., "void", "temporal", "anomaly", "ancient", "glowing", "circuit", "shard") significantly boost the rarity score.
*   **Character Complexity**: Presence of numbers or special characters also adds to the score.

The total score then maps to one of the five rarity levels:

*   **Common Scavenge**: Basic, everyday finds.
*   **Uncommon Find**: Slightly more interesting or useful items.
*   **Rare Relic**: Items with unique properties or historical significance.
*   **Legendary Artifact**: Powerful or exceptionally rare discoveries.
*   **Mythic Echo**: Items tied to the deepest mysteries of the apocalypse, often temporal or void-related.
