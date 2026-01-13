# Apocalypse Countdown

A whimsical React app that counts down to the next apocalypse. It displays a live timer and a random apocalypseâthemed message.

## Features
- Live countdown to a configurable target date
- Randomly chosen dramatic messages each render
- Simple, zeroâconfiguration start with npm

## Getting Started

```bash
# Clone the repository (or copy the generated folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-apocalypse-countdown

# Install dependencies
npm install

# Start the development server
npm start
```

Open your browser at `http://localhost:8080` to see the countdown.

## Building for Production

```bash
npm run build
```

The production bundle will be placed in the `dist/` folder.

## Testing

```bash
npm test
```

The test suite uses Jest and React Testing Library to verify the countdown logic with mocked time.

## Customizing the Target Date
Edit `src/App.jsx` and change the `targetDate` constant to any future ISOâ8601 date string.

---

*Built by the ApocalypsAI Nightly Integrator agent.*
