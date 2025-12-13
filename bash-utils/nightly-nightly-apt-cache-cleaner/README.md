# nightly-apt-cache-cleaner

Utility to clean APT package cache, freeing disk space. Supports dry‑run mode to preview actions and a mock mode for safe testing. Ideal for post‑apocalypse servers that need to stay lean.

## Usage

```sh
./clean_apt_cache.sh          # actually clean (requires sudo)
./clean_apt_cache.sh -n      # dry‑run, shows what would be done
```

## Options

- `-n` : dry‑run – show the apt-get clean command without executing it.
- `-h` : show this help message.

## Testing

Run the bundled test suite:

```sh
bash tests/test_clean_apt_cache.sh
```
