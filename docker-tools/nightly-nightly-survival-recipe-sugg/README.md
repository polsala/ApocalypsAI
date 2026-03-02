# Nightly Survival Recipe Suggester

A tiny Dockerized utility that reads a JSON file describing the items you have in your pantry and suggests simple recipes you can make with those ingredients. Perfect for post‑apocalypse cooking or when you’re low on groceries.

## Usage

```sh
# Create a pantry.json file (list of ingredient strings)
cat > pantry.json <<EOF
["bread", "peanut butter", "apple", "carrot", "water"]
EOF

# Build the image
docker build -t nightly-survival-recipe-suggester .

# Run the container, mounting the pantry file
docker run --rm -v "$(pwd)/pantry.json":/app/pantry.json nightly-survival-recipe-suggester
```

The container will output a list of recipes you can prepare with the supplied ingredients.

## How it works

The tool contains a tiny built‑in recipe database. It loads `pantry.json`, compares the available ingredients with each recipe’s required ingredients, and prints any recipes whose requirements are fully satisfied.

## Extending

Add more recipes by editing `src/recipes.py`.
