# Nightly Rad-Resistant Recipe Recommender

## 🍲 Survive & Thrive with Limited Ingredients! ☢️

This utility is your trusty companion in the desolate wastes, helping you whip up surprisingly palatable (and radiation-resistant!) meals from whatever scraps you've managed to scavenge. No fancy ingredients, no complex steps – just pure, unadulterated survival cuisine.

### Features

*   **Ingredient-Based Recommendations**: Tell it what you have, and it tells you what you can make.
*   **Prioritized Suggestions**: Recipes using more of your available ingredients rise to the top.
*   **Simple & Self-Contained**: No internet required, just your wits and a few cans of mystery meat.
*   **Whimsical Survival Lore**: Each recipe comes with a touch of post-apocalyptic charm.

### How to Use

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-rad-resistant-recipe-recommender
    ```

2.  **Run the recommender with your available ingredients**:
    Provide a space-separated list of ingredients you have on hand. The more specific, the better!

    ```bash
    python src/recommender.py --ingredients "canned beans" "stale bread" "water" "salt"
    ```

    Example output:
    ```
    --- Rad-Resistant Recipe Recommendations ---

    1. **Bunker Bean Stew (Matches 3/4 ingredients)**
       Ingredients: canned beans, water, salt, scavenged greens
       Instructions:
       * Combine canned beans, water, and a pinch of salt in a pot.
       * Heat over a low flame until simmering.
       * If you're lucky enough to find any scavenged greens, chop them and add for extra nutrients.
       * Serve hot with stale bread for dipping.
       *Survival Tip: A true survivor knows how to make a feast from a few beans and a prayer.*

    2. **Stale Bread & Water Gruel (Matches 2/2 ingredients)**
       Ingredients: stale bread, water
       Instructions:
       * Break stale bread into small pieces.
       * Soak in water until soft.
       * Consume slowly.
       *Survival Tip: Hydration is key, even if your meal is mostly liquid bread.*

    No other recipes found matching your ingredients.
    ```

### Development & Testing

To run the tests:

```bash
python -m unittest tests/test_recommender.py
```
