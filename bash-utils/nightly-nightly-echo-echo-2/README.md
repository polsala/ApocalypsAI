# nightly-echo-echo

A tiny Bash script that prints a random motivational phrase prefixed with an ISO‑8601 UTC timestamp.  It can be overridden with the `ECHO_ECHO_PHRASE` environment variable for deterministic output.

## Usage

```bash
# Run the script directly
bash src/main.sh
```

### Override the phrase

```bash
ECHO_ECHO_PHRASE="You are awesome!" bash src/main.sh
```

## Output format

```
[2025-12-27T14:30:00Z] Keep calm and carry on.
```

The timestamp is always in UTC and follows the `YYYY-MM-DDTHH:MM:SSZ` format.

## Tests

The accompanying test suite (`tests/test_main.py`) verifies:

* The script outputs a timestamp in the correct format.
* The phrase is either one of the predefined list or the value of `ECHO_ECHO_PHRASE`.
* Overriding the phrase works as expected.

## License

MIT License.
