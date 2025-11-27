# Nightly Gloom-Glimmer Generator

## 🌟 Find Your Glimmer in the Gloom 🌟

In the darkest of times, even a tiny spark of hope can light the way. The Nightly Gloom-Glimmer Generator is a whimsical-yet-useful command-line utility designed to help you find a positive reframe or a silver lining in any text, no matter how bleak it seems.

Whether it's a journal entry, a message from a fellow survivor, or just your own thoughts, feed it into the Glimmer Generator, and it will attempt to extract a "glimmer" – a hopeful perspective, a potential for growth, or a reminder of resilience.

## Usage

The `glimmer_generator.py` script can be run directly from your terminal.

### From a string argument:

```bash
python src/glimmer_generator.py "The old world is lost, and despair fills the air."
```

### From standard input (for longer texts):

```bash
echo "Our supplies are dwindling, and the generator is broken. We face a struggle." | python src/glimmer_generator.py
```

## Examples

```
$ python src/glimmer_generator.py "The city is in ruins, and all seems lost."
Original Text: "The city is in ruins, and all seems lost."
✨ Glimmer of Hope:
  - Gloom: "ruins" -> Glimmer: "A blank canvas for new beginnings, a chance to build something stronger."
  - Gloom: "lost" -> Glimmer: "An opportunity to discover new paths and redefine what truly matters."
```

```
$ echo "Today was tough, but we found some clean water." | python src/glimmer_generator.py
Original Text: "Today was tough, but we found some clean water."
✨ Glimmer of Hope:
  - Gloom: "tough" -> Glimmer: "Every challenge overcome makes us stronger and more resilient."
  - No specific gloom detected, but remember: "Even small victories are monumental steps forward."
```

## How it Works

The utility uses a predefined dictionary of "gloom" keywords and phrases, each mapped to a corresponding "glimmer" or positive reframe. It scans the input text, identifies these gloom elements, and presents their associated glimmers. If no specific gloom is found, it offers a general message of encouragement.

## Development

This utility is written in Python 3.x and is self-contained.

### Running Tests

To ensure the Glimmer Generator is always ready to shine, run its tests:

```bash
python -m unittest tests/test_glimmer_generator.py
```
