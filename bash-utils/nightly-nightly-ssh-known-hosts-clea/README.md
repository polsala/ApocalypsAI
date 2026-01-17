# nightly-ssh-known-hosts-cleaner

Utility to deduplicate and sort your SSH `known_hosts` file, removing duplicate host entries while preserving comments. Useful for keeping SSH fingerprints tidy.

## Usage

```sh
./clean_known_hosts.sh [path_to_known_hosts]
```

If no path is provided, the script defaults to `~/.ssh/known_hosts`.

## How it works

- Reads the file.
- Preserves comment lines (starting with `#`).
- Sorts and removes duplicate host lines.
- Creates a backup of the original file at `<file>.bak` before modifying.
- Writes the cleaned content back to the original file.

## Safety

The script never deletes data without first creating a backup. If something goes wrong, you can restore the original file from the `.bak` copy.

## Tests

Run the test suite with:

```sh
bash tests/test_clean_known_hosts.sh
```

The test creates a temporary `known_hosts` file with duplicate entries, runs the script, and verifies that the output matches the expected cleaned version.
