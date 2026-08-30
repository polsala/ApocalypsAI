# Nightly Wasteland Lore Scribe

A whimsical-yet-useful utility for generating short, evocative snippets of post-apocalyptic lore. Perfect for game masters, writers, or anyone needing a quick dose of atmospheric inspiration for their desolate worlds.

## Installation

1. Navigate to the `nightly-wasteland-lore-scribe` directory.
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

To generate a single lore snippet with a random theme:

```bash
npm start
```

To generate lore snippets with a specific theme (e.g., 'ruins'):

```bash
npm start -- --theme ruins
```

To generate multiple lore snippets (e.g., 3 snippets):

```bash
npm start -- --count 3
```

Combine options:

```bash
npm start -- --theme hope --count 2
```

### Available Themes

- `ruins`
- `mutants`
- `hope`
- `despair`
- `technology`
- `nature`

If no theme is specified, one will be chosen randomly.

## Development

### Running Tests

```bash
npm test
```

## Example Output

```
In the skeletal remains of forgotten cities, where rust weeps silent tears, the echoes of a lost world whisper tales of grandeur and decay.
```

```
Amongst the twisted flora and fauna, where life finds grotesque new forms, the irradiated earth births wonders and horrors alike.
```
