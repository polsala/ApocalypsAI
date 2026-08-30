#!/usr/bin/env node

export interface DiceSpec {
  count: number;
  sides: number;
  modifier: number;
}

/**
 * Parse a dice notation string like "2d6+1" or "d20".
 */
export function parseDiceNotation(notation: string): DiceSpec {
  const regex = /^(\d*)d(\d+)([+-]\d+)?$/i;
  const match = notation.replace(/\s+/g, "").match(regex);
  if (!match) {
    throw new Error(`Invalid dice notation: ${notation}`);
  }
  const count = match[1] ? parseInt(match[1], 10) : 1;
  const sides = parseInt(match[2], 10);
  const modifier = match[3] ? parseInt(match[3], 10) : 0;
  return { count, sides, modifier };
}

/**
 * Roll `count` dice with `sides` sides using the supplied random function.
 */
export function rollDice(count: number, sides: number, rand: () => number = Math.random): number[] {
  const rolls: number[] = [];
  for (let i = 0; i < count; i++) {
    const roll = Math.floor(rand() * sides) + 1;
    rolls.push(roll);
  }
  return rolls;
}

/**
 * Return an ASCII representation of a single die.
 * For standard 6‑sided dice we use a nice picture, otherwise we fall back to a simple box.
 */
export function asciiDie(value: number, sides: number): string {
  const diceArt: { [key: number]: string[] } = {
    1: [
      "+-------+",
      "|       |",
      "|   *   |",
      "|       |",
      "+-------+",
    ],
    2: [
      "+-------+",
      "| *     |",
      "|       |",
      "|     * |",
      "+-------+",
    ],
    3: [
      "+-------+",
      "| *     |",
      "|   *   |",
      "|     * |",
      "+-------+",
    ],
    4: [
      "+-------+",
      "| *   * |",
      "|       |",
      "| *   * |",
      "+-------+",
    ],
    5: [
      "+-------+",
      "| *   * |",
      "|   *   |",
      "| *   * |",
      "+-------+",
    ],
    6: [
      "+-------+",
      "| *   * |",
      "| *   * |",
      "| *   * |",
      "+-------+",
    ],
  };
  if (sides === 6 && diceArt[value]) {
    return diceArt[value].join("\n");
  }
  // Fallback for non‑standard dice
  return `+-------+\n|   ${value}   |\n+-------+`;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: dice <notation>");
    process.exit(1);
  }
  const spec = parseDiceNotation(args[0]);
  const rolls = rollDice(spec.count, spec.sides);
  const asciiFaces = rolls.map(v => asciiDie(v, spec.sides));
  // Combine the ASCII faces side‑by‑side
  const lineCount = asciiFaces[0].split("\n").length;
  const lines = Array.from({ length: lineCount }, (_, i) => {
    return asciiFaces.map(face => face.split("\n")[i]).join("   ");
  });
  console.log(lines.join("\n"));
  const total = rolls.reduce((a, b) => a + b, 0) + spec.modifier;
  const modSign = spec.modifier >= 0 ? "+" : "-";
  const modAbs = Math.abs(spec.modifier);
  console.log(`Rolls: [${rolls.join(", ")}] Modifier: ${modSign}${modAbs} Total: ${total}`);
}

if (require.main === module) {
  main();
}
