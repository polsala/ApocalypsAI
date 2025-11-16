# ROT13 Encoder

A tiny utility that applies the ROT13 cipher to input text. It can be used directly from the command line or piped data via **stdin**.

## Installation

The utility is self‑contained – just copy the folder into your repository and run the script with Python 3.11.

```bash
cd utils/nightly-rot13-encoder/utils/rot13-encoder
python -m src.rot13 "Hello World"
# => Uryyb Jbeyq
```

Or pipe data:

```bash
echo "Secret Message" | python -m src.rot13
# => Frperg Zrffntr
```

## How it works

ROT13 rotates each alphabetic character by 13 places while leaving numbers, punctuation and whitespace untouched. Applying ROT13 twice restores the original text.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
