export function encodeToAsciiArt(text: string): string {
  const rows = text.split('').map(ch => {
    const bin = ch.charCodeAt(0).toString(2).padStart(8, '0');
    return bin.replace(/0/g, '░').replace(/1/g, '█');
  });
  return rows.join('\n');
}

if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node index.js <text>');
    process.exit(1);
  }
  console.log(encodeToAsciiArt(input));
}
