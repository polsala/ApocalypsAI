import { randomInt } from 'crypto';

const WORDS = [
  'sun',
  'moon',
  'star',
  'river',
  'mountain',
  'forest',
  'wolf',
  'fox',
  'eagle',
  'storm'
];

const EMOJIS = [
  '🌞',
  '🌙',
  '⭐',
  '🌊',
  '⛰️',
  '🌲',
  '🐺',
  '🦊',
  '🦅',
  '⛈️'
];

/**
 * Generate a whimsical passphrase.
 * Format: <emoji>-<word>-<number>-<word>
 */
export function generatePassphrase(): string {
  const word1 = WORDS[randomInt(0, WORDS.length)];
  const word2 = WORDS[randomInt(0, WORDS.length)];
  const emoji = EMOJIS[randomInt(0, EMOJIS.length)];
  const number = randomInt(0, 100);
  return `${emoji}-${word1}-${number}-${word2}`;
}

// If executed directly, output a passphrase to stdout.
if (require.main === module) {
  console.log(generatePassphrase());
}
