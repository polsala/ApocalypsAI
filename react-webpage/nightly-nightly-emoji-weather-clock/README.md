# nightly-emoji-weather-clock

A tiny React app that displays a live digital clock with a weatherâthemed emoji that changes based on the hour of the day.

## Features

- Updates every second using `setInterval`.
- Shows a sun ð during daytime (6â¯am â 5â¯pm), a moon ð at night (6â¯pm â 5â¯am).
- Shows a cloud âï¸ for the âovercastâ hour (12â¯pm â 1â¯pm) as a playful surprise.
- Fully clientâside â no external APIs required.
- Includes a Jest + React Testing Library test suite that runs offline.

## Getting Started

```bash
# Clone the repository (or copy the generated folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-weather-clock

# Install dependencies
npm install

# Run the development server
npm start
```

Open `http://localhost:3000` in your browser to see the clock in action.

## Running Tests

```bash
npm test
```

The test suite checks that the correct emoji is rendered for mocked times.

## Project Structure

- `src/` â React source files.
- `public/` â Static HTML template.
- `tests/` â Jest test files.
- `package.json` â Project metadata and scripts.

## License

MIT â see the LICENSE file in the root of the main repository.

