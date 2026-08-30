# Nightly Pantry Recipe Suggester

Utility that, given a JSON file listing the ingredients you have in your pantry, suggests a random recipe that can be made with those ingredients. Packaged as a Docker container for easy use on any system.

## Usage

```sh
# Build the Docker image
docker build -t pantry-suggester .

# Create a pantry.json file, for example:
cat > pantry.json <<EOF
["egg", "flour", "milk", "sugar", "butter"]
EOF

# Run the container, mounting the pantry file
docker run --rm -v "$(pwd)/pantry.json":/app/pantry.json pantry-suggester
```

The container will output a recipe name and its required ingredients, or a message if no matching recipe is found.
