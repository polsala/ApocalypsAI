export function generateAsciiQr(text: string): string {
  // Simple placeholder QR generator:
  // For each character, convert its char code to an 8‑bit binary string.
  // Map '1' → '█' and '0' → ' '. Each character becomes one line of 8 symbols.
  const rows: string[] = [];
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    const bin = code.toString(2).padStart(8, '0');
    const line = bin.split('').map(b => b === '1' ? '█' : ' ').join('');
    rows.push(line);
  }
  return rows.join('\n');
}
