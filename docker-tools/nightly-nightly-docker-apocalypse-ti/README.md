# nightly-docker-apocalypse-tip

A whimsical Docker container that prints a random apocalypse survival tip. Provide an optional numeric seed to get a deterministic tip (useful for testing).

## Usage

```sh
docker run --rm nightly-docker-apocalypse-tip [seed]
```

- If `seed` is omitted, a random tip is chosen.
- If `seed` is provided, the tip is selected deterministically: tip index = seed % number_of_tips.

## Example

```sh
docker run --rm nightly-docker-apocalypse-tip 42
# => Water is more valuable than gold.
```

## Building

```sh
docker build -t nightly-docker-apocalypse-tip .
```
