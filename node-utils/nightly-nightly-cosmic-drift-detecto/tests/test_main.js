const { calculateStats, generateCosmicReading, cosmicAlerts } = require('../src/main'); // Assuming main.js exports these for testing

// Mocking console.log to capture output for assertions
let consoleOutput = [];
const originalConsoleLog = console.log;
console.log = (...args) => {
    consoleOutput.push(args.join(' '));
};

// Mocking setTimeout to prevent actual delays in tests
const originalSetTimeout = global.setTimeout;
global.setTimeout = (callback, delay) => {
    callback(); // Execute immediately
};

// Mocking process.argv to control command line arguments
const originalProcessArgv = process.argv;

// Helper to reset mocks and clear output
function resetMocks() {
    consoleOutput = [];
    process.argv = originalProcessArgv;
    global.setTimeout = originalSetTimeout;
}

describe('Cosmic Drift Detector Tests', () => {

    beforeEach(() => {
        resetMocks();
        // Re-require main.js to ensure mocks are applied correctly if it was already run
        jest.resetModules();
        require('../src/main');
    });

    afterEach(() => {
        resetMocks();
    });

    describe('calculateStats', () => {
        test('should return 0 for empty array', () => {
            const stats = calculateStats([]);
            expect(stats.mean).toBe(0);
            expect(stats.stdDev).toBe(0);
        });

        test('should calculate mean and stdDev correctly for a simple array', () => {
            const data = [1, 2, 3, 4, 5];
            const stats = calculateStats(data);
            expect(stats.mean).toBe(3);
            // Mock rationale: Using a known standard deviation calculation for a simple dataset.
            // For [1, 2, 3, 4, 5], variance is ((1-3)^2 + (2-3)^2 + (3-3)^2 + (4-3)^2 + (5-3)^2) / 5 = (4+1+0+1+4)/5 = 10/5 = 2.
            // StdDev is sqrt(2) which is approx 1.41421356.
            expect(stats.stdDev).toBeCloseTo(Math.sqrt(2));
        });

        test('should handle arrays with negative numbers', () => {
            const data = [-1, 0, 1];
            const stats = calculateStats(data);
            expect(stats.mean).toBe(0);
            // Mock rationale: For [-1, 0, 1], variance is ((-1-0)^2 + (0-0)^2 + (1-0)^2) / 3 = (1+0+1)/3 = 2/3.
            // StdDev is sqrt(2/3) which is approx 0.81649658.
            expect(stats.stdDev).toBeCloseTo(Math.sqrt(2/3));
        });
    });

    describe('generateCosmicReading', () => {
        test('should generate numbers within a reasonable range around the mean', () => {
            const mean = 50;
            const stdDev = 5;
            for (let i = 0; i < 100; i++) {
                const reading = generateCosmicReading(mean, stdDev);
                // Mock rationale: Expect readings to be within a few standard deviations of the mean.
                // This is a probabilistic test, so we allow a wide range.
                expect(reading).toBeGreaterThan(mean - 5 * stdDev);
                expect(reading).toBeLessThan(mean + 5 * stdDev);
            }
        });
    });

    describe('anomaly detection logic', () => {
        test('should not flag readings close to the mean', async () => {
            // Mock the generateCosmicReading to return values very close to the mean
            const mockGenerate = jest.spyOn(require('../src/main'), 'generateCosmicReading');
            mockGenerate.mockReturnValue(100);

            // Mock the calculateStats to return a stable mean and stdDev
            const mockCalculateStats = jest.spyOn(require('../src/main'), 'calculateStats');
            mockCalculateStats.mockReturnValue({ mean: 100, stdDev: 5 });

            // Set anomaly threshold to a high value to ensure no flags
            process.argv = ['node', 'src/main.js', '--streamSize=10', '--anomalyThreshold=10'];
            const runModule = require('../src/main');
            await runModule.runCosmicDriftDetector(10, 10);

            expect(consoleOutput.some(line => line.includes('COSMIC ANOMALY DETECTED'))).toBe(false);
            mockGenerate.mockRestore();
            mockCalculateStats.mockRestore();
        });

        test('should flag readings far from the mean', async () => {
            // Mock generateCosmicReading to return a value significantly outside the expected range
            const mockGenerate = jest.spyOn(require('../src/main'), 'generateCosmicReading');
            mockGenerate.mockImplementation((mean, stdDev) => mean + 5 * stdDev); // Always return a high anomaly

            // Mock calculateStats to return a stable mean and stdDev
            const mockCalculateStats = jest.spyOn(require('../src/main'), 'calculateStats');
            mockCalculateStats.mockReturnValue({ mean: 100, stdDev: 5 });

            // Set anomaly threshold to a low value to ensure flags
            process.argv = ['node', 'src/main.js', '--streamSize=5', '--anomalyThreshold=2'];
            const runModule = require('../src/main');
            await runModule.runCosmicDriftDetector(5, 2);

            expect(consoleOutput.some(line => line.includes('COSMIC ANOMALY DETECTED'))).toBe(true);
            mockGenerate.mockRestore();
            mockCalculateStats.mockRestore();
        });

        test('should use default parameters if none are provided', async () => {
            // Mock the runCosmicDriftDetector to capture its arguments
            const mockRunDetector = jest.spyOn(require('../src/main'), 'runCosmicDriftDetector');
            mockRunDetector.mockImplementation(() => Promise.resolve()); // Do nothing, just capture args

            process.argv = ['node', 'src/main.js']; // No arguments
            require('../src/main'); // This will trigger the parsing and call runCosmicDriftDetector

            // Mock rationale: Verify that the default values (500 for streamSize, 2 for anomalyThreshold) are used.
            expect(mockRunDetector).toHaveBeenCalledWith(500, 2);
            mockRunDetector.mockRestore();
        });

        test('should use provided parameters', async () => {
            const mockRunDetector = jest.spyOn(require('../src/main'), 'runCosmicDriftDetector');
            mockRunDetector.mockImplementation(() => Promise.resolve());

            process.argv = ['node', 'src/main.js', '--streamSize=200', '--anomalyThreshold=3.5'];
            require('../src/main');

            // Mock rationale: Verify that the provided command-line arguments are correctly parsed and passed.
            expect(mockRunDetector).toHaveBeenCalledWith(200, 3.5);
            mockRunDetector.mockRestore();
        });
    });

    describe('cosmicAlerts', () => {
        test('should contain a list of whimsical alerts', () => {
            expect(cosmicAlerts).toBeInstanceOf(Array);
            expect(cosmicAlerts.length).toBeGreaterThan(0);
            cosmicAlerts.forEach(alert => {
                expect(alert).toBeA('string');
                expect(alert.length).toBeGreaterThan(10); // Ensure alerts are substantial
            });
        });
    });
});

