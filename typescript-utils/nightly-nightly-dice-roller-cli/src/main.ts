import * as process from "process";

/**
 * Parse a dice notation string like "2d6+3" or "d20".
 * Returns an object with number of dice, sides per die, and modifier.
 */
export function parseNotation(notation: string): { count: number; sides: number; modifier: number } {
  const regex = /^(?:(\d*)d(\d+))(?:([+-])(\d+))?$/i;
  const match = notation.replace(/\s+/g, "").match(regex);
  if (!match) {
    throw new Error(`Invalid dice notation: ${notation}`);
  }
  const count = match[1] ? parseInt(match[1], 10) : 1;
  const sides = parseInt(match[2], 10);
  const sign = match[3];
  const modVal = match[4] ? parseInt(match[4], 10) : 0;
  const modifier = sign === "-" ? -modVal : modVal;
  return { count, sides, modifier };
}

/**
 * Roll a single die with given number of sides using Math.random.
 */
export function rollDie(sides: number): number {
  return Math.floor(Math.random() * sides) + 1;
}

/**
 * Convert a roll value (1‑6) to a Unicode dice face. For other values, return the number as a string.
 */
export function diceUnicode(value: number): string {
  const faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
  return value >= 1 && value <= 6 ? faces[value - 1] : value.toString();
}

/**
 * Roll dice according to the parsed notation. Returns each individual roll and the total (including modifier).
 */
export function rollDice(notation: string): { rolls: number[]; total: number; modifier: number } {
  const { count, sides, modifier } = parseNotation(notation);
  const rolls: number[] = [];
  for (let i = 0; i < count; i++) {
    rolls.push(rollDie(sides));
  }
  const sum = rolls.reduce((a, b) => a + b, 0);
  return { rolls, total: sum + modifier, modifier };
}

/**
 * CLI entry point.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: npx ts-node src/main.ts <dice-notation>");
    process.exit(1);
  }
  const notation = args[0];
  try {
    const { rolls, total, modifier } = rollDice(notation);
    console.log(`Rolling ${notation}`);
    rolls.forEach((r, idx) => {
      console.log(`Roll ${idx + 1}: ${diceUnicode(r)} (${r})`);
    });
    if (modifier !== 0) {
      const sign = modifier > 0 ? "+" : "-";
      console.log(`Modifier: ${sign}${Math.abs(modifier)}`);
    }
    console.log(`Total: ${total}`);
  } catch (e) {
    console.error(e instanceof Error ? e.message : String(e));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

