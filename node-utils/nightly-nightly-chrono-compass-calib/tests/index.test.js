const chalk = require('chalk');
const { program, fetchTemporalAnchorTime } = require('../src/index'); // Import program and fetchTemporalAnchorTime

// Mock console.log to capture output
const mockLog = jest.spyOn(console, 'log').mockImplementation(() => {});

// Mock Date for deterministic tests
const MOCK_LOCAL_TIME = new Date('2023-10-27T10:00:00.000Z');
const MOCK_ANCHOR_TIME_AHEAD = new Date('2023-10-27T10:00:05.123Z');
const MOCK_ANCHOR_TIME_BEHIND = new Date('2023-10-27T09:59:55.456Z');
const MOCK_ANCHOR_TIME_SAME = new Date('2023-10-27T10:00:00.000Z');

// Mock Math.random for deterministic distortion
const mockMathRandom = jest.spyOn(Math, 'random');

describe('Nightly Chrono-Compass Calibrator', () => {
    let originalProcessArgv;
    const originalDate = global.Date;

    beforeEach(() => {
        mockLog.mockClear();
        mockMathRandom.mockClear();
        originalProcessArgv = process.argv;

        // Mock rationale: We need to control the current system time for deterministic tests.
        // By mocking Date.now, we ensure that `new Date()` inside the utility always starts from a known point.
        jest.spyOn(global, 'Date').mockImplementation((...args) => {
            if (args.length) {
                return new originalDate(...args);
            }
            return MOCK_LOCAL_TIME;
        });
        global.Date.now = jest.fn(() => MOCK_LOCAL_TIME.getTime());

        // Mock rationale: Simulate NTP server response without actual network calls.
        // This ensures tests are deterministic and offline.
        fetchTemporalAnchorTime.mockClear(); // Clear any previous mocks
    });

    afterEach(() => {
        process.argv = originalProcessArgv;
        jest.restoreAllMocks();
    });

    test('should calibrate time without distortion when no options are provided', async () => {
        fetchTemporalAnchorTime.mockResolvedValue(MOCK_ANCHOR_TIME_AHEAD);

        process.argv = ['node', 'src/index.js'];
        await program.parseAsync(process.argv);

        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Calibrating with Temporal Anchor: ') + chalk.cyan('https://apocalypsai.time.anchor'));
        expect(mockLog).toHaveBeenCalledWith(chalk.yellow('[Chrono-Compass] Local Time: ') + MOCK_LOCAL_TIME.toISOString());
        expect(mockLog).toHaveBeenCalledWith(chalk.green('[Chrono-Compass] Anchor Time: ') + MOCK_ANCHOR_TIME_AHEAD.toISOString());
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Time difference: ') + chalk.white('+5.123 seconds.'));
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Suggested command to synchronize:'));
        expect(mockLog).toHaveBeenCalledWith(chalk.gray('    sudo date -s "2023-10-27 10:00:05"'));
        expect(fetchTemporalAnchorTime).toHaveBeenCalledWith('https://apocalypsai.time.anchor');
    });

    test('should calibrate time with distortion when --distort is enabled', async () => {
        fetchTemporalAnchorTime.mockResolvedValue(MOCK_ANCHOR_TIME_AHEAD);
        mockMathRandom.mockReturnValueOnce(0.75); // Mock rationale: Control random distortion magnitude (0.75 * 10 - 5 = 2.5 seconds)

        process.argv = ['node', 'src/index.js', '--distort'];
        await program.parseAsync(process.argv);

        const expectedDistortion = (0.75 * 10 - 5); // 2.5 seconds
        const distortedAnchorTime = new Date(MOCK_ANCHOR_TIME_AHEAD.getTime() + expectedDistortion * 1000);
        const expectedTimeDifference = (distortedAnchorTime.getTime() - MOCK_LOCAL_TIME.getTime()) / 1000;

        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Calibrating with Temporal Anchor: ') + chalk.cyan('https://apocalypsai.time.anchor'));
        expect(mockLog).toHaveBeenCalledWith(chalk.yellow('[Chrono-Compass] Local Time: ') + MOCK_LOCAL_TIME.toISOString());
        expect(mockLog).toHaveBeenCalledWith(chalk.green('[Chrono-Compass] Anchor Time: ') + MOCK_ANCHOR_TIME_AHEAD.toISOString());
        expect(mockLog).toHaveBeenCalledWith(chalk.magenta(`[Chrono-Compass] Applying whimsical temporal distortion... (${expectedDistortion.toFixed(3)} seconds)`));
        expect(mockLog).toHaveBeenCalledWith(chalk.magenta('[Chrono-Compass] Effective Anchor Time: ') + distortedAnchorTime.toISOString());
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Time difference: ') + chalk.white(`${expectedTimeDifference.toFixed(3)} seconds.`));
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Suggested command to synchronize:'));
        expect(mockLog).toHaveBeenCalledWith(chalk.gray(`    sudo date -s "${distortedAnchorTime.getFullYear()}-${String(distortedAnchorTime.getMonth() + 1).padStart(2, '0')}-${String(distortedAnchorTime.getDate()).padStart(2, '0')} ${String(distortedAnchorTime.getHours()).padStart(2, '0')}:${String(distortedAnchorTime.getMinutes()).padStart(2, '0')}:${String(distortedAnchorTime.getSeconds()).padStart(2, '0')}"`));
        expect(fetchTemporalAnchorTime).toHaveBeenCalledWith('https://apocalypsai.time.anchor');
    });

    test('should handle anchor time being behind local time', async () => {
        fetchTemporalAnchorTime.mockResolvedValue(MOCK_ANCHOR_TIME_BEHIND);

        process.argv = ['node', 'src/index.js'];
        await program.parseAsync(process.argv);

        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Time difference: ') + chalk.white('-4.544 seconds.'));
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Suggested command to synchronize:'));
        expect(mockLog).toHaveBeenCalledWith(chalk.gray('    sudo date -s "2023-10-27 09:59:55"'));
    });

    test('should handle anchor time being the same as local time', async () => {
        fetchTemporalAnchorTime.mockResolvedValue(MOCK_ANCHOR_TIME_SAME);

        process.argv = ['node', 'src/index.js'];
        await program.parseAsync(process.argv);

        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Time difference: ') + chalk.white('0.000 seconds.'));
        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Suggested command to synchronize:'));
        expect(mockLog).toHaveBeenCalledWith(chalk.gray('    sudo date -s "2023-10-27 10:00:00"'));
    });

    test('should use custom server URL if provided', async () => {
        fetchTemporalAnchorTime.mockResolvedValue(MOCK_ANCHOR_TIME_AHEAD);

        const customServer = 'https://my.custom.time.server';
        process.argv = ['node', 'src/index.js', '--server', customServer];
        await program.parseAsync(process.argv);

        expect(mockLog).toHaveBeenCalledWith(chalk.blue('[Chrono-Compass] Calibrating with Temporal Anchor: ') + chalk.cyan(customServer));
        expect(fetchTemporalAnchorTime).toHaveBeenCalledWith(customServer);
    });
});
