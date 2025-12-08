# nightly-bash-disk-emoji

Displays disk usage for each mounted filesystem as an emoji bar graph.

## Usage

```sh
./src/main.sh
```

The script reads `df -h` and prints lines like:

```
/ 50% 🟥🟥🟥🟥🟥⬜⬜⬜⬜⬜
/data 80% 🟥🟥🟥🟥🟥🟥🟥🟥⬜⬜
```

## How it works

- Uses `df -P -h` for predictable parsing.
- Converts the usage percentage into a 10‑character bar.
- Filled portion uses red square emoji (🟥), empty portion uses white square (⬜).

## Testing

Run the test suite:

```sh
bash tests/test_main.sh
```
