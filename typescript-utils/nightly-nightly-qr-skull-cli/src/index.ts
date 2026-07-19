#!/usr/bin/env node
export function generateSkullQR(text: string): string {
  const skull = "☠";
  const skullBlock = `${skull}${skull}\n${skull}${skull}`;
  const spaceBlock = "  \n  ";

  const lines: string[] = ["", ""];
  for (const ch of text) {
    const block = ch.charCodeAt(0) % 2 === 0 ? skullBlock : spaceBlock;
    const [top, bottom] = block.split("\n");
    lines[0] += top;
    lines[1] += bottom;
  }
  return lines.join("\n");
}

// CLI execution
if (require.main === module) {
  const input = process.argv[2] ?? "";
  console.log(generateSkullQR(input));
}