// Mocking helper functions that are not directly exported but used internally
// This is necessary because Jest might not pick up internal mocks if the module is required multiple times
// or if the mocks are not set up before the module is first imported.
// We'll re-define them here to ensure they are available for jest.spyOn.
function calculateStats(data) {
    const n = data.length;
    if (n === 0) {
        return { mean: 0, stdDev: 0 };
    }
    const mean = data.reduce((sum, value) => sum + value, 0) / n;
    const variance = data.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / n;
    const stdDev = Math.sqrt(variance);
    return { mean, stdDev };
}

function generateCosmicReading(mean = 100, stdDev = 10) {
    const u1 = Math.random();
    const u2 = Math.random();
    const randStdNormal = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);
    return mean + stdDev * randStdNormal;
}

const cosmicAlerts = [
    "A rogue nebula just zipped through the data stream! Prepare for unexpected stardust!",
    "The cosmic background radiation is acting a bit quirky today. Keep an eye out!",
    "Did a black hole just swallow a data packet? Readings are... unusual.",
    "A passing comet has left a trail of anomalous readings. Fascinating!",
    "The universe is humming a different tune! Anomaly detected.",
    "Looks like a wormhole opened up and warped some data points. Intriguing!"
];

// Exporting these for jest.spyOn to work correctly
module.exports = { calculateStats, generateCosmicReading, cosmicAlerts };
