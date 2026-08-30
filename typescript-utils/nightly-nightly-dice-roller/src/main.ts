#!/usr/bin/env ts-node

/**
 * nightly-dice-roller – a tiny CLI to roll dice using RPG notation.
 *
 * Exported functions are kept pure for unit‑testing.
 */

type Parsed = {
  count: number;
  sides: number;
  modifier: number;
};

/** Parse a dice notation string like "2d6+3".
 *  Returns the number of dice, the number of sides, and the modifier.
 */
export function parseNotation(notation: string): Parsed {
  const regex = /^\s*(\d*)d(\d+)([+-]\d+)?\s*$/i;
  const match = notation.match(regex);
  if (!match) {
    throw new Error(`Invalid dice notation: ${notation}`);
  }
  const count = match[1] ? parseInt(match[1], 10) : 1;
  const sides = parseInt(match[2], 10);
  const modifier = match[3] ? parseInt(match[3], 10) : 0;
  if (sides < 1) {
    throw new Error('Dice must have at least one side');
  }
  return { count, sides, modifier };
}

/** Roll the dice according to a parsed notation.
 *  Returns an array of individual roll results.
 */
export function rollDice(parsed: Parsed): number[] {
  const { count, sides } = parsed;
  const rolls: number[] = [];
  for (let i = 0; i < count; i++) {
    const roll = Math.floor(Math.random() * sides) + 1;
    rolls.push(roll);
  }
  return rolls;
}

/** Convert a numeric die value to a Unicode die face when possible. */
export function dieFace(value: number): string {
  const faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
  if (value >= 1 && value <= 6) {
    return faces[value - 1];
  }
  return value.toString();
}

/** Format the final output string shown to the user. */
export function formatResult(parsed: Parsed, rolls: number[]): string {
  const faces = rolls.map(dieFace).join(' ');
  const sum = rolls.reduce((a, b) => a + b, 0) + parsed.modifier;
  const modPart = parsed.modifier !== 0 ? ` ${parsed.modifier > 0 ? '+' : '-'} ${Math.abs(parsed.modifier)}` : '';
  const notation = `${parsed.count}d${parsed.sides}${parsed.modifier !== 0 ? (parsed.modifier > 0 ? '+' + parsed.modifier : parsed.modifier) : ''}`;
  return `🎲 ${notation} → [${faces}]${modPart} = ${sum}`;
}

/** CLI entry point */
if (require.main === module) {
  const arg = process.argv[2];
  if (!arg) {
    console.error('Usage: nightly-dice-roller <notation>');
    process.exit(1);
  }
  try {
    const parsed = parseNotation(arg);
    const rolls = rollDice(parsed);
    console.log(formatResult(parsed, rolls));
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
