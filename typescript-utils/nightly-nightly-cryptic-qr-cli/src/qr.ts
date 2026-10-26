/**
 * Generate a deterministic ASCII‑art “QR‑like” code from a string.
 *
 * The algorithm:
 * 1. Compute a simple hash by summing character codes.
 * 2. If the sum is even, use `#` as the fill character; otherwise `@`.
 * 3. Create a box whose inner width is `text.length + 2` and inner height is 3.
 *
 * @param text Input string
 * @returns Multiline string containing the ASCII art
 */
export function generateQrAscii(text: string): string {
  const sum = Array.from(text).reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
  const fill = sum % 2 === 0 ? "#" : "@";
  const innerWidth = text.length + 2;
  const topBottom = "+" + "-".repeat(innerWidth) + "+";
  const middle = "|" + fill.repeat(innerWidth) + "|";
  // three middle rows for a compact QR look
  return [topBottom, middle, middle, middle, topBottom].join("\n");
}
