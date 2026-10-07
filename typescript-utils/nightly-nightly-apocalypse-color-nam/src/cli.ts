#!/usr/bin/env node
import { getApocalypseName } from "./colorNamer";

function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.error("Usage: nightly-apocalypse-color-namer <hex>");
    process.exit(1);
  }
  try {
    const name = getApocalypseName(arg);
    console.log(name);
  } catch (e) {
    console.error("Error:", (e as Error).message);
    process.exit(1);
  }
}

main();
