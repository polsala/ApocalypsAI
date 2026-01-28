#!/usr/bin/env node
import { intToRoman, romanToInt } from "./roman";

function printUsage() {
  console.log('Usage:');
  console.log('  roman <number>          Convert integer (1-3999) to Roman numeral');
  console.log('  roman <roman>           Convert Roman numeral to integer');
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    printUsage();
    process.exit(1);
  }
  const input = args[0];
  if (/^[0-9]+$/.test(input)) {
    const num = parseInt(input, 10);
    try {
      console.log(intToRoman(num));
    } catch (e) {
      console.error(e.message);
      process.exit(1);
    }
  } else {
    try {
      console.log(romanToInt(input).toString());
    } catch (e) {
      console.error(e.message);
      process.exit(1);
    }
  }
}

if (require.main === module) {
  main();
}
