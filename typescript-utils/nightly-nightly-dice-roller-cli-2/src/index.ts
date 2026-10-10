// nightly-dice-roller-cli
// TypeScript implementation of a dice‑notation parser and roller.
// SPDX‑License-Identifier: MIT

export interface DiceNotation {
  count: number;
  sides: number;
  modifier: number;
}

/**
 * Parse a dice notation string.
 * Supported forms: "d20", "2d6", "3d8+2", "4d10-1".
 */
export function parseDiceNotation(input: string): DiceNotation {
  const trimmed = input.trim().toLowerCase();
  const regex = /^(?:(\d*)d(\d+))(?:([+-]\d+))?$/;
  const match = trimmed.match(regex);
  if (!match) {
    throw new Error(`Invalid dice notation: ${input}`);
  }
  const count = match[1] === "" ? 1 : parseInt(match[1], 10);
  const sides = parseInt(match[2], 10);
  const modifier = match[3] ? parseInt(match[3], 10) : 0;
  return { count, sides, modifier };
}

/**
 * Roll dice according to the parsed notation.
 * An optional RNG function can be injected for deterministic testing.
 */
export function rollDice(notation: DiceNotation, rng: () => number = Math.random): number {
  const rolls: number[] = [];
  for (let i = 0; i < notation.count; i++) {
    // rng returns [0,1); scale to [1, sides]
    const roll = Math.floor(rng() * notation.sides) + 1;
    rolls.push(roll);
  }
  const sum = rolls.reduce((a, b) => a + b, 0);
  return sum + notation.modifier;
}

/**
 * CLI entry point.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: nightly-dice-roller-cli <dice-notation>');
    process.exit(1);
  }
  try {
    const notation = parseDiceNotation(args[0]);
    const result = rollDice(notation);
    console.log(`Rolling ${args[0]} => ${result}`);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
