# nightly-planetary-age-calculator

Calculate your age on other planets.

## Installation

```sh
npm install -g nightly-planetary-age-calculator
```

## Usage

```sh
npx nightly-planetary-age-calculator 30
```

Outputs a JSON object mapping planet names to ages (in planetary years), rounded to two decimal places.

## API

```ts
import { calculatePlanetaryAges } from 'nightly-planetary-age-calculator';

const ages = calculatePlanetaryAges(30);
console.log(ages);
// {
//   Mercury: 124.6,
//   Venus: 48.73,
//   Earth: 30,
//   Mars: 15.95,
//   Jupiter: 2.53,
//   Saturn: 1.02,
//   Uranus: 0.36,
//   Neptune: 0.18,
//   Pluto: 0.12
// }
```

The function throws an error for negative or non‑numeric inputs.
