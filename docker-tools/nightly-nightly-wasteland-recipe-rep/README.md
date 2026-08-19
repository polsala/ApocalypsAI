# Nightly Wasteland Recipe Replicator

## Summary
This utility helps survivors in the wasteland figure out what delicious (or at least edible) meals they can concoct with the scavenged ingredients they have on hand. It's a containerized solution, ensuring consistent operation across various post-apocalyptic computing environments.

## How it Works
The `Wasteland Recipe Replicator` takes a comma-separated list of available ingredients as input. It then cross-references these with a predefined 'Wasteland Cookbook' (a JSON file of recipes) and outputs a list of all recipes that can be fully prepared with the provided ingredients.

## Usage

### 1. Build the Docker Image
Navigate to the `nightly-wasteland-recipe-replicator` directory and build the Docker image:

```bash
docker build -t wasteland-recipe-replicator .
```

### 2. Run the Container
Execute the container, passing your available ingredients using the `--ingredients` flag. Ingredients should be comma-separated.

```bash
docker run wasteland-recipe-replicator --ingredients "mutant fungus,stale bread,purified water"
```

**Example Output:**

```json
[
  {
    "name": "Fungus & Bread Gruel",
    "ingredients": [
      "mutant fungus",
      "stale bread",
      "purified water"
    ],
    "instructions": "Combine fungus and bread in a pot with water. Boil until mushy. Serve lukewarm."
  }
]
```

### 3. Explore Recipes
Try different combinations of ingredients to discover new culinary delights (or necessities)!

```bash
docker run wasteland-recipe-replicator --ingredients "radroach meat,wild herbs"
```

## Development

### `src/app.py`
The core Python script that processes ingredients and matches them against recipes.

### `src/recipes.json`
The 'Wasteland Cookbook' containing all known recipes, their required ingredients, and instructions.

### `Dockerfile`
Defines the Docker image, installing Python and copying the application files.

## Tests
To run the integration tests, execute the `tests/run_tests.sh` script. This script builds the Docker image and then runs it with various ingredient inputs, asserting the expected JSON output.

```bash
bash tests/run_tests.sh
```
