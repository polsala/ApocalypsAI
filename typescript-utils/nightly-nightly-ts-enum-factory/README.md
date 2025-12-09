# nightly-ts-enum-factory

Convert CLI input to TypeScript enums with optional whimsy! Supports:
- Uppercase enum keys
- Random suffixes
- Emoji prefixes
- Snake-case conversion

Example:
```bash
$ ts-enum-factory --input "Red Green Blue" --suffix -tone --emoji 🎨
export enum Colors {
  🎨RedTone = 'Red',
  🎨GreenTone = 'Green',
  🎨BlueTone = 'Blue'
}
```
