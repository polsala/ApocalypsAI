type Resource = keyof typeof PRICE_TABLE;

/**
 * Static price table for known resources. Adjust as needed.
 */
export const PRICE_TABLE = {
  water: 2,
  food: 5,
  ammo: 10,
  medicine: 20
} as const;

/**
 * Calculates the total barter value for a given resource map.
 *
 * @param resources - An object where keys are resource names and values are quantities.
 * @returns The total value as a number.
 * @throws If an unknown resource is encountered or a quantity is negative/non‑numeric.
 */
export function calculateValue(resources: Record<string, unknown>): number {
  if (typeof resources !== 'object' || resources === null) {
    throw new Error('Resources must be a non‑null object');
  }

  let total = 0;
  for (const [key, rawQty] of Object.entries(resources)) {
    const resource = key as Resource;
    if (!(resource in PRICE_TABLE)) {
      throw new Error(`Unknown resource: ${resource}`);
    }
    const qty = Number(rawQty);
    if (!Number.isFinite(qty) || qty < 0) {
      throw new Error(`Invalid quantity for ${resource}: ${rawQty}`);
    }
    total += PRICE_TABLE[resource] * qty;
  }
  return total;
}

/**
 * CLI entry point. Expects a single argument: a JSON string representing the resources map.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node index.js \'{\"water\":10,\"food\":5}\'');
    process.exit(1);
  }
  let resources: Record<string, unknown>;
  try {
    resources = JSON.parse(args[0]);
  } catch (e) {
    console.error('Failed to parse JSON input:', e.message);
    process.exit(1);
  }
  try {
    const total = calculateValue(resources);
    console.log(`Total barter value: ${total}`);
  } catch (e) {
    console.error('Error calculating value:', e.message);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

