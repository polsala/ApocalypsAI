import { generateAsciiQr } from "../src/index";

function normalize(str: string): string {
  return str.trim().replace(/\r\n/g, "\n");
}

// Expected output for the single character "A" (ASCII 65 => 01000001)
const expected = `
█████
█ █ █
█   █
█ █ █
█████
`;

const result = generateAsciiQr("A");
if (normalize(result) !== normalize(expected)) {
  throw new Error(`Unexpected output.\nGot:\n${result}\nExpected:\n${expected}`);
}

console.log("test passed");
