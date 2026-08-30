import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

// Mock rationale: We need to simulate file system operations for the CLI tool
// without actually touching the disk. This ensures tests are deterministic and offline.
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
  },
  // Keep other fs functions if needed, but for this CLI, readdir is the primary interaction.
  ...jest.requireActual('fs'),
}));

// Mock rationale: We need to control the path resolution for consistent testing
// of the CLI's interaction with the file system. This ensures that relative paths
// are calculated predictably within the mocked environment.
jest.mock('path', () => ({
  ...jest.requireActual('path'),
  resolve: jest.fn((p: string) => p), // Mock resolve to return path as is for simplicity in tests
  relative: jest.fn((from: string, to: string) => {
    if (to.startsWith(from)) {
      const relative = to.substring(from.length);
      return relative.startsWith('/') ? relative.substring(1) : relative;
    }
    return to;
  }),
}));

const mockReaddir = fs.promises.readdir as jest.MockedFunction<typeof fs.promises.readdir>;
const mockPathResolve = path.resolve as jest.MockedFunction<typeof path.resolve>;
const mockPathRelative = path.relative as jest.MockedFunction<typeof path.relative>;

const cliEntrypoint = path.join(__dirname, '../src/cli.ts');

describe('CosmicCompass CLI', () => {
  const mockProjectRoot = '/mock/cli-project';

  beforeEach(() => {
    jest.clearAllMocks();
    mockPathResolve.mockImplementation((p: string) => p);
    mockPathRelative.mockImplementation((from: string, to: string) => {
      if (to.startsWith(from)) {
        const relative = to.substring(from.length);
        return relative.startsWith('/') ? relative.substring(1) : relative;
      }
      return to;
    });
  });

  it('should display help message when no arguments are provided', (done) => {
    exec(`npx ts-node ${cliEntrypoint}`, (error, stdout, stderr) => {
      expect(stdout).toContain('Usage: cosmic-compass [options] <path>');
      expect(error).not.toBeNull(); // Commander exits with error if required arg is missing
      done();
    });
  });

  it('should scan a directory and report success without search', (done) => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'file1.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    exec(`npx ts-node ${cliEntrypoint} ${mockProjectRoot}`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toContain(`Initiating Cosmic Scan of: ${mockProjectRoot}`);
      expect(stdout).toContain('Cosmic Atlas built! 1 celestial bodies mapped.');
      expect(stdout).toContain('Use --search <keywords...> to find specific stellar phenomena.');
      done();
    });
  });

  it('should search for keywords and display results', (done) => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'component.ts', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
      { name: 'utils', isDirectory: () => true, isFile: () => false, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);
    mockReaddir.mockResolvedValueOnce([]); // For utils dir

    exec(`npx ts-node ${cliEntrypoint} ${mockProjectRoot} --search comp`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toContain('Searching for cosmic anomalies matching: comp');
      expect(stdout).toContain('1 celestial bodies detected:');
      expect(stdout).toContain('⭐ component.ts');
      expect(stdout).toContain("Found 'comp' in path/name");
      done();
    });
  });

  it('should report no results found for a search', (done) => {
    mockReaddir.mockResolvedValueOnce([
      { name: 'file.txt', isDirectory: () => false, isFile: () => true, isBlockDevice: () => false, isCharacterDevice: () => false, isFIFO: () => false, isSocket: () => false, isSymbolicLink: () => false },
    ]);

    exec(`npx ts-node ${cliEntrypoint} ${mockProjectRoot} --search nonexistent`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toContain('No celestial bodies found matching your search criteria. The void is vast.');
      done();
    });
  });

  it('should handle file system errors gracefully and exit with error code', (done) => {
    mockReaddir.mockRejectedValueOnce(new Error('Permission denied'));

    exec(`npx ts-node ${cliEntrypoint} ${mockProjectRoot}`, (error, stdout, stderr) => {
      expect(error).not.toBeNull(); // Expect an error from the CLI process
      expect(error?.code).toBe(1); // Expect exit code 1 due to process.exit(1)
      expect(stderr).toContain('Cosmic disturbance detected: Permission denied');
      done();
    });
  });
});
