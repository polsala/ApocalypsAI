# Nightly Pantry Recipe Suggester

A whimsical yet practical Docker‑based utility that reads a CSV file containing the items you have in your pantry and suggests recipes you can make with those ingredients.

## How it works
1. **Inventory CSV** – Provide a file `inventory.csv` where each line is a single ingredient name (case‑insensitive). Example:
   ```
   beans
   water
   salt
   rice
   oil
   ```
2. **Docker image** – The container runs a tiny Python script that loads the CSV, compares it against a built‑in list of simple recipes, and prints any matches.
3. **Output** – If matching recipes are found, they are listed; otherwise you get a friendly "No recipes match your pantry items." message.

## Build the image
```bash
docker build -t pantry-suggester .
```

## Run the container
Mount your inventory CSV into `/data/inventory.csv` inside the container:
```bash
docker run --rm -v $(pwd)/inventory.csv:/data/inventory.csv pantry-suggester
```

## Sample inventory
Create a file `inventory.csv` with the following content to see some suggestions:
```
beans
water
salt
rice
oil
bread
peanut butter
```
Running the container with this file will output:
```
You can make:
- Bean Soup
- Rice Pilaf
- Peanut Butter Toast
```

## Extending recipes
The recipe list lives in `src/app.py` as the `RECIPES` constant. Feel free to edit it and add your own favorite dishes.

## Testing
The utility includes a pytest suite. To run the tests locally (outside Docker):
```bash
pip install pytest
pytest tests
```

---
*Built by the ApocalypsAI Nightly Integrator agent.*
