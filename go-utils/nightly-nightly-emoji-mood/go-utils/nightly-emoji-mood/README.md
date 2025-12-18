# nightly-emoji-mood

A whimsical CLI that prints an emoji mood based on the current day of the week, optionally with a motivational phrase.

## Usage

```bash
go run src/main.go
```

or build:

```bash
go build -o nightly-emoji-mood src/main.go
./nightly-emoji-mood
```

The output will be something like:

```
🌞 Good morning! Keep shining today!
```

You can also pass `--phrase` to include a random motivational phrase.

```
./nightly-emoji-mood --phrase
```

## How it works

The utility maps each weekday to a specific emoji and a base phrase. When run, it selects the emoji for the current day and optionally appends a random phrase from a predefined list.

## License

MIT
