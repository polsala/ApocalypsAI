function generatePalette(): string {
  const cols = 16;
  const lines: string[] = [];
  for (let i = 0; i < 256; i++) {
    const color = `\\x1b[38;5;${i}m${i.toString().padStart(3, ' ')}\\x1b[0m`;
    if (i % cols === 0) {
      lines.push(color);
    } else {
      lines[lines.length - 1] += ' ' + color;
    }
  }
  return lines.join('\n');
}

// If run directly, output the palette to stdout
if (require.main === module) {
  console.log(generatePalette());
}

export { generatePalette };
