#!/usr/bin/env ts-node

import { decodeEmojis } from "./decoder";

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: ts-node src/cli.ts \"<emoji string>\"");
    process.exit(1);
  }
  const input = args.join(" ");
  const results = decodeEmojis(input);
  const tokens = input.trim().split(/\s+/);
  tokens.forEach((token, idx) => {
    const meanings = results[idx];
    if (meanings.length > 0) {
      console.log(`${token}: ${meanings.join(", ")}`);
    } else {
      console.log(`${token}: (no known meaning)`);
    }
  });
}

main();
