# Nightly Scavenger Meal Planner

Utility that reads a list of available pantry items and suggests a whimsical recipe using only those items. Containerized for easy use.

## Usage

```sh
# Build the Docker image
docker build -t scavenger-meal-planner .

# Prepare an ingredients file (one ingredient per line)
cat > ingredients.txt <<EOF
rat
water
spice
EOF

# Run the container, mounting the ingredients file
docker run --rm -v $(pwd)/ingredients.txt:/app/ingredients.txt scavenger-meal-planner
```

The container expects an `ingredients.txt` file at the working directory `/app`. Each line should contain a single ingredient name.

## How it works

The app reads the file, looks for recipe templates whose required ingredients are a subset of the supplied list, picks one at random (with a fixed seed for reproducibility), and prints the recipe.

## License

MIT
