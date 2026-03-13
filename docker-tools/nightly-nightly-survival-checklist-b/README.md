# Nightly Survival Checklist Builder

Utility that reads a JSON file describing available supplies and generates a prioritized survival checklist based on importance and quantity. Packaged as a Docker container for easy use.

## Usage

```sh
docker build -t survival-checklist .

docker run --rm -v $(pwd)/supplies.json:/app/supplies.json survival-checklist
```

The container will output a checklist to stdout.

## Input format

```json
{
  "items": [
    {"name": "Water", "importance": 10, "quantity": 5},
    {"name": "Canned Beans", "importance": 6, "quantity": 12},
    {"name": "First Aid Kit", "importance": 9, "quantity": 1}
  ]
}
```

## Output

```
1. Water (Qty: 5) - Importance: 10
2. First Aid Kit (Qty: 1) - Importance: 9
3. Canned Beans (Qty: 12) - Importance: 6
```

## Testing

Run `pytest -q` inside the repository.
