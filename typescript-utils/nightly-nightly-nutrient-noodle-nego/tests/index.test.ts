import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: fs operations are external dependencies and should not be performed during unit tests.
// Mocking them ensures deterministic, offline testing and prevents actual file system changes.
jest.mock('fs', () => ({
  existsSync: jest.fn(),
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
}));

// Mock rationale: process.argv is an external dependency (CLI arguments).
// Mocking it allows controlling the input to the CLI for deterministic testing.
// Mocking console.log/error prevents test output pollution and allows assertion on messages.
const mockProcessExit = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
  throw new Error(`process.exit called with code: ${code}`);
});
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

const RECORD_FILE = path.join(process.cwd(), '.nutrient_noodle_record.json');

describe('CLI Tool', () => {
  let originalArgv: string[];

  beforeEach(() => {
    originalArgv = process.argv; // Store original argv
    jest.clearAllMocks();
    (fs.existsSync as jest.Mock).mockReturnValue(false); // Default: no record file exists
    (fs.readFileSync as jest.Mock).mockReturnValue(''); // Default: empty content
  });

  afterEach(() => {
    process.argv = originalArgv; // Restore original argv
    mockProcessExit.mockRestore();
    mockConsoleLog.mockRestore();
    mockConsoleError.mockRestore();
  });

  it('should suggest the first paste if no record exists', () => {
    process.argv = ['node', 'index.js']; // Simulate running without args
    require('../src/index'); // Run the main function

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Algae & Soy Blend'));
    expect(fs.writeFileSync).toHaveBeenCalledWith(
      RECORD_FILE,
      JSON.stringify({ lastConsumedId: 'algae-soy', history: ['algae-soy'] }, null, 2),
      'utf8'
    );
  });

  it('should load existing record and suggest next paste', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    (fs.readFileSync as jest.Mock).mockReturnValue(JSON.stringify({ lastConsumedId: 'algae-soy', history: ['algae-soy'] }));

    process.argv = ['node', 'index.js'];
    require('../src/index');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Synthetic Berry Burst'));
    expect(fs.writeFileSync).toHaveBeenCalledWith(
      RECORD_FILE,
      JSON.stringify({ lastConsumedId: 'berry-burst', history: ['berry-burst', 'algae-soy'] }, null, 2),
      'utf8'
    );
  });

  it('should suggest mood-matching paste if --mood is provided', () => {
    // Set up a record where 'algae-soy' is last consumed, 'berry-burst' is next rotationally AND sweet.
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    (fs.readFileSync as jest.Mock).mockReturnValue(JSON.stringify({ lastConsumedId: 'algae-soy', history: ['algae-soy'] }));

    process.argv = ['node', 'index.js', '--mood', 'sweet'];
    require('../src/index');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Synthetic Berry Burst'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("(Influenced by your 'sweet' mood)"));
    expect(fs.writeFileSync).toHaveBeenCalledWith(
      RECORD_FILE,
      JSON.stringify({ lastConsumedId: 'berry-burst', history: ['berry-burst', 'algae-soy'] }, null, 2),
      'utf8'
    );
  });

  it('should handle invalid record file gracefully', () => {
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    (fs.readFileSync as jest.Mock).mockReturnValue('invalid json'); // Simulate corrupted file

    process.argv = ['node', 'index.js'];
    require('../src/index');

    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error loading consumption record'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Algae & Soy Blend')); // Should start fresh
  });

  it('should handle write error gracefully', () => {
    (fs.writeFileSync as jest.Mock).mockImplementation(() => {
      throw new Error('Simulated write failed'); // Simulate file write error
    });

    process.argv = ['node', 'index.js'];
    require('../src/index');

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Algae & Soy Blend'));
    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Error saving consumption record'));
  });
});
