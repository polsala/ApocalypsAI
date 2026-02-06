# Nightly Scavenged Recipe Generator

A containerized utility to inspire culinary creativity in the wasteland. Input your scavenged ingredients, and get a unique, whimsical recipe idea!

## Purpose
In the post-apocalyptic world, resources are scarce, and meal planning can be a challenge. This tool helps survivors transform their random hauls into imaginative (and hopefully edible) dishes by generating whimsical recipe names, descriptions, and simple instructions based on a list of available ingredients.

## How it Works

The utility takes a comma-separated list of ingredients as input. It then uses a dash of AI-powered whimsy to combine these ingredients with pre-defined post-apocalyptic culinary terms to create a unique recipe.

## Usage

1.  **Build the Docker image:**

    ```bash
    docker build -t scavenged-recipe-gen .
    ```

2.  **Run the container with your ingredients:**

    Pass your scavenged ingredients as a comma-separated string to the container.

    ```bash
    docker run scavenged-recipe-gen "rusty can,mutant fungus,purified water,irradiated berries"
    ```

    **Example Output:**

    ```
    --- The Rusty Fungus Forage ---
    A hearty forage to reconstitute your spirits, featuring the rare mutant fungus.

    Instructions:
    1. Gather your rusty can, mutant fungus, purified water, irradiated berries.
    2. Reconstitute them over a flickering barrel fire.
    3. Serve with a side of existential dread.
    ```

3.  **Run without specific ingredients (for a mystery meal):**

    ```bash
    docker run scavenged-recipe-gen
    ```

    **Example Output:**

    ```
    --- The Forgotten Mystery Mash ---
    A hearty mash to scramble your spirits, featuring the rare mystery ingredient.

    Instructions:
    1. Gather your mystery ingredients.
    2. Scramble them with salvaged kitchenware.
    3. Serve with a side of existential dread.
    ```

## Development

The core logic is a simple Python script (`src/app.py`) that uses `random` to combine elements. The `Dockerfile` packages this script and its dependencies into a runnable container.
