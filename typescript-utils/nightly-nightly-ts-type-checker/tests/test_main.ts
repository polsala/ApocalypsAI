import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';

// Mock the validateJsonAgainstSchema function for isolated testing
jest.mock('../src/main', () => ({
  ...jest.requireActual('../src/main'),
  validateJsonAgainstSchema: jest.fn(),
}));

import { validateJsonAgainstSchema } from '../src/main';

// Mock rationale: We are mocking the core validation logic to test the CLI argument parsing and file handling separately.
// The actual validation logic is complex and best tested with real TS compilation.

describe('Nightly TypeScript Type Checker', () => {
  const mockSchemaPath = path.join(__dirname, 'mock_schema.ts');
  const mockDataPath = path.join(__dirname, 'mock_data.json');

  beforeAll(() => {
    // Create mock schema file
    const mockSchemaContent = `
      export interface MockData {
        id: number;
        name: string;
        isActive?: boolean;
        tags: string[];
      }
    `;
    fs.writeFileSync(mockSchemaPath, mockSchemaContent);

    // Create mock data file
    const mockDataContent = `
      {
        "id": 1,
        "name": "Test Item",
        "tags": ["a", "b"]
      }
    `;
    fs.writeFileSync(mockDataPath, mockDataContent);
  });

  afterAll(() => {
    // Clean up mock files
    fs.unlinkSync(mockSchemaPath);
    fs.unlinkSync(mockDataPath);
  });

  it('should correctly parse arguments and call validation', async () => {
    // Mock the actual validateJsonAgainstSchema function to check if it's called
    const mockValidate = validateJsonAgainstSchema as jest.Mock;
    mockValidate.mockReturnValue({ isValid: true, errors: [] }); // Default mock return

    // Mock process.argv to simulate command line arguments
    const originalArgv = process.argv;
    process.argv = ['node', 'dist/main.js', '--schema', mockSchemaPath, '--data', mockDataPath];

    // Mock console.log and console.error to capture output
    const consoleSpyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    const consoleSpyError = jest.spyOn(console, 'error').mockImplementation(() => {});

    // Mock ts.createProgram to return a dummy program object
    const mockProgram = {
      getTypeChecker: () => ({}),
      getSourceFile: () => ({}),
      getRootFileNames: () => [mockSchemaPath],
    } as ts.Program;
    jest.spyOn(ts, 'createProgram').mockReturnValue(mockProgram);

    // Mock fs.readFileSync to return dummy JSON data
    jest.spyOn(fs, 'readFileSync').mockReturnValue(Buffer.from('{"id": 1, "name": "Test Item", "tags": ["a", "b"]}'));

    // Mock path.resolve to return the input path directly
    jest.spyOn(path, 'resolve').mockImplementation((p) => p);

    // Mock fs.existsSync to return true for existing files
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);

    // Dynamically import main to ensure mocks are applied before execution
    const { main } = await import('../src/main');
    await main();

    // Assert that validateJsonAgainstSchema was called with correct arguments
    expect(mockValidate).toHaveBeenCalledTimes(1);
    // We can't easily check the exact JSON data passed without more complex mocking of JSON.parse, but we can check the interface name extraction.
    expect(mockValidate).toHaveBeenCalledWith(expect.any(Object), 'MockData', expect.any(Object));

    // Assert console output for success
    expect(consoleSpyLog).toHaveBeenCalledWith('Data is valid according to the schema.');

    // Restore mocks and original argv
    consoleSpyLog.mockRestore();
    consoleSpyError.mockRestore();
    process.argv = originalArgv;
    jest.restoreAllMocks();
  });

  it('should report validation errors', async () => {
    const mockValidate = validateJsonAgainstSchema as jest.Mock;
    mockValidate.mockReturnValue({
      isValid: false,
      errors: [
        "Property 'name' is missing.",
        "At path 'tags': Expected string, got number."
      ]
    });

    const originalArgv = process.argv;
    process.argv = ['node', 'dist/main.js', '--schema', mockSchemaPath, '--data', mockDataPath];

    const consoleSpyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    const consoleSpyError = jest.spyOn(console, 'error').mockImplementation(() => {});

    const mockProgram = {
      getTypeChecker: () => ({}),
      getSourceFile: () => ({}),
      getRootFileNames: () => [mockSchemaPath],
    } as ts.Program;
    jest.spyOn(ts, 'createProgram').mockReturnValue(mockProgram);

    jest.spyOn(fs, 'readFileSync').mockReturnValue(Buffer.from('{"id": 1, "tags": ["a", 123]}'));
    jest.spyOn(path, 'resolve').mockImplementation((p) => p);
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);

    const { main } = await import('../src/main');
    await main();

    expect(consoleSpyError).toHaveBeenCalledWith('Validation failed:');
    expect(consoleSpyError).toHaveBeenCalledWith("- Property 'name' is missing.");
    expect(consoleSpyError).toHaveBeenCalledWith("- At path 'tags': Expected string, got number.");

    consoleSpyLog.mockRestore();
    consoleSpyError.mockRestore();
    process.argv = originalArgv;
    jest.restoreAllMocks();
  });

  it('should handle missing schema file', async () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'dist/main.js', '--schema', 'non_existent_schema.ts', '--data', mockDataPath];

    const consoleSpyError = jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(fs, 'existsSync').mockImplementation((p) => p === mockDataPath);

    const { main } = await import('../src/main');
    await expect(main()).rejects.toThrow(); // Expecting an error to be thrown or process.exit(1)
    expect(consoleSpyError).toHaveBeenCalledWith('Error: Schema file not found at non_existent_schema.ts');

    consoleSpyError.mockRestore();
    process.argv = originalArgv;
    jest.restoreAllMocks();
  });

  it('should handle missing data file', async () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'dist/main.js', '--schema', mockSchemaPath, '--data', 'non_existent_data.json'];

    const consoleSpyError = jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(fs, 'existsSync').mockImplementation((p) => p === mockSchemaPath);

    const { main } = await import('../src/main');
    await expect(main()).rejects.toThrow(); // Expecting an error to be thrown or process.exit(1)
    expect(consoleSpyError).toHaveBeenCalledWith('Error: Data file not found at non_existent_data.json');

    consoleSpyError.mockRestore();
    process.argv = originalArgv;
    jest.restoreAllMocks();
  });
});
