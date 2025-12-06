# ASCII Clock

Render the current time as ASCII art digits in the terminal.

## Usage

```sh
python utils/ascii-clock/src/clock.py
```

Or, if you have the repository root on your `PYTHONPATH`:

```sh
python -m utils.ascii-clock.src.clock
```

The script prints the current local time in a stylized ASCII format.

## Example Output

```
    _    _   
  | _| .  _| |_| 
  | |_  .  _|  |
```

(The actual digits will reflect the current time when you run the command.)

## Testing

Run the test suite with:

```sh
python -m unittest discover utils/ascii-clock/tests
```

The tests are deterministic and use mocks, so they run offline without any network access.
