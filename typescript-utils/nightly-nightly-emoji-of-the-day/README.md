# nightly-emoji-of-the-day

Deterministically generates a daily emoji based on the date, useful for mood tracking or daily standups.

## Usage

```bash
# Install
npm install nightly-emoji-of-the-day

# Import in TypeScript
import { emojiOfTheDay } from 'nightly-emoji-of-the-day';

console.log(emojiOfTheDay()); // Emoji for today
console.log(emojiOfTheDay(new Date('2023-10-01'))); // Emoji for Oct 1, 2023
```

## API

- `emojiOfTheDay(date?: Date): string`  
  Returns the emoji for the given date or today if omitted.

## Example

```ts
import { emojiOfTheDay } from 'nightly-emoji-of-the-day';

console.log(`Today's emoji: ${emojiOfTheDay()}`);
```
