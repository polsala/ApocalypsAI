# nightly-void-whispers-affirmations

A TypeScript utility that generates personalized post-apocalyptic affirmations with a haunting void whisper style.

## Features

- Generates unique affirmations with a post-apocalyptic theme
- Personalized messages based on user input
- CLI interface with customizable options
- Whimsical void whisper delivery style

## Installation

```bash
npm install -g nightly-void-whispers-affirmations
```

## Usage

```bash
# Generate a random affirmation
void-whispers

# Generate a personalized affirmation
void-whispers --name "Survivor"

# Generate an affirmation with custom mood
void-whispers --mood "hopeful"

# Generate multiple affirmations
void-whispers --count 5
```

## Options

- `--name` - Personalize the affirmation with a name
- `--mood` - Set the mood (hopeful, determined, cautious, fierce)
- `--count` - Number of affirmations to generate (1-10)
- `--help` - Show help information

## Examples

```bash
$ void-whispers --name "Rebel"
"In the silence of the wasteland, Rebel, your spirit burns brighter than any ember. The void whispers your name with reverence."

$ void-whispers --mood "determined" --count 2
"The path ahead is treacherous, but your determination cuts through darkness like a blade through shadow."
"Each step you take reshapes the wasteland. Your will is the hammer that forges tomorrow."
```

## License

MIT
