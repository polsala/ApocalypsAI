#!/usr/bin/env node
import { generateAsciiQr } from "./index";

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error("Usage: nightly-qr-cryptic <text>");
  process.exit(1);
}

const text = args.join(" ");
console.log(generateAsciiQr(text));
