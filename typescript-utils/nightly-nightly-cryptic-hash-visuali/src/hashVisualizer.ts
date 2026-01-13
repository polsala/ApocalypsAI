import { createHash } from 'crypto';

/**
 * Map a single hexadecimal digit to a block character.
 * 0â3 â â, 4â7 â â, 8âb â â, câf â â
 */
function hexToBlock(hex: string): string {
  const mapping: Record<string, string> = {
    '0': 'â', '1': 'â', '2': 'â', '3': 'â',
    '4': 'â', '5': 'â', '6': 'â', '7': 'â',
    '8': 'â', '9': 'â', 'a': 'â', 'b': 'â',
    'c': 'â', 'd': 'â', 'e': 'â', 'f': 'â'
  };
  return mapping[hex.toLowerCase()];
}

/**
 * Produce a visual representation of the SHAâ256 hash of `input`.
 * The result is four lines, each 16 characters long, joined by "
".
 */
export function visualizeHash(input: string): string {
  const hashHex = createHash('sha256').update(input).digest('hex');
  const blocks = hashHex.split('').map(hexToBlock);
  const width = 16;
  const rows: string[] = [];
  for (let i = 0; i < blocks.length; i += width) {
    rows.push(blocks.slice(i, i + width).join(''));
  }
  return rows.join('
');
}

