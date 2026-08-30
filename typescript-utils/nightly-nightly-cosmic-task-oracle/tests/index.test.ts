import { Task, PrioritizedTask } from '../src/types';
import { prioritizeTasks } from '../src/taskOracle'; // Import the actual function
import * as fs from 'fs';
import * as path from 'path';

// Mock the prioritizeTasks function to control its output for CLI tests
// # Mock rationale: Mocking `prioritizeTasks` allows testing the CLI's input parsing and output formatting
// independently of the complex scoring logic, ensuring deterministic CLI behavior.
jest.mock('../src/taskOracle', () => ({
  prioritizeTasks: jest.fn((tasks: Task[]) => {
    // Return a predictable prioritized list based on input tasks for CLI testing
    if (tasks.length === 0) return [];
    const mockPrioritized: PrioritizedTask[] = tasks.map((task, index) => ({
      ...task,
      cosmicScore: 100 - index, // Simple descending score
      rationale: `Mock rationale for ${task.description}`,
    }));
    return mockPrioritized.sort((a, b) => b.cosmicScore - a.cosmicScore);
  }),
}));

// Mock console.log to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });

describe('CLI Integration', () => {
  const originalArgv = process.argv;
  const originalReadFileSync = fs.readFileSync;

  beforeEach(() => {
    jest.clearAllMocks();
    process.argv = [...originalArgv]; // Reset argv for each test
    (prioritizeTasks as jest.Mock).mockClear();
  });

  afterAll(() => {
    process.argv = originalArgv; // Restore original argv
    fs.readFileSync = originalReadFileSync; // Restore original readFileSync
    mockConsoleLog.mockRestore();
    mockConsoleError.mockRestore();
    mockProcessExit.mockRestore();
  });

  it('should display usage if no arguments are provided', async () => {
    process.argv = ['node', 'index.ts'];
    await require('../src/index').main(); // Call the main function directly

    expect(mockConsoleLog).toHaveBeenCalledWith('Usage: npm start "Task 1" "Task 2" ...');
    expect(mockConsoleLog).toHaveBeenCalledWith('Or:    npm start -- --file <path/to/tasks.txt>');
    expect(mockProcessExit).toHaveBeenCalledWith(0);
  });

  it('should parse tasks from command-line arguments and display the top one', async () => {
    process.argv = ['node', 'index.ts', 'Task A', 'Task B', 'Task C'];
    await require('../src/index').main();

    expect(prioritizeTasks).toHaveBeenCalledWith([
      { id: 'task-1', description: 'Task A' },
      { id: 'task-2', description: 'Task B' },
      { id: 'task-3', description: 'Task C' },
    ]);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('✨ The Cosmic Task Oracle has spoken! ✨'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Task: Task A'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Cosmic Score: 100'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Rationale: Mock rationale for Task A'));
    expect(mockProcessExit).not.toHaveBeenCalled();
  });

  it('should read tasks from a specified file', async () => {
    const mockFileContent = 'Task from file 1\nTask from file 2\n# This is a comment\n\nTask from file 3';
    // # Mock rationale: fs.readFileSync is mocked to simulate reading from a file without actual disk I/O.
    // This makes the test deterministic and independent of the file system.
    jest.spyOn(fs, 'readFileSync').mockReturnValue(mockFileContent);

    process.argv = ['node', 'index.ts', '--file', 'test-tasks.txt'];
    await require('../src/index').main();

    expect(fs.readFileSync).toHaveBeenCalledWith(path.resolve(process.cwd(), 'test-tasks.txt'), 'utf8');
    expect(prioritizeTasks).toHaveBeenCalledWith([
      { id: 'file-task-1', description: 'Task from file 1' },
      { id: 'file-task-2', description: 'Task from file 2' },
      { id: 'file-task-3', description: 'Task from file 3' },
    ]);
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Task: Task from file 1'));
    expect(mockProcessExit).not.toHaveBeenCalled();
  });

  it('should handle file not found errors', async () => {
    // # Mock rationale: fs.readFileSync is mocked to simulate a file not found error.
    // This allows testing error handling without requiring a non-existent file.
    jest.spyOn(fs, 'readFileSync').mockImplementation(() => {
      throw new Error('ENOENT: no such file or directory');
    });

    process.argv = ['node', 'index.ts', '--file', 'non-existent.txt'];
    await expect(require('../src/index').main()).rejects.toThrow('process.exit: 1');

    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error reading file non-existent.txt: ENOENT: no such file or directory'));
    expect(mockProcessExit).toHaveBeenCalledWith(1);
  });

  it('should handle no tasks found in file', async () => {
    const mockFileContent = '# Only comments\n\n';
    // # Mock rationale: fs.readFileSync is mocked to simulate a file with no valid tasks.
    jest.spyOn(fs, 'readFileSync').mockReturnValue(mockFileContent);

    process.argv = ['node', 'index.ts', '--file', 'empty-tasks.txt'];
    await require('../src/index').main();

    expect(prioritizeTasks).toHaveBeenCalledWith([]);
    expect(mockConsoleLog).toHaveBeenCalledWith('No tasks provided to the Cosmic Task Oracle. What shall I prioritize?');
    expect(mockProcessExit).toHaveBeenCalledWith(0);
  });

  it('should handle no tasks provided at all', async () => {
    process.argv = ['node', 'index.ts'];
    await require('../src/index').main();
    expect(mockConsoleLog).toHaveBeenCalledWith('Usage: npm start "Task 1" "Task 2" ...');
    expect(mockProcessExit).toHaveBeenCalledWith(0);
  });
});
