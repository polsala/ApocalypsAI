# Apocalypse Pet Name Generator

A whimsical utility to generate unique, post-apocalyptic themed names for your loyal wasteland companions. Whether you've found a trusty dog, a resilient cat, or even a mutated squirrel, this generator will help you find a name that fits the grim-yet-hopeful future.

## Usage

To generate a single pet name:

```bash
python src/generator.py
```

To generate multiple pet names:

```bash
python src/generator.py --count 5
```

## Examples of Generated Names

*   Cinder-Paw
*   Rusty Bolt
*   Shadow Hound
*   Grit-Eye
*   Rubble-Runner
*   Whisper-Fang
*   Blaze Scout
*   Scrap Warden

## Development

The generator uses a simple set of word lists (adjectives, nouns, suffixes) to combine into unique names. Contributions for more thematic words are welcome!

### Running Tests

```bash
python -m unittest tests/test_generator.py
```
