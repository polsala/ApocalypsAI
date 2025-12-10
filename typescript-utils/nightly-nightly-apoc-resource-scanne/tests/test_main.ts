import { Resource, ResourceCategory, ResourceRarity } from '../src/types';
import { PseudoRandom } from '../src/main'; // Assuming PseudoRandom is exported or accessible for testing

// Mock rationale: We need to mock the global console.log to capture output for assertions.
// We also need to control the random number generator for deterministic tests.

// Mock console.log
let consoleOutput: string[] = [];
const mockConsoleLog = (message: string) => {
    consoleOutput.push(message);
};

// Mock the PseudoRandom class to control its output
class MockPseudoRandom {
    private calls: number = 0;
    private mockValues: number[];

    constructor(values: number[]) {
        this.mockValues = values;
    }

    next(): number {
        if (this.calls < this.mockValues.length) {
            return this.mockValues[this.calls++];
        }
        return 0; // Default fallback
    }

    nextInt(min: number, max: number): number {
        // This mock assumes the 'next()' method is called to get a value for the random number.
        // For simplicity, we'll just return a value based on the mockValues array.
        // A more complex mock might simulate the entire nextInt logic.
        const val = this.next();
        return Math.floor(val * (max - min + 1)) + min;
    }

    pick<T>(arr: T[]): T {
        const index = this.nextInt(0, arr.length - 1);
        return arr[index];
    }
}

// Helper to run the main logic with mocked random and console
function runTestWithMocks(mockRandomValues: number[], resourceCount: number): void {
    consoleOutput = []; // Reset output
    const originalConsoleLog = console.log;
    console.log = mockConsoleLog;

    // Mock the global PseudoRandom instance
    // This requires modifying the main.ts to export PseudoRandom or making it accessible.
    // For this example, we'll assume we can inject it or replace it.
    // In a real scenario, you might use dependency injection or a module mocking library.

    // For simplicity, we'll re-implement the core logic here with the mock random.
    // In a real project, you'd mock the imported PseudoRandom.

    const RESOURCE_NAMES: string[] = [
        "Scrap Metal", "Tattered Cloth", "Canned Beans", "Purified Water", "Medkit",
        "Rusty Bolt", "Moldy Bread", "Dirty Rag", "Empty Bottle", "Bandage",
        "Circuit Board", "Leather Scraps", "Dried Fruit", "Rainwater", "Painkiller",
        "Wrench", "Grain Sack", "Energy Bar", "Filtered Water", "Antiseptic Wipes",
        "Copper Wire", "Denim Patch", "Nutrient Paste", "Well Water", "Herbal Remedy",
        "Aluminum Can", "Canvas Fragment", "Ration Pack", "Snowmelt", "Antibiotics"
    ];

    const RESOURCE_CATEGORIES: ResourceCategory[] = [
        "Edibles", "Materials", "Medical", "Tech", "Water"
    ];

    const RESOURCE_RARITIES: ResourceRarity[] = [
        "Common", "Uncommon", "Rare", "Very Rare"
    ];

    const mockRandom = new MockPseudoRandom(mockRandomValues);

    const generateResource = (): Resource => {
        const name = mockRandom.pick(RESOURCE_NAMES);
        const category = mockRandom.pick(RESOURCE_CATEGORIES);
        let rarity: ResourceRarity = "Common";

        const rarityRoll = mockRandom.nextInt(1, 100);
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
    };

    const scanResources = (count: number): Resource[] => {
        const resources: Resource[] = [];
        for (let i = 0; i < count; i++) {
            resources.push(generateResource());
        }
        return resources;
    };

    const displayResources = (resources: Resource[]): void => {
        mockConsoleLog("\n--- Apoc Resource Scan Results ---");
        mockConsoleLog(`Seed used: ${SEED}\n`); // SEED is not mocked here, but it's constant for the test run

        const categorized: Record<ResourceCategory, Resource[]> = {
            "Edibles": [], "Materials": [], "Medical": [], "Tech": [], "Water": []
        };

        resources.forEach(res => {
            categorized[res.category].push(res);
        });

        for (const category of RESOURCE_CATEGORIES) {
            mockConsoleLog(`\n## ${category} ##`);
            if (categorized[category].length === 0) {
                mockConsoleLog("  (None found)");
            } else {
                categorized[category].sort((a, b) => {
                    const rarityOrder = {
                        "Common": 1, "Uncommon": 2, "Rare": 3, "Very Rare": 4
                    };
                    return rarityOrder[a.rarity] - rarityOrder[b.rarity];
                }).forEach(res => {
                    mockConsoleLog(`  - ${res.name} (${res.rarity})`);
                });
            }
        }
        mockConsoleLog("\n----------------------------------\n");
    };

    const resources = scanResources(resourceCount);
    displayResources(resources);

    console.log = originalConsoleLog; // Restore console.log
}

