const { run, _private } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to control file system operations to ensure tests are deterministic
// and do not affect the actual file system. This allows us to simulate different states
// of the plant.json file without side effects.
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
}));

describe('Nightly Desk Plant Pal', () => {
    let consoleSpy;
    let mockDate;

    beforeEach(() => {
        consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        // Mock rationale: Fix the current date for deterministic testing of 'days since' calculations.
        mockDate = new Date('2023-10-26T10:00:00.000Z');
        jest.useFakeTimers().setSystemTime(mockDate);

        // Reset mocks before each test
        fs.existsSync.mockClear();
        fs.readFileSync.mockClear();
        fs.writeFileSync.mockClear();
    });

    afterEach(() => {
        consoleSpy.mockRestore();
        jest.useRealTimers();
    });

    // Helper to simulate command line arguments
    const setArgs = (args) => {
        process.argv = ['node', 'src/index.js', ...args];
    };

    describe('init command', () => {
        test('should initialize a new plant if none exists', () => {
            fs.existsSync.mockReturnValue(false); // No plant file exists
            setArgs(['init', 'Fernie', '4']);
            run();

            expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
            expect(fs.writeFileSync).toHaveBeenCalledWith(_private.PLANT_FILE, expect.any(String));
            const writtenData = JSON.parse(fs.writeFileSync.mock.calls[0][0]);
            expect(writtenData.name).toBe('Fernie');
            expect(writtenData.wateringFrequency).toBe(4);
            expect(writtenData.lastWatered).toBe('2023-10-26');
            expect(consoleSpy).toHaveBeenCalledWith('🌿 Welcome Fernie, your new desk plant pal!');
            expect(consoleSpy).toHaveBeenCalledWith('Remember to water it every 4 days.');
        });

        test('should use default name and frequency if not provided', () => {
            fs.existsSync.mockReturnValue(false);
            setArgs(['init']);
            run();

            const writtenData = JSON.parse(fs.writeFileSync.mock.calls[0][0]);
            expect(writtenData.name).toBe('Leafy');
            expect(writtenData.wateringFrequency).toBe(3);
        });

        test('should not initialize if a plant already exists', () => {
            fs.existsSync.mockReturnValue(true);
            fs.readFileSync.mockReturnValue(JSON.stringify({ name: 'OldPlant' })); // Mock existing plant
            setArgs(['init', 'NewPlant']);
            run();

            expect(fs.writeFileSync).not.toHaveBeenCalled();
            expect(consoleSpy).toHaveBeenCalledWith('You already have a plant! Use "check" or "water".');
        });
    });

    describe('check command', () => {
        test('should report no plant if file does not exist', () => {
            fs.existsSync.mockReturnValue(false);
            setArgs(['check']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('No plant found. Use "init <name> [frequency]" to get one!');
        });

        test('should report happy plant if recently watered', () => {
            fs.existsSync.mockReturnValue(true);
            // Mock rationale: Simulate a plant watered yesterday, within its frequency.
            fs.readFileSync.mockReturnValue(JSON.stringify({
                name: 'Bloom',
                wateringFrequency: 3,
                lastWatered: '2023-10-25' // 1 day ago
            }));
            setArgs(['check']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('\n--- Bloom\'s Status ---');
            expect(consoleSpy).toHaveBeenCalledWith('Last watered: 2023-10-25 (1 days ago)');
            expect(consoleSpy).toHaveBeenCalledWith('Current mood: Happy');
            expect(consoleSpy).toHaveBeenCalledWith('Message: Your plant is thriving! Keep up the good work.');
            expect(consoleSpy).toHaveBeenCalledWith('\n✨ Bloom is doing great!');
        });

        test('should report thirsty plant if past watering frequency', () => {
            fs.existsSync.mockReturnValue(true);
            // Mock rationale: Simulate a plant watered 4 days ago, with a 3-day frequency.
            fs.readFileSync.mockReturnValue(JSON.stringify({
                name: 'Sprout',
                wateringFrequency: 3,
                lastWatered: '2023-10-22' // 4 days ago
            }));
            setArgs(['check']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('Last watered: 2023-10-22 (4 days ago)');
            expect(consoleSpy).toHaveBeenCalledWith('Current mood: Thirsty');
            expect(consoleSpy).toHaveBeenCalledWith('Message: Your plant looks a bit parched. Maybe a drink soon?');
            expect(consoleSpy).toHaveBeenCalledWith('\n💧 It\'s time to water Sprout!');
        });

        test('should report distressed plant if severely overdue', () => {
            fs.existsSync.mockReturnValue(true);
            // Mock rationale: Simulate a plant watered 10 days ago, with a 3-day frequency.
            fs.readFileSync.mockReturnValue(JSON.stringify({
                name: 'Wilt',
                wateringFrequency: 3,
                lastWatered: '2023-10-16' // 10 days ago
            }));
            setArgs(['check']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('Last watered: 2023-10-16 (10 days ago)');
            expect(consoleSpy).toHaveBeenCalledWith('Current mood: Distressed');
            expect(consoleSpy).toHaveBeenCalledWith('Message: Your plant is in critical condition. Water immediately!');
            expect(consoleSpy).toHaveBeenCalledWith('\n💧 It\'s time to water Wilt!');
        });
    });

    describe('water command', () => {
        test('should report no plant if file does not exist', () => {
            fs.existsSync.mockReturnValue(false);
            setArgs(['water']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('No plant found. Use "init <name> [frequency]" to get one!');
            expect(fs.writeFileSync).not.toHaveBeenCalled();
        });

        test('should update lastWatered date and show updated status', () => {
            fs.existsSync.mockReturnValue(true);
            const initialPlantData = {
                name: 'Aqua',
                wateringFrequency: 5,
                lastWatered: '2023-10-20' // 6 days ago, so thirsty
            };
            fs.readFileSync.mockReturnValue(JSON.stringify(initialPlantData));
            setArgs(['water']);
            run();

            expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
            expect(fs.writeFileSync).toHaveBeenCalledWith(_private.PLANT_FILE, expect.any(String));
            const updatedData = JSON.parse(fs.writeFileSync.mock.calls[0][0]);
            expect(updatedData.lastWatered).toBe('2023-10-26'); // Updated to mockDate
            expect(consoleSpy).toHaveBeenCalledWith('\n💦 You watered Aqua! It looks much happier now.');
            expect(consoleSpy).toHaveBeenCalledWith('Current mood: Happy'); // Should be happy after watering
        });
    });

    describe('default command', () => {
        test('should show usage instructions for unknown command', () => {
            setArgs(['unknown']);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('Usage:');
            expect(consoleSpy).toHaveBeenCalledWith('  node src/index.js init <plant_name> [watering_frequency_days]');
            expect(consoleSpy).toHaveBeenCalledWith('  node src/index.js check');
            expect(consoleSpy).toHaveBeenCalledWith('  node src/index.js water');
        });

        test('should show usage instructions for no command', () => {
            setArgs([]);
            run();

            expect(consoleSpy).toHaveBeenCalledWith('Usage:');
        });
    });

    describe('Private functions', () => {
        test('getDaysSince calculates correctly', () => {
            // Mock rationale: Test the date calculation logic in isolation.
            jest.useRealTimers(); // Use real timers for this specific test to avoid conflicts with mockDate
            const today = new Date('2023-10-26T12:00:00.000Z');
            const yesterday = '2023-10-25';
            const twoDaysAgo = '2023-10-24';
            const tenDaysAgo = '2023-10-16';

            // Mock rationale: Temporarily mock Date to control 'now' for this specific test.
            const mockDateNow = jest.spyOn(global, 'Date').mockImplementation((dateString) => {
                if (dateString) return new Date(dateString);
                return today;
            });

            expect(_private.getDaysSince(yesterday)).toBe(1);
            expect(_private.getDaysSince(twoDaysAgo)).toBe(2);
            expect(_private.getDaysSince(tenDaysAgo)).toBe(10);

            mockDateNow.mockRestore();
            jest.useFakeTimers().setSystemTime(mockDate); // Restore fake timers for other tests
        });

        test('getPlantMood returns correct status and message', () => {
            expect(_private.getPlantMood(1, 3)).toEqual({ status: 'Happy', message: 'Your plant is thriving! Keep up the good work.' });
            expect(_private.getPlantMood(3, 3)).toEqual({ status: 'Happy', message: 'Your plant is thriving! Keep up the good work.' });
            expect(_private.getPlantMood(4, 3)).toEqual({ status: 'Thirsty', message: 'Your plant looks a bit parched. Maybe a drink soon?' });
            expect(_private.getPlantMood(5, 3)).toEqual({ status: 'Thirsty', message: 'Your plant looks a bit parched. Maybe a drink soon?' });
            expect(_private.getPlantMood(6, 3)).toEqual({ status: 'Wilting', message: 'Oh no! Your plant is wilting. It desperately needs water!' });
            expect(_private.getPlantMood(8, 3)).toEqual({ status: 'Wilting', message: 'Oh no! Your plant is wilting. It desperately needs water!' });
            expect(_private.getPlantMood(9, 3)).toEqual({ status: 'Distressed', message: 'Your plant is in critical condition. Water immediately!' });
        });
    });
});
