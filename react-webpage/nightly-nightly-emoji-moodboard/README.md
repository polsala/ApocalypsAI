# Emoji Moodboard

A whimsical React web app that turns a user‑entered mood into a curated emoji moodboard.

## Features

- Input a mood (e.g., happy, sad, excited)
- See a set of emojis that represent the mood
- No external API calls – all data is local

## Install & Run

```sh
npm install
npm start
```

The app will be available at http://localhost:3000.

## Test

```sh
npm test
```

## How it works

The app contains a small hard‑coded map from moods to emoji arrays. When the user submits a mood, the matching emojis are displayed. If the mood is unknown, a fallback set is shown.
