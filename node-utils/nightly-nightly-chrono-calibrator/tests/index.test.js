const { getTrueUnixTime, getLocalUnixTime, calculateDrift, main, API_URL } = require('../src/index');
const fetch = require('node-fetch');
const chalk = require('chalk');

// Mock rationale: We need to control the external network request to worldtimeapi.org
// to ensure deterministic test results and avoid actual network calls.
jest.mock('node-fetch');

// Mock rationale: We need to capture console output to verify the script's messages
// without actually printing to the console during tests.
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

// Mock rationale: We need to control the system's current time to simulate different
// drift scenarios for deterministic testing.
const mockDateNow = jest.spyOn(Date, 'now');

describe('Nightly Chrono-Compass Calibrator', () => {
    beforeEach(() => {
        mockLog.mockClear();
        mockError.mockClear();
        fetch.mockClear();
        mockDateNow.mockClear();
        // Reset chalk level for each test to ensure consistent color output mocking
        chalk.level = 3; // Default to colored output for tests unless explicitly disabled
    });

    afterAll(() => {
        mockLog.mockRestore();
        mockError.mockRestore();
        mockDateNow.mockRestore();
    });

    describe('getTrueUnixTime', () => {
        test('should fetch true Unix time successfully', async () => {
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ unixtime: 1678886400 })
            });

            const trueTime = await getTrueUnixTime();
            expect(trueTime).toBe(1678886400);
            expect(fetch).toHaveBeenCalledWith(API_URL);
        });

        test('should handle API errors gracefully', async () => {
            fetch.mockResolvedValueOnce({
                ok: false,
                statusText: 'Service Unavailable',
                json: () => Promise.resolve({})
            });

            // Mock rationale: process.exit is called on error, which would terminate the test runner.
            // We mock it to prevent actual exit and check if it was called.
            const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

            await getTrueUnixTime();

            expect(mockError).toHaveBeenCalledWith(expect.stringContaining('🚨 Failed to contact Temporal Beacon Network: Temporal Beacon Network error: Service Unavailable'));
            expect(mockExit).toHaveBeenCalledWith(1);

            mockExit.mockRestore(); // Restore process.exit
        });
    });

    describe('getLocalUnixTime', () => {
        test('should return local Unix time', () => {
            mockDateNow.mockReturnValue(1678886405000);
            expect(getLocalUnixTime()).toBe(1678886405);
        });
    });

    describe('calculateDrift', () => {
        test('should calculate positive drift (local ahead)', () => {
            expect(calculateDrift(100, 105)).toBe(5);
        });

        test('should calculate negative drift (local behind)', () => {
            expect(calculateDrift(105, 100)).toBe(-5);
        });

        test('should calculate zero drift (aligned)', () => {
            expect(calculateDrift(100, 100)).toBe(0);
        });
    });

    describe('main', () => {
        test('should report perfect alignment', async () => {
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ unixtime: 1678886400 })
            });
            mockDateNow.mockReturnValue(1678886400000); // Local time matches true time

            await main();

            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.cyan('🌌 Initiating Chrono-Compass Calibration...')));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.green('✨ Your Chrono-Compass is perfectly aligned! No significant Temporal Drift Anomalies detected.')));
            expect(mockLog).not.toHaveBeenCalledWith(expect.stringContaining(chalk.red('⚠️ Temporal Drift Anomaly Detected!')));
        });

        test('should report positive drift (local ahead)', async () => {
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ unixtime: 1678886400 })
            });
            mockDateNow.mockReturnValue(1678886405000); // Local time is 5 seconds ahead

            await main();

            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.red('⚠️ Temporal Drift Anomaly Detected!')));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.red('Your Chrono-Compass is drifting by +5.000 seconds (ahead of true time).')));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.gray('To re-harmonize your Chrono-Compass, consider these actions:')));
        });

        test('should report negative drift (local behind)', async () => {
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ unixtime: 1678886400 })
            });
            mockDateNow.mockReturnValue(1678886395000); // Local time is 5 seconds behind

            await main();

            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.magenta('⚠️ Temporal Drift Anomaly Detected!')));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.magenta('Your Chrono-Compass is drifting by -5.000 seconds (behind true time).')));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining(chalk.gray('To re-harmonize your Chrono-Compass, consider these actions:')));
        });

        test('should disable color output with --no-color flag', async () => {
            // Mock rationale: yargs parses process.argv, so we need to simulate CLI arguments.
            // We temporarily modify process.argv for this test.
            const originalArgv = process.argv;
            process.argv = ['node', 'src/index.js', '--no-color'];

            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ unixtime: 1678886400 })
            });
            mockDateNow.mockReturnValue(1678886405000); // Local time is 5 seconds ahead

            await main();

            // Verify output contains the message but without color codes
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('⚠️ Temporal Drift Anomaly Detected!'));
            expect(mockLog).toHaveBeenCalledWith(expect.stringContaining('Your Chrono-Compass is drifting by +5.000 seconds (ahead of true time).'));

            process.argv = originalArgv; // Restore original argv
        });
    });
});
