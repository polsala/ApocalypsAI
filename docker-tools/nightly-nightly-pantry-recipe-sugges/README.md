# Pantry Recipe Suggester

A whimsical Dockerized Bash utility that reads a CSV list of pantry items and suggests simple recipes you can make with what you have. Perfect for post‑apocalyptic kitchens.

## Build

```sh
docker build -t pantry-suggester .
```

## Run

Provide a CSV file (item,quantity) via stdin or a file path:

```sh
cat pantry.csv | docker run -i --rm pantry-suggester
# or
docker run -i --rm pantry-suggester < pantry.csv
```

The utility will output one or more recipe suggestions.

## Example

`pantry.csv`:

```
rice,1
beans,2
tomato,3
```

Running the tool prints:

```
Suggested recipes:
- Rice and Beans Bowl
- Tomato Rice Soup
```

## Testing

```sh
./tests/test_suggest.sh
```
