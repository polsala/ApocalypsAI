const { triageTasks, calculateTriageScore, program } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We want to test the core logic of triageTasks and calculateTriageScore
// without actual file system operations or CLI parsing. The CLI parsing and file reading
// are handled by commander.js and fs, which are external dependencies. We mock
// fs.readFileSync and path.resolve to provide deterministic input for our tests.
jest.mock('fs');
jest.mock('path');

describe('calculateTriageScore', () => {
    test('should calculate score correctly for valid inputs', () => {
        const task1 = { description: 'High priority, fast decay', urgency: 9, decay_rate: 'fast' };
        const scoredTask1 = calculateTriageScore(task1);
        expect(scoredTask1.triage_score).toBe(13.5);
        expect(scoredTask1.urgency).toBe(9);
        expect(scoredTask1.decay_rate).toBe('fast');

        const task2 = { description: 'Medium priority, medium decay', urgency: 5, decay_rate: 'medium' };
        const scoredTask2 = calculateTriageScore(task2);
        expect(scoredTask2.triage_score).toBe(5.0);
        expect(scoredTask2.urgency).toBe(5);
        expect(scoredTask2.decay_rate).toBe('medium');

        const task3 = { description: 'Low priority, slow decay', urgency: 2, decay_rate: 'slow' };
        const scoredTask3 = calculateTriageScore(task3);
        expect(scoredTask3.triage_score).toBe(1.0);
        expect(scoredTask3.urgency).toBe(2);
        expect(scoredTask3.decay_rate).toBe('slow');
    });

    test('should apply default urgency and decay_rate if missing', () => {
        const task = { description: 'Task with defaults' };
        const scoredTask = calculateTriageScore(task);
        expect(scoredTask.triage_score).toBe(5.0); // Default urgency 5 * Default decay medium 1.0
        expect(scoredTask.urgency).toBe(5);
        expect(scoredTask.decay_rate).toBe('medium');
    });

    test('should handle invalid urgency by using default', () => {
        const task = { description: 'Invalid urgency', urgency: 'ten', decay_rate: 'fast' };
        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console warnings for cleaner test output.
        const scoredTask = calculateTriageScore(task);
        expect(scoredTask.triage_score).toBe(7.5); // Default urgency 5 * fast decay 1.5
        expect(scoredTask.urgency).toBe(5);
        expect(scoredTask.decay_rate).toBe('fast');
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining("Invalid urgency 'ten'"));
        consoleWarnSpy.mockRestore();
    });

    test('should handle out-of-range urgency by using default', () => {
        const task = { description: 'Urgency too high', urgency: 15, decay_rate: 'medium' };
        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console warnings for cleaner test output.
        const scoredTask = calculateTriageScore(task);
        expect(scoredTask.triage_score).toBe(5.0); // Default urgency 5 * medium decay 1.0
        expect(scoredTask.urgency).toBe(5);
        expect(scoredTask.decay_rate).toBe('medium');
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining("Invalid urgency '15'"));
        consoleWarnSpy.mockRestore();
    });

    test('should handle invalid decay_rate by using default', () => {
        const task = { description: 'Invalid decay rate', urgency: 7, decay_rate: 'super-fast' };
        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console warnings for cleaner test output.
        const scoredTask = calculateTriageScore(task);
        expect(scoredTask.triage_score).toBe(7.0); // Urgency 7 * Default decay medium 1.0
        expect(scoredTask.urgency).toBe(7);
        expect(scoredTask.decay_rate).toBe('medium');
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining("Invalid decay_rate 'super-fast'"));
        consoleWarnSpy.mockRestore();
    });

    test('should return a new object without modifying the original task', () => {
        const originalTask = { description: 'Original task', urgency: 6, decay_rate: 'slow' };
        const scoredTask = calculateTriageScore(originalTask);
        expect(scoredTask).not.toBe(originalTask); // Ensure it's a new object
        expect(originalTask).toEqual({ description: 'Original task', urgency: 6, decay_rate: 'slow' }); // Original remains unchanged
    });
});

