#!/usr/bin/env node
import { Buffer } from 'buffer';

const HEX_TO_EMOJI: Record<string, string> = {
  '0': '0️⃣',
  '1': '1️⃣',
  '2': '2️⃣',
  '3': '3️⃣',
  '4': '4️⃣',
  '5': '5️⃣',
  '6': '6️⃣',
  '7': '7️⃣',
  '8': '8️⃣',
  '9': '9️⃣',
  'a': '🅰️',
  'b': '🅱️',
  'c': '🆑',
  'd': '🆓',
  'e': '🆔',
  'f': '🆕',
};

const EMOJI_TO_HEX: Record<string, string> = Object.entries(HEX_TO_EMOJI).reduce(
  (acc, [hex, emoji]) => {
    acc[emoji] = hex;
    return acc;
  },
  {} as Record<string, string>
);

export function encodeToEmoji(input: string): string {
  const hex = Buffer.from(input, 'utf8').toString('hex');
  return hex.split('').map(ch => HEX_TO_EMOJI[ch]).join('');
}

export function decodeFromEmoji(emojiStr: string): string {
  const hexChars = Array.from(emojiStr).map(ch => {
    const hex = EMOJI_TO_HEX[ch];
    if (hex === undefined) {
      throw new Error(`Unrecognized emoji: ${ch}`);
    }
    return hex;
  });
  const hex = hexChars.join('');
  return Buffer.from(hex, 'hex').toString('utf8');
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: hex-emoji-encoder [--decode] <text>');
    process.exit(1);
  }
  const decode = args[0] === '--decode';
  const text = decode ? args[1] ?? '' : args[0];
  try {
    const result = decode ? decodeFromEmoji(text) : encodeToEmoji(text);
    console.log(result);
  } catch (e) {
    console.error('Error:', (e as Error).message);
    process.exit(1);
  }
}
