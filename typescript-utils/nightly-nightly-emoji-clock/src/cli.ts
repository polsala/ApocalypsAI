#!/usr/bin/env ts-node
import { timeToClockEmoji } from "./emojiClock";

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: emoji-clock <HH:MM>");
    process.exit(1);
  }
  try {
    const emoji = timeToClockEmoji(args[0]);
    console.log(emoji);
  } catch (e:any) {
    console.error(e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
