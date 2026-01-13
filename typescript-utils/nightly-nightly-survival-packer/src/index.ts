#!/usr/bin/env node

interface Item {
  name: string;
  weight: number;
  utility: number;
}

const ITEMS: Item[] = [
  { name: "Water Bottle", weight: 3, utility: 8 },
  { name: "Canned Food", weight: 2, utility: 6 },
  { name: "First Aid Kit", weight: 5, utility: 9 },
  { name: "Flashlight", weight: 1, utility: 4 },
  { name: "Radio", weight: 4, utility: 5 },
  { name: "Knife", weight: 2, utility: 7 },
  { name: "Blanket", weight: 6, utility: 5 },
  { name: "Map", weight: 1, utility: 3 },
];

export function packSurvivalKit(maxWeight: number): Item[] {
  const sorted = [...ITEMS].sort((a, b) => (b.utility / b.weight) - (a.utility / a.weight));
  const result: Item[] = [];
  let remaining = maxWeight;
  for (const item of sorted) {
    if (item.weight <= remaining) {
      result.push(item);
      remaining -= item.weight;
    }
  }
  return result;
}

// CLI handling
function parseArgs(): { maxWeight: number } {
  const args = process.argv.slice(2);
  let maxWeight = 10; // default
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--max-weight" && i + 1 < args.length) {
      const val = parseInt(args[i + 1], 10);
      if (!isNaN(val) && val > 0) {
        maxWeight = val;
      }
      i++;
    }
  }
  return { maxWeight };
}

if (require.main === module) {
  const { maxWeight } = parseArgs();
  const kit = packSurvivalKit(maxWeight);
  console.log(`Survival kit (max weight ${maxWeight}):`);
  for (const item of kit) {
    console.log(`- ${item.name} (weight ${item.weight}, utility ${item.utility})`);
  }
}

