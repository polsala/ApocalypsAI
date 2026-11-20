const { run, _parseOffset, _getExternalTime, _getLocalTime } = require('../src/index');

// Mock console.log to capture output
let consoleOutput = [];
const originalConsoleLog = console.log;
const originalConsoleError = console.error;
const mockConsoleLog = (message) => consoleOutput.push(message);
const mockConsoleError = (message) => consoleOutput.push(message);

beforeEach(() => {
    consoleOutput = [];
    console.log = mockConsoleLog;
    console.error = mockConsoleError;
});

afterEach(() => {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
});

describe('parseOffset', () => {
    test('should parse positive seconds', () => {
        expect(_parseOffset('+5s')).toBe(5 * 1000);
    });

    test('should parse negative minutes', () => {
        expect(_parseOffset('-10m')).toBe(-10 * 60 * 1000);
    });

    test('should parse positive hours', () => {
        expect(_parseOffset('+1h')).toBe(1 * 60 * 60 * 1000);
    });

    test('should return 0 for no offset string', () => {
        expect(_parseOffset(undefined)).toBe(0);
        expect(_parseOffset(null)).toBe(0);
        expect(_parseOffset('')).toBe(0);
    });

    test('should exit with error for invalid format', () => {
        const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
        _parseOffset('invalid');
        expect(consoleOutput[0]).toContain("Invalid offset format");
        expect(mockExit).toHaveBeenCalledWith(1);
        mockExit.mockRestore();
    });
});

describe('run', () => {
    const externalTimeMs = new Date('2024-07-20T12:00:00.000Z').getTime();
    const localTimeMs = new Date('2024-07-20T11:59:50.000Z').getTime(); // 10 seconds behind

    test('should report time difference and suggest sync without offset', () => {
        // # Mock rationale: Control the "external" and "local" times for predictable test results.
        // # This simulates a scenario where the external source is at 12:00:00 and local is 11:59:50.
        const mockGetExternalTime = jest.spyOn(require('../src/index'), '_getExternalTime').mockReturnValue(externalTimeMs);
        const mockGetLocalTime = jest.spyOn(require('../src/index'), '_getLocalTime').mockReturnValue(localTimeMs);

        run([]); // No arguments

        expect(consoleOutput.join('\n')).toContain('External Time Signal: 2024-07-20T12:00:00.000Z');
        expect(consoleOutput.join('\n')).toContain('Local System Time:    2024-07-20T11:59:50.000Z');
        expect(consoleOutput.join('\n')).toContain('Calculated Synchronized Time: 2024-07-20T12:00:00Z');
        expect(consoleOutput.join('\n')).toContain('Time Difference (Local vs. Synced): 10 seconds');
        expect(consoleOutput.join('\n')).toContain('Recommendation: Your local time is significantly off.');
        expect(consoleOutput.join('\n')).toContain('sudo date -s "2024-07-20T12:00:00Z"');

        mockGetExternalTime.mockRestore();
        mockGetLocalTime.mockRestore();
    });

    test('should report time difference and suggest sync with positive offset', () => {
        // # Mock rationale: Simulate a "temporal distortion" where the external time needs a +5s adjustment.
        // # External: 12:00:00, Local: 11:59:50. Synced time becomes 12:00:05.
        const mockGetExternalTime = jest.spyOn(require('../src/index'), '_getExternalTime').mockReturnValue(externalTimeMs);
        const mockGetLocalTime = jest.spyOn(require('../src/index'), '_getLocalTime').mockReturnValue(localTimeMs);

        run(['node', 'src/index.js', '--offset', '+5s']);

        expect(consoleOutput.join('\n')).toContain('External Time Signal: 2024-07-20T12:00:00.000Z');
        expect(consoleOutput.join('\n')).toContain('Local System Time:    2024-07-20T11:59:50.000Z');
        expect(consoleOutput.join('\n')).toContain('Temporal Distortion Applied: 5 seconds');
        expect(consoleOutput.join('\n')).toContain('Calculated Synchronized Time: 2024-07-20T12:00:05Z');
        expect(consoleOutput.join('\n')).toContain('Time Difference (Local vs. Synced): 15 seconds');
        expect(consoleOutput.join('\n')).toContain('sudo date -s "2024-07-20T12:00:05Z"');

        mockGetExternalTime.mockRestore();
        mockGetLocalTime.mockRestore();
    });

    test('should report time difference and suggest sync with negative offset', () => {
        // # Mock rationale: Simulate a "temporal distortion" where the external time needs a -5s adjustment.
        // # External: 12:00:00, Local: 11:59:50. Synced time becomes 11:59:55.
        const mockGetExternalTime = jest.spyOn(require('../src/index'), '_getExternalTime').mockReturnValue(externalTimeMs);
        const mockGetLocalTime = jest.spyOn(require('../src/index'), '_getLocalTime').mockReturnValue(localTimeMs);

        run(['node', 'src/index.js', '--offset', '-5s']);

        expect(consoleOutput.join('\n')).toContain('External Time Signal: 2024-07-20T12:00:00.000Z');
        expect(consoleOutput.join('\n')).toContain('Local System Time:    2024-07-20T11:59:50.000Z');
        expect(consoleOutput.join('\n')).toContain('Temporal Distortion Applied: -5 seconds');
        expect(consoleOutput.join('\n')).toContain('Calculated Synchronized Time: 2024-07-20T11:59:55Z');
        expect(consoleOutput.join('\n')).toContain('Time Difference (Local vs. Synced): 5 seconds');
        expect(consoleOutput.join('\n')).toContain('sudo date -s "2024-07-20T11:59:55Z"');

        mockGetExternalTime.mockRestore();
        mockGetLocalTime.mockRestore();
    });

    test('should report time is synchronized if difference is small', () => {
        // # Mock rationale: Simulate a scenario where local time is very close to external time.
        // # External: 12:00:00, Local: 11:59:59.500 (500ms difference)
        const mockGetExternalTime = jest.spyOn(require('../src/index'), '_getExternalTime').mockReturnValue(externalTimeMs);
        const mockGetLocalTime = jest.spyOn(require('../src/index'), '_getLocalTime').mockReturnValue(externalTimeMs - 500); // 500ms behind

        run([]);

        expect(consoleOutput.join('\n')).toContain('Time Difference (Local vs. Synced): 0.5 seconds');
        expect(consoleOutput.join('\n')).toContain('Recommendation: Your local time is within acceptable synchronization limits.');
        expect(consoleOutput.join('\n')).not.toContain('sudo date -s');

        mockGetExternalTime.mockRestore();
        mockGetLocalTime.mockRestore();
    });

    test('should handle invalid offset gracefully and exit', () => {
        const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
        run(['node', 'src/index.js', '--offset', 'bad_format']);
        expect(consoleOutput.join('\n')).toContain("Invalid offset format");
        expect(mockExit).toHaveBeenCalledWith(1);
        mockExit.mockRestore();
    });
});
