#!/usr/bin/env node
const { decodeEmojis } = require("./decoder");
const fs = require("fs");

let input = process.argv.slice(2).join(" ");

if (!input) {
  // read from stdin if no args
  const stdin = fs.readFileSync(0, "utf-8").trim();
  input = stdin;
}

if (!input) {
  console.error("Usage: emoji-decoder <emoji string>");
  process.exit(1);
}

console.log(decodeEmojis(input));
