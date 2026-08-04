#!/usr/bin/env node
import { generateQrAscii } from "./qr";

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: npx ts-node src/index.ts <text>");
    process.exit(1);
  }
  const text = args.join(" ");
  console.log(generateQrAscii(text));
}

main();
