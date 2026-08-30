# Nightly Scavenger Report

A whimsical Dockerized utility that reads a JSON list of scavenged items and produces a colorful survival report with emojis.

## Usage

```sh
docker build -t scavenger .
 docker run --rm -v $(pwd)/items.json:/app/items.json scavenger
```

The `items.json` file should contain an array of objects:

```json
[
  {"name": "canned beans", "quantity": 3},
  {"name": "bottled water", "quantity": 2}
]
```

The container will output a formatted report.

## Example

```
🗃️ Scavenger Report
--------------------
🥫 canned beans x3
💧 bottled water x2
```
