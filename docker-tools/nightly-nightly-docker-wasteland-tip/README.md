# Wasteland Tips Docker Container

A tiny Docker image that prints a post‑apocalypse survival tip. The tip is selected deterministically based on the `SEED` environment variable, making it easy to test and predict.

## Build

```sh
docker build -t wasteland-tips .
```

## Run

```sh
docker run --rm -e SEED=3 wasteland-tips
```

If `SEED` is not set, it defaults to `0`.

## Adding Tips

Edit `src/tips.sh` and add more entries to the `TIPS` array.

## Testing

Run the provided test script:

```sh
sh tests/test_container.sh
```
