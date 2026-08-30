# nightly-survival-recipe-gen

A whimsical-yet-useful standalone utility for the community, designed to help survivors craft delicious (or at least edible) meals from the most unlikely post-apocalyptic ingredients. This CLI tool takes your available scavenged items and suggests recipes from its curated list, ensuring you never go hungry... or at least, not without a creative attempt!

Built with TypeScript for robust type-safety, ensuring your "Mutant Mushrooms" are always handled correctly.

## Features

*   **Type-Safe Ingredients & Recipes**: Strongly typed definitions for all ingredients and recipes prevent culinary mishaps.
*   **Whimsical Recipe Suggestions**: Discover unique dishes like "Glowing Mushroom Stew" or "Wasteland Worm & Potato Hash".
*   **CLI Interface**: Quickly find recipes by listing your available ingredients.
*   **Extensible**: Easily add new ingredients and recipes to expand your post-apocalyptic cookbook.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-survival-recipe-gen
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Build the project**:
    ```bash
    npm run build
    ```

## Usage

Run the utility from the command line, providing your available ingredients as arguments:

```bash
# To see available ingredients and usage
npm run cli

# Example: Find recipes with Mutant Mushroom and Dusty Water
npm run cli "Mutant Mushroom" "Dusty Water" "Scavenged Spice Mix" "Canned Mystery Meat"

# Example: Find recipes with Glow-in-the-dark Berries
npm run cli "Glow-in-the-dark Berry" "Ration Bar Crumbs"
```

The tool will output any recipes you can make with the provided ingredients, along with their descriptions and instructions. Ingredient matching is case-insensitive.

## Development & Testing

To run the tests:

```bash
npm test
```

To run the CLI directly with `ts-node` during development:

```bash
npm run cli "Irradiated Potato" "Wasteland Worms" "Salt Lick"
```

## Contributing

Feel free to add more whimsical ingredients, creative recipes, or improve the recipe matching logic! Ensure new additions are type-safe and include corresponding tests.
