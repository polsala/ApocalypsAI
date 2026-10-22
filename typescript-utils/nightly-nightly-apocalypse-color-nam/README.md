# Nightly Apocalypse Color Namer

Utility that maps a hex color code to a post‑apocalyptic themed name (e.g., `#ff4500` → `Molten Ember`). Useful for adding flavor to logs, UI themes, or story writing.

## Installation

```sh
npm install -g nightly-apocalypse-color-namer
```

## Usage

```sh
npx nightly-apocalypse-color-namer #ff4500
# => Molten Ember
```

## API

```ts
import { getApocalypseName } from "./colorNamer";

const name = getApocalypseName("#ff4500");
```

## How it works

The utility contains a small palette of themed colors. It converts the input hex to RGB, computes Euclidean distance to each palette entry, and returns the closest name.
