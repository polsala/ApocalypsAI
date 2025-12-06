# Error Fortune Teller

A whimsical utility that transforms mundane error messages into cryptic, encouraging, or humorous "fortune cookie" wisdom, offering a moment of levity during debugging. Because sometimes, all you need is a good laugh and a cryptic hint to find that elusive bug.

## Purpose

Debugging can be a frustrating journey. This tool aims to inject a bit of fun and philosophical reflection into the process by providing a random, debugging-themed "fortune" whenever you encounter an error or just need a moment of inspiration.

## How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/error-fortune-teller/
    ```

2.  **Run the fortune teller:**

    *   **For a general debugging fortune:**
        ```bash
        python src/fortune_teller.py
        ```

    *   **To get a fortune related to a specific error message (the message itself is currently ignored for fortune generation, but can be used for context):**
        ```bash
        python src/fortune_teller.py "TypeError: 'NoneType' object is not subscriptable"
        ```
        or
        ```bash
        python src/fortune_teller.py "Segmentation fault (core dumped)"
        ```

## Examples

```
$ python src/fortune_teller.py

For your current coding challenge:

✨ Your debugging fortune: The wisdom of the stack trace is profound, if only you learn to read its ancient script. ✨

May your code compile and your tests pass!
```

```
$ python src/fortune_teller.py "Error 404: Page Not Found"

For your error: 'Error 404: Page Not Found'

✨ Your debugging fortune: The greatest bugs are often found in the smallest details. Observe closely. ✨

May your code compile and your tests pass!
```

## Development

### Running Tests

To ensure everything is working as expected, run the tests from the utility's root directory:

```bash
python -m unittest tests/test_fortune_teller.py
```
