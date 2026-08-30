# nightly-survival-packer

A tiny Docker‑wrapped utility that helps you decide which supplies to pack for a post‑apocalypse trek.

## What it does

* Accepts a JSON file describing available items (name, weight, value) and a maximum carry weight.
* Uses a **greedy** algorithm (highest value‑to‑weight ratio first) to pick items that fit within the weight limit.
* Prints the selected items and the total weight/value.

The algorithm is intentionally simple – it runs fast in a tiny Alpine container and is good enough for quick planning.

## Build the image

```bash
docker build -t nightly-survival-packer .
```

## Run the tool

Create an `input.json` (see the example below) and run:

```bash
docker run --rm -v $(pwd)/input.json:/data/input.json nightly-survival-packer /data/input.json
```

### Example `input.json`

```json
{
  "max_weight": 10,
  "items": [
    {"name": "Water Bottle", "weight": 3, "value": 8},
    {"name": "Canned Food", "weight": 2, "value": 5},
    {"name": "First‑Aid Kit", "weight": 5, "value": 9},
    {"name": "Flashlight", "weight": 1, "value": 3},
    {"name": "Map", "weight": 1, "value": 2}
  ]
}
```

**Sample output**

```
Selected items:
- Water Bottle (weight: 3, value: 8)
- Canned Food (weight: 2, value: 5)
- Flashlight (weight: 1, value: 3)
- Map (weight: 1, value: 2)
Total weight: 7
Total value: 18
```

## Testing

A deterministic test suite lives in `tests/test_pack.sh`. It builds the image, runs the container with a known input, and asserts the exact output.

Run the tests with:

```bash
bash tests/test_pack.sh
```

## License

MIT © ApocalypsAI
