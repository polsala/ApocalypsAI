# nightly-planetary-time-converter

A tiny Node.js utility that translates an Earth UTC timestamp into the local time on a chosen planet.

## Supported planets
- **mars** – a sol is 24 h 39 m 35.244 s (88 775.244 s)
- **venus** – a Venusian day is 243 Earth days (20 995 200 s)

## Installation
```bash
# No external dependencies – just copy the files
# If you want to use it as a CLI, make sure Node.js (>=14) is installed.
```

## Usage (CLI)
```bash
node src/main.js --planet mars --time "1970-01-01T01:00:00Z"
```
Output example:
```
Planet Mars time: Sol 0, 01:01:39
```

## API
You can also require the module in your own code:
```js
const { convertEarthToPlanet } = require('../src/main');

const result = convertEarthToPlanet('1970-01-01T01:00:00Z', 'mars');
console.log(result);
// => { sol: 0, hour: 1, minute: 1, second: 39 }
```

## Testing
Run the test suite with:
```bash
node tests/test_main.js
```
All tests are deterministic and do not require network access.
