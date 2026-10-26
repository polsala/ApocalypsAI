# nightly-apocalypse-text-stylizer

Utility that converts ordinary text into a post‑apocalyptic stylized version using Unicode symbols. Useful for adding flair to messages, logs, or social posts.

## Install

```sh
npm install -g nightly-apocalypse-text-stylizer
```

## Usage

```sh
npx nightly-apocalypse-text-stylizer "Hello World"
```

or pipe:

```sh
echo "Survive" | npx nightly-apocalypse-text-stylizer
```

## How it works

Replaces selected Latin characters with visually similar Unicode glyphs (e.g., a → α, e → ε, t → †) and adds occasional “☢” symbols.

## API

```ts
import { stylize } from "nightly-apocalypse-text-stylizer";

const fancy = stylize("Hello");
```