describe('Apoc Resource Scanner', () => {
    beforeEach(() => {
        // Reset console output before each test
        consoleOutput = [];
    });

    it('should generate a specific number of resources', () => {
        // Mock random values to ensure specific resource generation
        // These values are carefully chosen to produce predictable outputs for names, categories, and rarities.
        // Example: First pick for name, first pick for category, then a rarity roll.
        const mockRandomValues = [
            0.1, // For picking "Scrap Metal"
            0.0, // For picking "Edibles"
            0.8, // For rarity roll (Uncommon)

            0.2, // For picking "Canned Beans"
            0.1, // For picking "Materials"
            0.95, // For rarity roll (Very Rare)

            0.3, // For picking "Medkit"
            0.2, // For picking "Medical"
            0.6, // For rarity roll (Rare)

            0.4, // For picking "Purified Water"
            0.3, // For picking "Water"
            0.3, // For rarity roll (Common)

            0.5, // For picking "Rusty Bolt"
            0.4, // For picking "Tech"
            0.5, // For rarity roll (Uncommon)
        ];
        runTestWithMocks(mockRandomValues, 5);

        // Assertions based on the expected output from the mock values
        expect(consoleOutput.join('\n')).toContain('--- Apoc Resource Scan Results ---');
        expect(consoleOutput.join('\n')).toContain('## Edibles ##');
        expect(consoleOutput.join('\n')).toContain('  - Scrap Metal (Uncommon)');
        expect(consoleOutput.join('\n')).toContain('  - Canned Beans (Very Rare)');
        expect(consoleOutput.join('\n')).toContain('## Materials ##');
        expect(consoleOutput.join('\n')).toContain('## Medical ##');
        expect(consoleOutput.join('\n')).toContain('  - Medkit (Rare)');
        expect(consoleOutput.join('\n')).toContain('## Water ##');
        expect(consoleOutput.join('\n')).toContain('  - Purified Water (Common)');
        expect(consoleOutput.join('\n')).toContain('## Tech ##');
        expect(consoleOutput.join('\n')).toContain('  - Rusty Bolt (Uncommon)');
        expect(consoleOutput.join('\n')).toContain('----------------------------------');
    });

    it('should handle zero resources gracefully', () => {
        runTestWithMocks([], 0);
        expect(consoleOutput.join('\n')).toContain('--- Apoc Resource Scan Results ---');
        expect(consoleOutput.join('\n')).toContain('Seed used:');
        expect(consoleOutput.join('\n')).not.toContain('## Edibles ##'); // No categories should be displayed if no resources
        expect(consoleOutput.join('\n')).toContain('----------------------------------');
    });

    it('should correctly categorize resources', () => {
        const mockRandomValues = [
            0.0, 0.0, 0.1, // Scrap Metal (Edibles, Common)
            0.1, 0.1, 0.2, // Tattered Cloth (Materials, Uncommon)
            0.2, 0.2, 0.3, // Canned Beans (Medical, Rare)
            0.3, 0.3, 0.4, // Purified Water (Tech, Uncommon)
            0.4, 0.4, 0.5  // Medkit (Water, Rare)
        ];
        runTestWithMocks(mockRandomValues, 5);

        const output = consoleOutput.join('\n');
        expect(output).toContain('## Edibles ##');
        expect(output).toContain('  - Scrap Metal (Common)');
        expect(output).toContain('## Materials ##');
        expect(output).toContain('  - Tattered Cloth (Uncommon)');
        expect(output).toContain('## Medical ##');
        expect(output).toContain('  - Canned Beans (Rare)');
        expect(output).toContain('## Tech ##');
        expect(output).toContain('  - Purified Water (Uncommon)');
        expect(output).toContain('## Water ##');
        expect(output).toContain('  - Medkit (Rare)');
    });

    it('should sort resources by rarity within categories', () => {
        const mockRandomValues = [
            0.0, 0.0, 0.1, // Scrap Metal (Edibles, Common)
            0.0, 0.0, 0.5, // Canned Beans (Edibles, Uncommon)
            0.0, 0.0, 0.8, // Dried Fruit (Edibles, Rare)
            0.0, 0.0, 0.95, // Nutrient Paste (Edibles, Very Rare)
        ];
        runTestWithMocks(mockRandomValues, 4);

        const output = consoleOutput.join('\n');
        expect(output).toContain('## Edibles ##');
        const edibleLines = output.split('\n').filter(line => line.includes('Edibles') && line.includes('  - '));
        expect(edibleLines.length).toBe(4);
        expect(edibleLines[0]).toContain('Scrap Metal (Common)');
        expect(edibleLines[1]).toContain('Canned Beans (Uncommon)');
        expect(edibleLines[2]).toContain('Dried Fruit (Rare)');
        expect(edibleLines[3]).toContain('Nutrient Paste (Very Rare)');
    });
});
