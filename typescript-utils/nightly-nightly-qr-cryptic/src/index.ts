export function generateAsciiQr(text: string): string {
  // Convert each character to an 8‑bit binary string and concatenate
  const binary = Array.from(text)
    .map(ch => ch.charCodeAt(0).toString(2).padStart(8, "0"))
    .join("");

  // Determine a square-ish grid size
  const size = Math.ceil(Math.sqrt(binary.length));
  const padded = binary.padEnd(size * size, "0");

  const rows: string[] = [];
  for (let i = 0; i < size; i++) {
    const rowBits = padded.slice(i * size, (i + 1) * size);
    const row = rowBits
      .split("")
      .map(b => (b === "1" ? "█" : " "))
      .join("");
    rows.push(row);
  }

  // Add a border around the art
  const border = "█".repeat(size + 2);
  const borderedRows = rows.map(r => `█${r}█`);
  return [border, ...borderedRows, border].join("\n");
}

export default generateAsciiQr;
