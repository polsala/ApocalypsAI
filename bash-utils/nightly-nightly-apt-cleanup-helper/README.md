# nightly-apt-cleanup-helper

Utility to help clean up the apt package cache on Debian/Ubuntu systems. In dry‑run mode it shows what would be removed; with `--execute` it actually runs `apt-get autoremove` and `apt-get clean`.

## Usage

```sh
./src/apt_cleanup.sh [--dry-run|--execute]
```

* `--dry-run` (default) – prints the packages that would be removed without making any changes.
* `--execute` – performs the actual cleanup.

The script respects the environment variable `MOCK_APT_GET_OUTPUT` for testing purposes; when set, its value is used as the simulated output of the apt commands.
