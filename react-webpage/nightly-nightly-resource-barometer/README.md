# Nightly Resource Barometer

## Overview
A whimsical yet useful React web app that visualises three essential postâapocalyptic resources â **Water**, **Food**, and **Ammo** â as adjustable sliders. The app computes an overall *Survival Rating* (the average of the three percentages) so you can quickly gauge how prepared you are for the next fallout.

## Features
- Three sliders (0â100%) for water, food, and ammo.
- Realâtime update of each resource value.
- Automatic calculation of a Survival Rating.
- Simple, zeroâdependency UI (just React).

## Installation
```bash
# Clone the repository (or copy the generated folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-resource-barometer

# Install dependencies
npm install
```

## Running the App
```bash
npm start
```
The app will be available at `http://localhost:3000`.

## Testing
```bash
npm test
```
The test suite uses **Jest** and **@testing-library/react** to verify that the sliders correctly affect the Survival Rating.

## License
MIT â see the root LICENSE file.
