# nightly-emoji-moodboard

A whimsical React web app that displays a random emoji mood board based on the current hour. Click the button to refresh and get a new set of emojis that match the time of day.

## Features

- Shows 5 emojis that reflect the current hour (morning, afternoon, evening, night)
- Click "Refresh" to generate a new random selection
- Fully offline – no external API calls
- Includes Jest + React Testing Library tests

## Usage

```sh
# Install dependencies
npm install

# Run the development server
npm start

# Run tests
npm test
```

## How it works

The app maps the hour of the day to a theme (morning, afternoon, evening, night) and selects emojis from a predefined list for that theme. The selection is random each time you click *Refresh*.
