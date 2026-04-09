# nightly-plant-watering-scheduler

Calculate the next watering date for a plant.

## Installation

```sh
npm install
```

## Usage

```sh
node src/index.js <last-watered-ISO> <interval-days>
```

Example:

```sh
node src/index.js 2023-09-01 3
# => 2023-09-04
```

## API

```js
const { nextWaterDate } = require('./index');
```

```js
// Returns a string in YYYY-MM-DD format
const next = nextWaterDate('2023-09-01', 3);
console.log(next); // "2023-09-04"
```
