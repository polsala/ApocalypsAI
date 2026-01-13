import { Buffer } from 'buffer';

// Mapping from hex digit to emoji
const hexToEmoji: Record<string, string> = {
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
  'd': '🆒',
  'e': '🆓',
  'f': '🆔'
};

// Reverse mapping for decoding
const emojiToHex: Record<string, string> = Object.fromEntries(
  Object.entries(hexToEmoji).map(([hex, emoji]) => [emoji, hex])
);

/**
 * Encode a UTF‑8 string into an emoji sequence.
 * @param input Plain text
 * @returns Emoji string
 */
export function encode(input: string): string {
  const bytes = Buffer.from(input, 'utf8');
  let result = '';
  for (const byte of bytes) {
    const hex = byte.toString(16).padStart(2, '0');
    result += hexToEmoji[hex[0]] + hexToEmoji[hex[1]];
  }
  return result;
}

/**
 * Decode an emoji sequence back to the original UTF‑8 string.
 * @param emojis Emoji string produced by {@link encode}
 * @returns Decoded plain text
 */
export function decode(emojis: string): string {
  let hexStr = '';
  let i = 0;
  while (i < emojis.length) {
    let matched = false;
    for (const [emoji, hex] of Object.entries(emojiToHex)) {
      if (emojis.startsWith(emoji, i)) {
        hexStr += hex;
        i += emoji.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      throw new Error('Invalid emoji sequence at position ' + i);
    }
  }
  if (hexStr.length % 2 !== 0) {
    throw new Error('Corrupted hex string length');
  }
  const bytes = [] as number[];
  for (let j = 0; j < hexStr.length; j += 2) {
    const byte = parseInt(hexStr.slice(j, j + 2), 16);
    bytes.push(byte);
  }
  return Buffer.from(bytes).toString('utf8');
}

/** Simple CLI handling */
function printUsage(): void {
  console.log('Usage:');
  console.log('  node index.ts encode <text>   # Encode text to emojis');
  console.log('  node index.ts decode <emoji>  # Decode emojis back to text');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    printUsage();
    process.exit(1);
  }
  const command = args[0];
  const payload = args.slice(1).join(' ');
  try {
    if (command === 'encode') {
      console.log(encode(payload));
    } else if (command === 'decode') {
      console.log(decode(payload));
    } else {
      printUsage();
      process.exit(1);
    }
  } catch (err) {
    console.error('Error:', (err as Error).message);
    process.exit(1);
  }
}

