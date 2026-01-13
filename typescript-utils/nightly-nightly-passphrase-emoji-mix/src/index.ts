import * as fs from 'fs';

/**
 * Small static word list â feel free to extend.
 */
const WORDS = [
  'alpha', 'bravo', 'charlie', 'delta', 'echo',
  'foxtrot', 'golf', 'hotel', 'india', 'juliet'
];

/**
 * Small static emoji list â postâapocalyptic vibes included.
 */
const EMOJIS = [
  'ð', 'ð', 'ð', 'ð¥', 'ð§',
  'â¡', 'ð§©', 'ð¡ï¸', 'ð¡ï¸', 'â¢ï¸'
];

/**
 * Generate a passphrase consisting of `wordCount` random words and `emojiCount` random emojis.
 * The function is pure â it only depends on `Math.random`.
 */
export function generatePassphrase(wordCount: number, emojiCount: number): string {
  if (wordCount < 0 || emojiCount < 0) {
    throw new Error('wordCount and emojiCount must be nonânegative');
  }

  const chosenWords: string[] = [];
  for (let i = 0; i < wordCount; i++) {
    const idx = Math.floor(Math.random() * WORDS.length);
    chosenWords.push(WORDS[idx]);
  }

  const chosenEmojis: string[] = [];
  for (let i = 0; i < emojiCount; i++) {
    const idx = Math.floor(Math.random() * EMOJIS.length);
    chosenEmojis.push(EMOJIS[idx]);
  }

  return [...chosenWords, ...chosenEmojis].join(' ');
}

/**
 * Simple CLI wrapper â parses `--words` and `--emojis` flags.
 */
function parseArgs(): { wordCount: number; emojiCount: number } {
  const args = process.argv.slice(2);
  let wordCount = 4;
  let emojiCount = 2;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--words' && i + 1 < args.length) {
      wordCount = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--emojis' && i + 1 < args.length) {
      emojiCount = parseInt(args[i + 1], 10);
      i++;
    }
  }

  return { wordCount, emojiCount };
}

if (require.main === module) {
  const { wordCount, emojiCount } = parseArgs();
  const phrase = generatePassphrase(wordCount, emojiCount);
  console.log(phrase);
}

export default generatePassphrase;