describe('triageTasks', () => {
    test('should sort tasks correctly by triage score', () => {
        const tasks = [
            { id: 1, description: 'Repair temporal displacement unit', urgency: 9, decay_rate: 'fast' }, // 13.5
            { id: 2, description: 'Gather glowing mushrooms for dinner', urgency: 3, decay_rate: 'medium' }, // 3.0
            { id: 3, description: 'Archive ancient prophecies', urgency: 7, decay_rate: 'slow' }, // 3.5
            { id: 4, description: 'Calibrate Chrono-Compass', urgency: 8, decay_rate: 'fast' }, // 12.0
            { id: 5, description: 'Polish time-traveling boots', urgency: 1, decay_rate: 'slow' }, // 0.5
            { id: 6, description: 'Scavenge for spare parts', urgency: 5 } // Default: 5.0
        ];

        const sortedTasks = triageTasks(tasks);

        expect(sortedTasks.length).toBe(6);
        expect(sortedTasks[0].description).toBe('Repair temporal displacement unit');
        expect(sortedTasks[0].triage_score).toBe(13.5);
        expect(sortedTasks[1].description).toBe('Calibrate Chrono-Compass');
        expect(sortedTasks[1].triage_score).toBe(12.0);
        expect(sortedTasks[2].description).toBe('Scavenge for spare parts');
        expect(sortedTasks[2].triage_score).toBe(5.0);
        expect(sortedTasks[3].description).toBe('Archive ancient prophecies');
        expect(sortedTasks[3].triage_score).toBe(3.5);
        expect(sortedTasks[4].description).toBe('Gather glowing mushrooms for dinner');
        expect(sortedTasks[4].triage_score).toBe(3.0);
        expect(sortedTasks[5].description).toBe('Polish time-traveling boots');
        expect(sortedTasks[5].triage_score).toBe(0.5);
    });

    test('should handle an empty array gracefully', () => {
        const tasks = [];
        const sortedTasks = triageTasks(tasks);
        expect(sortedTasks).toEqual([]);
    });

    test('should throw an error if input is not an array', () => {
        expect(() => triageTasks(null)).toThrow("Input must be an array of tasks.");
        expect(() => triageTasks({})).toThrow("Input must be an array of tasks.");
        expect(() => triageTasks("string")).toThrow("Input must be an array of tasks.");
    });

    test('should handle tasks with only description', () => {
        const tasks = [
            { description: 'Task A' }, // Default: 5.0
            { description: 'Task B' }  // Default: 5.0
        ];
        const sortedTasks = triageTasks(tasks);
        expect(sortedTasks.length).toBe(2);
        expect(sortedTasks[0].triage_score).toBe(5.0);
        expect(sortedTasks[1].triage_score).toBe(5.0);
        // Order might be arbitrary if scores are equal, but values should be correct
    });
});

// Test the CLI part by mocking fs and process.exit
describe('CLI execution', () => {
    let consoleLogSpy;
    let consoleErrorSpy;
    let processExitSpy;

    beforeEach(() => {
        consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {}); // Mock rationale: Capture console output for verification.
        consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock rationale: Capture console output for verification.
        processExitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {}); // Mock rationale: Prevent process from exiting during tests.
        fs.readFileSync.mockClear();
        path.resolve.mockClear();
    });

    afterEach(() => {
        consoleLogSpy.mockRestore();
        consoleErrorSpy.mockRestore();
        processExitSpy.mockRestore();
    });

    test('should read file and print sorted tasks', async () => {
        const mockTasks = [
            { id: 1, description: 'Task A', urgency: 9, decay_rate: 'fast' },
            { id: 2, description: 'Task B', urgency: 3, decay_rate: 'medium' }
        ];
        fs.readFileSync.mockReturnValueOnce(JSON.stringify(mockTasks)); // Mock rationale: Simulate reading a JSON file.
        path.resolve.mockReturnValueOnce('/mock/path/tasks.json'); // Mock rationale: Simulate path resolution.

        // Use the exported program to parse arguments
        await program.parseAsync(['node', 'index.js', '-f', 'tasks.json']);

        expect(fs.readFileSync).toHaveBeenCalledWith('/mock/path/tasks.json', 'utf8');
        expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('--- Triage Report ---'));
        expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('1. Task A (Urgency: 9, Decay: fast, Score: 13.5)'));
        expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('2. Task B (Urgency: 3, Decay: medium, Score: 3.0)'));
        expect(processExitSpy).not.toHaveBeenCalled();
    });

    test('should exit with error if file is not specified', async () => {
        // Clear previous arguments to ensure no file option is present
        program.parse([]);
        await program.parseAsync(['node', 'index.js']);

        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error: No input file specified.'));
        expect(processExitSpy).toHaveBeenCalledWith(1);
    });

    test('should exit with error if file reading fails', async () => {
        fs.readFileSync.mockImplementationOnce(() => { // Mock rationale: Simulate a file reading error.
            throw new Error('File not found');
        });
        path.resolve.mockReturnValueOnce('/mock/path/nonexistent.json'); // Mock rationale: Simulate path resolution.

        await program.parseAsync(['node', 'index.js', '-f', 'nonexistent.json']);

        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing file nonexistent.json: File not found'));
        expect(processExitSpy).toHaveBeenCalledWith(1);
    });

    test('should exit with error if JSON parsing fails', async () => {
        fs.readFileSync.mockReturnValueOnce('{"tasks": [}'); // Mock rationale: Simulate invalid JSON content.
        path.resolve.mockReturnValueOnce('/mock/path/invalid.json'); // Mock rationale: Simulate path resolution.

        await program.parseAsync(['node', 'index.js', '-f', 'invalid.json']);

        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing file invalid.json: Unexpected end of JSON input'));
        expect(processExitSpy).toHaveBeenCalledWith(1);
    });

    test('should exit with error if triageTasks throws an error (e.g., malformed JSON array)', async () => {
        fs.readFileSync.mockReturnValueOnce('{"not_an_array": "value"}'); // Mock rationale: Simulate JSON that's not an array.
        path.resolve.mockReturnValueOnce('/mock/path/malformed.json'); // Mock rationale: Simulate path resolution.

        await program.parseAsync(['node', 'index.js', '-f', 'malformed.json']);

        expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error during task triage: Input must be an array of tasks.'));
        expect(processExitSpy).toHaveBeenCalledWith(1);
    });
});
