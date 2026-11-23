export function encodeToAsciiArt(text: string): string[] {
  // Convert each character to its 8‑bit binary representation
  // and map 1 → "#", 0 → " "
  const lines: string[] = [];
  for (const ch of text) {
    const code = ch.charCodeAt(0);
    const binary = code.toString(2).padStart(8, "0");
    const line = binary
      .split("")
      .map((bit) => (bit === "1" ? "#" : " "))
      .join("");
    lines.push(line);
  }
  return lines;
}

// CLI handling – only runs when the file is executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node main.js <text>");
    process.exit(1);
  }
  const input = args.join(" ");
  const art = encodeToAsciiArt(input);
  console.log(art.join("\n"));
}
