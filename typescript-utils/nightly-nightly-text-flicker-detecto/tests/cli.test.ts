import { runCli } from '../src/cli';
import * as fs from 'fs';

describe('CLI Integration', () => {
  let consoleLogSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;
  let processExitSpy: jest.SpyInstance;
  let readFileSyncSpy: jest.SpyInstance;
  let originalArgv: string[];

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });
    readFileSyncSpy = jest.spyOn(fs, 'readFileSync');
    originalArgv = process.argv;
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
    processExitSpy.mockRestore();
    readFileSyncSpy.mockRestore();
    process.argv = originalArgv;
  });

  it('should print usage and exit if not enough arguments are provided', () => {
    process.argv = ['node', 'cli.js', 'fileA.txt'];
    expect(() => runCli()).toThrow('process.exit: 1');
    expect(consoleErrorSpy).toHaveBeenCalledWith('Usage: node dist/cli.js <path_to_file_A> <path_to_file_B>');
  });

  it('should print usage and exit if too many arguments are provided', () => {
    process.argv = ['node', 'cli.js', 'fileA.txt', 'fileB.txt', 'extra.txt'];
    expect(() => runCli()).toThrow('process.exit: 1');
    expect(consoleErrorSpy).toHaveBeenCalledWith('Usage: node dist/cli.js <path_to_file_A> <path_to_file_B>');
  });

  it('should handle file not found errors', () => {
    process.argv = ['node', 'cli.js', 'nonexistent.txt', 'fileB.txt'];
    // Mock rationale: fs.readFileSync is mocked to simulate a file not found error,
    // ensuring the CLI handles I/O errors gracefully without actual file system interaction.
    readFileSyncSpy.mockImplementation((filePath: string) => {
      if (filePath === 'nonexistent.txt') {
        throw new Error('ENOENT: no such file or directory, open \'nonexistent.txt\'');
      }
      return 'content';
    });

    expect(() => runCli()).toThrow('process.exit: 1');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error: ENOENT: no such file or directory'));
  });

  it('should print a flicker report for differing files', () => {
    process.argv = ['node', 'cli.js', 'fileA.txt', 'fileB.txt'];
    // Mock rationale: fs.readFileSync is mocked to provide deterministic file content
    // without actual file I/O, ensuring tests are fast and isolated.
    readFileSyncSpy.mockReturnValueOnce('Line 1 original\nLine 2 same\nLine 3 changed') // fileA.txt
                   .mockReturnValueOnce('Line 1 changed\nLine 2 same\nLine 3 different'); // fileB.txt

    runCli();

    expect(consoleLogSpy).toHaveBeenCalledWith('Temporal Flicker Report:');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining("Comparing 'fileA.txt' (Temporal Anchor) with 'fileB.txt' (Temporal Echo)"));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('--- Line 1 ---'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Original: Line 1 original'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Echo:     Line 1 changed'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Flicker:        ^^^^^^^'));
    expect(consoleLogSpy).not.toHaveBeenCalledWith(expect.stringContaining('--- Line 2 ---')); // Line 2 is identical
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('--- Line 3 ---'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Original: Line 3 changed'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Echo:     Line 3 different'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Flicker:           ^^^^^^^^'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Total lines compared: 3'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Lines with flicker: 2'));
  });

  it('should indicate no flicker for identical files', () => {
    process.argv = ['node', 'cli.js', 'fileA.txt', 'fileB.txt'];
    const identicalContent = 'Line 1\nLine 2\nLine 3';
    // Mock rationale: fs.readFileSync is mocked to provide deterministic file content
    // without actual file I/O, ensuring tests are fast and isolated.
    readFileSyncSpy.mockReturnValueOnce(identicalContent)
                   .mockReturnValueOnce(identicalContent);

    runCli();

    expect(consoleLogSpy).toHaveBeenCalledWith('Temporal Flicker Report:');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining("Comparing 'fileA.txt' (Temporal Anchor) with 'fileB.txt' (Temporal Echo)"));
    expect(consoleLogSpy).toHaveBeenCalledWith('No flicker detected. Files are identical.');
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Total lines compared: 3'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Lines with flicker: 0'));
  });

  it('should handle files with different line counts correctly', () => {
    process.argv = ['node', 'cli.js', 'fileA.txt', 'fileB.txt'];
    // Mock rationale: fs.readFileSync is mocked to provide deterministic file content
    // without actual file I/O, ensuring tests are fast and isolated.
    readFileSyncSpy.mockReturnValueOnce('Line 1\nLine 2') // fileA.txt
                   .mockReturnValueOnce('Line 1 changed\nLine 2\nLine 3 new'); // fileB.txt

    runCli();

    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('--- Line 1 ---'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Original: Line 1'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Echo:     Line 1 changed'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Flicker:        ^^^^^^^'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('--- Line 3 ---'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Original: ')); // Empty line for original
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Echo:     Line 3 new'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Flicker:  ^^^^^^^^^^'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Total lines compared: 3'));
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Lines with flicker: 2'));
  });
});
