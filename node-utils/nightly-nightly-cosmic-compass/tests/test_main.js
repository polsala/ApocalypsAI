const moment = require('moment');
const { jest } = require('@jest/globals');

// Mock the moment module to control time
jest.mock('moment', () => {
    const originalMoment = jest.requireActual('moment');
    return (timestamp) => {
        if (timestamp) {
            return originalMoment(timestamp);
        } else {
            // Mock a specific fixed time for deterministic tests
            return originalMoment('2023-10-27T10:30:00.000Z');
        }
    };
});

// Mock the SeededRandom class to ensure deterministic output
class MockSeededRandom {
    constructor(seed) {
        this.calls = 0;
        // Predefined sequence of random numbers for predictable results
        this.sequence = [
            0.5, // For RA
            0.25, // For Dec
            0.75, // For Epoch index
            0.1,  // For Constellation index
            0.9,  // Another RA
            0.6,  // Another Dec
            0.3,  // Another Epoch index
            0.8   // Another Constellation index
        ];
    }

    next() {
        const value = this.sequence[this.calls % this.sequence.length];
        this.calls++;
        return value;
    }
}

// Replace the actual SeededRandom with our mock
const originalSeededRandom = require('../src/main.js').SeededRandom;
jest.mock('../src/main.js', () => {
    const actualModule = jest.requireActual('../src/main.js');
    return {
        ...actualModule,
        SeededRandom: MockSeededRandom
    };
});


// Re-require the main module after mocking
const { generateCosmicCoordinates } = require('../src/main.js');

describe('Cosmic Compass', () => {
    // Mock rationale: We are mocking moment to ensure that the timestamp used to seed the random number generator is always the same, making the output deterministic. This is crucial for reliable testing.
    // Mock rationale: We are mocking the SeededRandom class to provide a fixed sequence of 'random' numbers. This ensures that the generated coordinates are predictable and consistent across test runs, allowing us to assert specific outputs.

    test('should generate deterministic cosmic coordinates for a fixed time', () => {
        const expectedOutput = {
            RA: "12h 0m 0.0s",
            Dec: "+22° 30' 0.0\"",
            Epoch: "Galactic Twilight",
            Constellation: "The Lunar Moth"
        };
        expect(generateCosmicCoordinates()).toEqual(expectedOutput);
    });

    test('should generate different coordinates with a different mock sequence', () => {
        // Temporarily override the mock sequence for a second test case
        const originalSequence = MockSeededRandom.prototype.sequence;
        MockSeededRandom.prototype.sequence = [
            0.9, // RA
            0.1, // Dec
            0.2, // Epoch index
            0.5, // Constellation index
        ];

        const expectedOutput = {
            RA: "21h 36m 0.0s",
            Dec: "-78° 0' 0.0\"",
            Epoch: "Nebula Dawn",
            Constellation: "The Starfall Bloom"
        };
        expect(generateCosmicCoordinates()).toEqual(expectedOutput);

        // Restore the original sequence
        MockSeededRandom.prototype.sequence = originalSequence;
    });
});
