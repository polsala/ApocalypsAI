# Wasteland Calendar Converter

A tiny TypeScript utility that translates a Gregorian date (YYYY‑MM‑DD) into the fictional Wasteland Calendar used by the survivors of the Great Collapse.

## How it works

- The Wasteland year starts at **2077** (the year the apocalypse began).  
  Wasteland year = Gregorian year - 2077.
- Months are renamed to reflect the harsh environment:

| Number | Name |
|--------|------|
| 1 | Dust |
| 2 | Ash |
| 3 | Scorch |
| 4 | Ember |
| 5 | Ruin |
| 6 | Fallout |
| 7 | Barren |
| 8 | Mirage |
| 9 | Cinder |
|10 | Blight |
|11 | Dusk |
|12 | Nightfall |

- The day of month stays the same.

## Usage

```sh
npx ts-node src/index.ts 2025-03-14
# → 48 Scorch 14
```

You can also import the conversion function in your own TypeScript projects:

```ts
import { convertToWasteland } from "./index";

console.log(convertToWasteland("2025-03-14")); // 48 Scorch 14
```

## Testing

Run the bundled tests with:

```sh
npm test
```

(Tests are written in TypeScript and use Node's built‑in `assert` module.)

## License

MIT
