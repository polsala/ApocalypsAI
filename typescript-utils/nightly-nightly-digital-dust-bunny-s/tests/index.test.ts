import * as fs from 'fs';
import * as path from 'path';
import { FileInfo, DustBunnyReport } from '../src/types';

// Mock rationale: Simulates file system operations (readdirSync, statSync, existsSync) to ensure deterministic testing
// without actual disk I/O. It allows controlling file metadata like modification times and sizes for various test scenarios.
jest.mock('fs', () => ({
  readdirSync: jest.fn(),
  statSync: jest.fn(),
  existsSync: jest.fn(),
}));

// Mock rationale: To control the current time for deterministic age calculations in tests.
const MOCK_CURRENT_TIMESTAMP = new Date('2024-04-23T10:00:00Z').getTime();

// Helper to create mock stats objects
const createMockStats = (mtime: Date, size: number, isDirectory: boolean = false, isFile: boolean = true) => ({
  mtimeMs: mtime.getTime(),
  size: size,
  isDirectory: () => isDirectory,
  isFile: () => isFile,
  // Add other fs.Stats properties if needed by the utility, but these are sufficient for now
});

// Import the functions to be tested after mocks are set up
import { scanDirectory, parseArgs } from '../src/index';

describe('Digital Dust Bunny Sweeper', () => {
  const mockReaddirSync = fs.readdirSync as jest.Mock;
  const mockStatSync = fs.statSync as jest.Mock;
  const mockExistsSync = fs.existsSync as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
    mockExistsSync.mockReturnValue(true); // Assume target directory always exists for tests
  });

  it('should find no dust bunnies if no files match criteria', () => {
    // Mock a directory with files that are recent and small
    mockReaddirSync.mockReturnValueOnce([
      { name: 'recent_small.txt', isDirectory: () => false, isFile: () => true },
      { name: 'another_recent.log', isDirectory: () => false, isFile: () => true },
    ]);
    mockStatSync
      .mockReturnValueOnce(createMockStats(new Date('2024-04-01T00:00:00Z'), 10 * 1024)) // 10KB, recent
      .mockReturnValueOnce(createMockStats(new Date('2024-03-15T00:00:00Z'), 5 * 1024)); // 5KB, recent

    const report = scanDirectory('/test/dir', 365, 100 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);

    expect(report.totalFilesScanned).toBe(2);
    expect(report.totalDustBunniesFound).toBe(0);
    expect(report.dustBunnies).toEqual([]);
  });

  it('should find dust bunnies based on age criteria', () => {
    // Mock a directory with an old file
    mockReaddirSync.mockReturnValueOnce([
      { name: 'old_file.txt', isDirectory: () => false, isFile: () => true },
      { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStatSync
      .mockReturnValueOnce(createMockStats(new Date('2022-01-01T00:00:00Z'), 1 * 1024 * 1024)) // Old (over 2 years), 1MB
      .mockReturnValueOnce(createMockStats(new Date('2024-04-01T00:00:00Z'), 1 * 1024 * 1024)); // Recent, 1MB

    // Scan for files older than 365 days (1 year)
    const report = scanDirectory('/test/dir', 365, 100 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);

    expect(report.totalFilesScanned).toBe(2);
    expect(report.totalDustBunniesFound).toBe(1);
    expect(report.dustBunnies[0].name).toBe('old_file.txt');
    expect(report.dustBunnies[0].ageDays).toBeCloseTo(843.42, 2); // (MOCK_CURRENT_TIMESTAMP - '2022-01-01') / (1000*60*60*24)
  });

  it('should find dust bunnies based on size criteria', () => {
    // Mock a directory with a large file
    mockReaddirSync.mockReturnValueOnce([
      { name: 'large_file.zip', isDirectory: () => false, isFile: () => true },
      { name: 'small_file.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStatSync
      .mockReturnValueOnce(createMockStats(new Date('2024-04-01T00:00:00Z'), 150 * 1024 * 1024)) // Recent, 150MB
      .mockReturnValueOnce(createMockStats(new Date('2024-04-01T00:00:00Z'), 1 * 1024 * 1024)); // Recent, 1MB

    // Scan for files larger than 100MB
    const report = scanDirectory('/test/dir', 365, 100 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);

    expect(report.totalFilesScanned).toBe(2);
    expect(report.totalDustBunniesFound).toBe(1);
    expect(report.dustBunnies[0].name).toBe('large_file.zip');
    expect(report.dustBunnies[0].size).toBe(150 * 1024 * 1024);
  });

  it('should find dust bunnies in nested directories', () => {
    // Mock a directory structure:
    // /test/dir
    //   ├── sub_dir/
    //   │   └── old_nested.log (old)
    //   └── recent_file.txt
    mockReaddirSync
      .mockReturnValueOnce([
        { name: 'sub_dir', isDirectory: () => true, isFile: () => false },
        { name: 'recent_file.txt', isDirectory: () => false, isFile: () => true },
      ]) // For /test/dir
      .mockReturnValueOnce([
        { name: 'old_nested.log', isDirectory: () => false, isFile: () => true },
      ]); // For /test/dir/sub_dir

    mockStatSync
      .mockReturnValueOnce(createMockStats(new Date('2024-01-01T00:00:00Z'), 10 * 1024, true, false)) // sub_dir
      .mockReturnValueOnce(createMockStats(new Date('2022-01-01T00:00:00Z'), 5 * 1024 * 1024)) // old_nested.log (old, 5MB)
      .mockReturnValueOnce(createMockStats(new Date('2024-04-01T00:00:00Z'), 1 * 1024 * 1024)); // recent_file.txt (recent, 1MB)

    // Scan for files older than 90 days
    const report = scanDirectory('/test/dir', 90, 1 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);

    expect(report.totalFilesScanned).toBe(3); // /test/dir, sub_dir, old_nested.log, recent_file.txt
    expect(report.totalDustBunniesFound).toBe(1);
    expect(report.dustBunnies[0].name).toBe('old_nested.log');
    expect(report.dustBunnies[0].path).toBe('/test/dir/sub_dir/old_nested.log');
  });

  it('should handle empty directories gracefully', () => {
    mockReaddirSync.mockReturnValueOnce([]); // Empty directory
    const report = scanDirectory('/empty/dir', 365, 100 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);
    expect(report.totalFilesScanned).toBe(0);
    expect(report.totalDustBunniesFound).toBe(0);
    expect(report.dustBunnies).toEqual([]);
  });

  it('should handle files that cannot be accessed (EACCES)', () => {
    mockReaddirSync.mockReturnValueOnce([
      { name: 'unreadable.txt', isDirectory: () => false, isFile: () => true },
    ]);
    mockStatSync.mockImplementationOnce(() => {
      const error = new Error('Permission denied');
      (error as any).code = 'EACCES';
      throw error;
    });

    const report = scanDirectory('/test/dir', 365, 100 * 1024 * 1024, MOCK_CURRENT_TIMESTAMP);
    expect(report.totalFilesScanned).toBe(1); // The file was 'scanned' in the sense that readdir found it, but stat failed.
    expect(report.totalDustBunniesFound).toBe(0);
    expect(report.dustBunnies).toEqual([]);
  });

  it('should correctly parse command line arguments', () => {
    // Mock process.argv
    const mockProcessArgv = ['node', 'src/index.ts', '/my/path', '--age', '180', '--size', '50'];
    const { targetDir, minAgeDays, minSizeBytes, dryRun } = parseArgs(mockProcessArgv);

    expect(targetDir).toBe('/my/path');
    expect(minAgeDays).toBe(180);
    expect(minSizeBytes).toBe(50 * 1024 * 1024);
    expect(dryRun).toBe(true);
  });

  it('should use default arguments if not provided', () => {
    const mockProcessArgv = ['node', 'src/index.ts', '/my/path'];
    const { targetDir, minAgeDays, minSizeBytes, dryRun } = parseArgs(mockProcessArgv);

    expect(targetDir).toBe('/my/path');
    expect(minAgeDays).toBe(365); // Default
    expect(minSizeBytes).toBe(100 * 1024 * 1024); // Default
    expect(dryRun).toBe(true); // Default
  });

  it('should exit with error if no target directory is provided', () => {
    const mockProcessArgv = ['node', 'src/index.ts', '--age', '100'];
    const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

    parseArgs(mockProcessArgv);

    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('No target directory specified'));
    expect(mockExit).toHaveBeenCalledWith(1);

    mockExit.mockRestore();
    mockError.mockRestore();
  });

  it('should exit with error for invalid --age argument', () => {
    const mockProcessArgv = ['node', 'src/index.ts', '/my/path', '--age', 'invalid'];
    const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

    parseArgs(mockProcessArgv);

    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('--age must be a positive number of days.'));
    expect(mockExit).toHaveBeenCalledWith(1);

    mockExit.mockRestore();
    mockError.mockRestore();
  });

  it('should exit with error for invalid --size argument', () => {
    const mockProcessArgv = ['node', 'src/index.ts', '/my/path', '--size', 'invalid'];
    const mockExit = jest.spyOn(process, 'exit').mockImplementation((() => {}) as any);
    const mockError = jest.spyOn(console, 'error').mockImplementation(() => {});

    parseArgs(mockProcessArgv);

    expect(mockError).toHaveBeenCalledWith(expect.stringContaining('--size must be a positive number of MB.'));
    expect(mockExit).toHaveBeenCalledWith(1);

    mockExit.mockRestore();
    mockError.mockRestore();
  });
});
