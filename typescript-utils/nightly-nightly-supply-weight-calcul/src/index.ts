export type WeightUnit = 'g' | 'kg' | 'lb' | 'oz';

export interface SupplyItem {
  name: string;
  weight: number; // weight per single item
  unit: WeightUnit;
  quantity: number;
}

// Conversion factors to grams
const toGrams: Record<WeightUnit, number> = {
  g: 1,
  kg: 1000,
  lb: 453.59237,
  oz: 28.349523125,
};

export function convertToGrams(value: number, unit: WeightUnit): number {
  return value * toGrams[unit];
}

export function convertFromGrams(value: number, unit: WeightUnit): number {
  return value / toGrams[unit];
}

/**
 * Compute total weight of a collection of supplies in the desired unit.
 * @param items Array of supply items.
 * @param targetUnit Desired output unit (default: grams).
 * @returns Total weight expressed in `targetUnit`.
 */
export function computeTotalWeight(items: SupplyItem[], targetUnit: WeightUnit = 'g'): number {
  const totalGrams = items.reduce((sum, item) => {
    const perItemGrams = convertToGrams(item.weight, item.unit);
    return sum + perItemGrams * item.quantity;
  }, 0);
  return convertFromGrams(totalGrams, targetUnit);
}

// CLI handling – only runs when executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  let targetUnit: WeightUnit = 'g';
  const unitFlagIdx = args.indexOf('--unit');
  if (unitFlagIdx !== -1 && args[unitFlagIdx + 1]) {
    const candidate = args[unitFlagIdx + 1] as WeightUnit;
    if (toGrams[candidate]) {
      targetUnit = candidate;
      args.splice(unitFlagIdx, 2);
    } else {
      console.error(`Unsupported unit: ${candidate}`);
      process.exit(1);
    }
  }

  let data = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => data += chunk);
  process.stdin.on('end', () => {
    try {
      const items: SupplyItem[] = JSON.parse(data);
      const total = computeTotalWeight(items, targetUnit);
      console.log(`Total weight: ${total.toFixed(3)} ${targetUnit}`);
    } catch (e) {
      console.error('Failed to parse input JSON:', (e as Error).message);
      process.exit(1);
    }
  });
}
