const emojis = ['😀','😃','😄','😁','😆','😅','😂','🤣'];

/**
 * Maps a single character to an emoji based on its Unicode code point.
 */
function charToEmoji(ch: string): string {
  const code = ch.charCodeAt(0);
  return emojis[code % emojis.length];
}

/**
 * Generates a square grid of emojis from the input string.
 */
function generateEmojiGrid(input: string): string[] {
  const chars = input.split('');
  const size = Math.ceil(Math.sqrt(chars.length));
  const total = size * size;
  // Pad with spaces if needed
  while (chars.length < total) {
    chars.push(' ');
  }
  const rows: string[] = [];
  for (let r = 0; r < size; r++) {
    let row = '';
    for (let c = 0; c < size; c++) {
      const idx = r * size + c;
      row += charToEmoji(chars[idx]);
    }
    rows.push(row);
  }
  return rows;
}

/**
 * Entry point – reads from CLI args or STDIN and prints the emoji grid.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const input = args.join(' ');
    const grid = generateEmojiGrid(input);
    console.log(grid.join('\n'));
  } else {
    // Read from STDIN
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      const input = data.trim();
      const grid = generateEmojiGrid(input);
      console.log(grid.join('\n'));
    });
  }
}

if (require.main === module) {
  main();
}
