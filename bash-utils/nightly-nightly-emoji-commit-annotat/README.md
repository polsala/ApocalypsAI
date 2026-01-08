# nightly-emoji-commit-annotator

Adds a rotating set of emojis to each line of a git commit message, making logs more expressive.

## Usage

```sh
cat commit.txt | ./src/annotate.sh > annotated.txt
```

Or directly:

```sh
./src/annotate.sh < commit.txt
```

You can also pass a file:

```sh
./src/annotate.sh commit.txt
```

## How it works

The script reads the input, prefixes each line with an emoji from a predefined list (🚀✨🔥💡🎉) cycling through them.

## License

MIT
