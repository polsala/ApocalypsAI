# Nightly Cosmic Compass

A whimsical Node.js utility that helps you navigate the cosmos by providing a celestial direction based on the current time and a user-provided 'cosmic event'. Think of it as a fun, abstract compass for your daily journey through the universe.

## Philosophy

Embrace the unknown with a touch of whimsy. This tool is designed to spark imagination and provide a lighthearted, yet functional, way to orient yourself in the grand tapestry of time and space.

## Installation

1. Clone this repository.
2. Navigate to the `utils/nightly-cosmic-compass` directory.
3. Run `npm install` to install dependencies.

## Usage

Run the utility from your terminal:

```bash
node src/main.js "Supernova Burst"
```

Replace `"Supernova Burst"` with any string representing your chosen cosmic event. The utility will output a direction (e.g., 'North-East', 'South-West') and a whimsical description.

## How it Works

The utility combines the current time (hours, minutes, seconds) with a hash of the provided cosmic event string to generate a pseudo-random but deterministic direction. This ensures that for the same time and event, you'll always get the same result.

## Contributing

Feel free to fork this repository and submit pull requests with new features or improvements. We encourage creative additions!

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
