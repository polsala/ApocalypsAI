const assert = require('assert');
const { generateCosmicCompass, displayCompass } = require('../src/index.js');

// Mocking Math.random to ensure deterministic tests
let mockRandomSeed = 0;
const originalMathRandom = Math.random;

function mockMathRandom() {
    // A simple pseudo-random sequence for deterministic testing
    const x = Math.sin(mockRandomSeed++) * 10000;
    return x - Math.floor(x);
}

describe('Cosmic Compass', () => {

    beforeEach(() => {
        // Reset seed and replace Math.random before each test
        mockRandomSeed = 0;
        Math.random = mockMathRandom;
    });

    afterEach(() => {
        // Restore original Math.random after each test
        Math.random = originalMathRandom;
    });

    it('should generate a star system with a name, coordinates, and type', () => {
        const compassData = generateCosmicCompass();

        // Mock rationale: The first call to Math.random (seed 0) should produce a specific value.
        // Based on the mockMathRandom function, this value is approximately 0.5403023058681398.
        // This value is used to derive the expected star name and coordinates.
        // The exact derivation of star names/types from this seed is complex due to array indexing,
        // so we focus on the structure and range of the output.

        assert.ok(compassData.starName, 'Star name should be present');
        assert.ok(compassData.galacticCoordinates, 'Galactic coordinates should be present');
        assert.ok(compassData.galacticCoordinates.X !== undefined, 'Coordinate X should be present');
        assert.ok(compassData.galacticCoordinates.Y !== undefined, 'Coordinate Y should be present');
        assert.ok(compassData.galacticCoordinates.Z !== undefined, 'Coordinate Z should be present');
        assert.ok(compassData.starType, 'Star type should be present');

        // Check if coordinates are within a reasonable range (approx -1000 to 1000)
        assert.ok(compassData.galacticCoordinates.X >= -1000 && compassData.galacticCoordinates.X <= 1000, 'Coordinate X out of range');
        assert.ok(compassData.galacticCoordinates.Y >= -1000 && compassData.galacticCoordinates.Y <= 1000, 'Coordinate Y out of range');
        assert.ok(compassData.galacticCoordinates.Z >= -1000 && compassData.galacticCoordinates.Z <= 1000, 'Coordinate Z out of range');
    });

    it('should generate deterministic output with mocked Math.random', () => {
        // Mock rationale: By controlling Math.random, we ensure that subsequent calls to generateCosmicCompass
        // produce the exact same output, making the tests repeatable.
        const compassData1 = generateCosmicCompass();
        const compassData2 = generateCosmicCompass();

        // The second call to generateCosmicCompass should produce the same result as the first
        // because the mock seed is reset in beforeEach and the sequence is deterministic.
        // However, since we are calling it twice *within* this test, the seed will increment.
        // We need to call it again to get the *same* result as the first call.
        mockRandomSeed = 0; // Reset seed to ensure we get the *exact* same sequence as the first call
        Math.random = mockMathRandom;
        const compassData3 = generateCosmicCompass();

        assert.deepStrictEqual(compassData1, compassData3, 'Output should be deterministic');
    });

    it('should display compass data correctly', () => {
        const mockCompassData = {
            starName: "Test Nebula",
            galacticCoordinates: {
                X: 123.45,
                Y: -67.89,
                Z: 98.76
            },
            starType: "Supernova Remnant"
        };

        // Mock rationale: We capture console.log output to verify that displayCompass formats the data as expected.
        const originalConsoleLog = console.log;
        let consoleOutput = [];
        console.log = (message) => {
            consoleOutput.push(message);
        };

        displayCompass(mockCompassData);

        // Restore console.log
        console.log = originalConsoleLog;

        assert.strictEqual(consoleOutput.length, 3, 'Should have 3 lines of output');
        assert.strictEqual(consoleOutput[0], 'Star System: Test Nebula', 'First line incorrect');
        assert.strictEqual(consoleOutput[1], 'Galactic Coordinates: X: 123.45, Y: -67.89, Z: 98.76', 'Second line incorrect');
        assert.strictEqual(consoleOutput[2], 'Star Type: Supernova Remnant', 'Third line incorrect');
    });

});
