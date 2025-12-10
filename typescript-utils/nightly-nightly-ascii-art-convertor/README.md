# Nightly ASCII Art Convertor

A whimsical yet practical TypeScript CLI tool that transforms images into ASCII art. Perfect for adding flair to your terminal, creating ASCII signatures, or just having fun with retro aesthetics.

## Features

- Convert PNG, JPG, and GIF images to ASCII art
- Three output styles: Block, Dots, and Braille
- Adjustable width and contrast
- Save to text file or display directly in terminal
- Zero external dependencies (pure TypeScript)

## Installation

```bash
npm install -g nightly-ascii-art-convertor
```

## Usage

```bash
# Convert image with default settings
ascii-art convert input.png

# Convert with custom width and style
ascii-art convert input.png --width 120 --style dots

# Save to file
ascii-art convert input.png --output ascii_art.txt

# View help
ascii-art --help
```

## Styles

- **Block**: Uses block characters (█) - bold and high contrast
- **Dots**: Uses dot patterns (⠂) - medium detail
- **Braille**: Uses Braille patterns (⣿) - finest detail

## Examples

```bash
# Create ASCII art signature
ascii-art convert photo.jpg --width 80 --style braille --output signature.txt

# Quick preview
ascii-art convert meme.jpg --width 60
```

## License

MIT
