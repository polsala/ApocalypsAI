import { Resource, ResourceCategory, ResourceRarity } from './types';

// Mock rationale: Using a fixed seed for deterministic random generation during testing and for predictable output.
const SEED = process.argv.includes('--seed') ? parseInt(process.argv[process.argv.indexOf('--seed') + 1], 10) : Date.now();

// Simple pseudo-random number generator for deterministic results
class PseudoRandom {
    private seed: number;

    constructor(seed: number) {
        this.seed = seed;
    }

    next(): number {
        this.seed = (this.seed * 9301 + 49297) % 233280;
        return this.seed / 233280;
    }

    nextInt(min: number, max: number): number {
        return Math.floor(this.next() * (max - min + 1)) + min;
    }

    pick<T>(arr: T[]): T {
        return arr[this.nextInt(0, arr.length - 1)];
    }
}

const random = new PseudoRandom(SEED);

const RESOURCE_NAMES: string[] = [
    "Scrap Metal", "Tattered Cloth", "Canned Beans", "Purified Water", "Medkit",
    "Rusty Bolt", "Moldy Bread", "Dirty Rag", "Empty Bottle", "Bandage",
    "Circuit Board", "Leather Scraps", "Dried Fruit", "Rainwater", "Painkiller",
    "Wrench", "Grain Sack", "Energy Bar", "Filtered Water", "Antiseptic Wipes",
    "Copper Wire", "Denim Patch", "Nutrient Paste", "Well Water", "Herbal Remedy",
    "Aluminum Can", "Canvas Fragment", "Ration Pack", "Spring Water", "Splint Kit",
    "Steel Plate", "Wool Scarf", "Dehydrated Meal", "Snowmelt", "Antibiotics"
];

const RESOURCE_CATEGORIES: ResourceCategory[] = [
    "Edibles", "Materials", "Medical", "Tech", "Water"
];

const RESOURCE_RARITIES: ResourceRarity[] = [
    "Common", "Uncommon", "Rare", "Very Rare"
];

function generateResource(): Resource {
    const name = random.pick(RESOURCE_NAMES);
    const category = random.pick(RESOURCE_CATEGORIES);
    let rarity: ResourceRarity = "Common";

    const rarityRoll = random.nextInt(1, 100);
    if (rarityRoll > 90) {
        rarity = "Very Rare";
    } else if (rarityRoll > 70) {
        rarity = "Rare";
    } else if (rarityRoll > 40) {
        rarity = "Uncommon";
    }

    return {
        name,
        category,
        rarity,
        discoveredAt: new Date().toISOString()
    };
}

function scanResources(count: number): Resource[] {
    const resources: Resource[] = [];
    for (let i = 0; i < count; i++) {
        resources.push(generateResource());
    }
    return resources;
}

function displayResources(resources: Resource[]): void {
    console.log("\n--- Apoc Resource Scan Results ---");
    console.log(`Seed used: ${SEED}\n`);

    const categorized: Record<ResourceCategory, Resource[]> = {
        "Edibles": [], "Materials": [], "Medical": [], "Tech": [], "Water": []
    };

    resources.forEach(res => {
        categorized[res.category].push(res);
    });

    for (const category of RESOURCE_CATEGORIES) {
        console.log(`\n## ${category} ##`);
        if (categorized[category].length === 0) {
            console.log("  (None found)");
        } else {
            categorized[category].sort((a, b) => {
                const rarityOrder = {
                    "Common": 1, "Uncommon": 2, "Rare": 3, "Very Rare": 4
                };
                return rarityOrder[a.rarity] - rarityOrder[b.rarity];
            }).forEach(res => {
                console.log(`  - ${res.name} (${res.rarity})`);
            });
        }
    }
    console.log("\n----------------------------------\n");
}

function main() {
    const args = process.argv.slice(2);
    let resourceCount = 10;

    const countIndex = args.indexOf('--count');
    if (countIndex !== -1 && args[countIndex + 1]) {
        resourceCount = parseInt(args[countIndex + 1], 10);
        if (isNaN(resourceCount) || resourceCount <= 0) {
            console.error("Invalid count value. Please provide a positive number.");
            process.exit(1);
        }
    }

    const resources = scanResources(resourceCount);
    displayResources(resources);
}

main();
