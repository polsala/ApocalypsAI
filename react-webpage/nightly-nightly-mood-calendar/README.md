# Nightly Mood Calendar

A whimsical React component that displays a calendar of emojis representing your mood for each day. The mood for each day is deterministically derived from the date, so the same date always shows the same emoji.

## Usage

```bash
npm install
npm start
```

Import `MoodCalendar` and embed it:

```jsx
import MoodCalendar from './src/App.jsx';

<MoodCalendar startDate="2023-01-01" days={30} />
```

## How it works

The component calculates the number of days since the start date and selects an emoji from a fixed list using modulo arithmetic.

## Testing

Run `npm test` to execute the Jest test suite.
