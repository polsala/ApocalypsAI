#!/usr/bin/env node
import { generateChrono } from "./emojiChronometer";

function parseArgs(): { seconds: number; interval: number } {
  const args = process.argv.slice(2);
  let seconds = 0;
  let interval = 1;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--interval" && i + 1 < args.length) {
      interval = parseInt(args[i + 1], 10);
      i++;
    } else {
      seconds = parseInt(args[i], 10);
    }
  }
  return { seconds, interval };
}

const { seconds, interval } = parseArgs();
if (isNaN(seconds) || seconds <= 0) {
  console.error("Please provide a positive number of seconds.");
  process.exit(1);
}

const emojis = generateChrono(seconds, interval);
for (const e of emojis) {
  console.log(e);
}

