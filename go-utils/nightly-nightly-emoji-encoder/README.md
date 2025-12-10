# nightly-emoji-encoder

A whimsical Go CLI that turns your text into a string of emojis. Each alphabetic character is replaced by its corresponding regional indicator symbol, digits by number emojis, and punctuation is left unchanged. Useful for adding a playful touch to logs or messages.

## Usage

```bash
# Encode a string
echo "Hi!" | nightly-emoji-encoder

# Or pass as argument
nightly-emoji-encoder "Good morning!"
```

## Example

```
$ echo "Hi!" | nightly-emoji-encoder
🇭🇮!
```

## License

MIT
