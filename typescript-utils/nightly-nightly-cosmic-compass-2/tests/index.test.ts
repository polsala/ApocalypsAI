import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { Command } from 'commander';
import { PackageJson, OutdatedPackage, AuditReport } from '../src/types';

// Mock chalk to prevent color codes in test output and simplify assertions
jest.mock('chalk', () => ({
  red: jest.fn((text) => text),
  green: jest.fn((text) => text),
  yellow: jest.fn((text) => text),
  blue: jest.fn((text) => text),
  magenta: jest.fn((text) => text),
  cyan: jest.fn((text) => text),
  gray: jest.fn((text) => text),
}));

// Mock fs and child_process to control file system and external command execution
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
}));

jest.mock('child_process', () => ({
  execSync: jest.fn(),
}));

// Mock process.exit to prevent actual exit during tests, instead throwing an error
const mockExit = jest.spyOn(process, 'exit').mockImplementation((code?: number) => {
  throw new Error(`Process exited with code ${code}`);
});

// Mock console.log and console.error to capture output for assertions
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Cosmic Compass CLI', () => {
  const mockPackageJson: PackageJson = {
    name: 'test-project',
    version: '1.0.0',
    dependencies: {
      'dep-a': '^1.0.0',
      'dep-b': '^2.0.0',
    },
    devDependencies: {
      'dev-dep-x': '^0.5.0',
    },
  };

  const mockOutdatedOutputNoDrift = JSON.stringify({});
  const mockOutdatedOutputWithDrift = JSON.stringify({
    'dep-a': {
      current: '1.0.0',
      wanted: '1.1.0',
      latest: '2.0.0',
      type: 'dependencies',
      url: 'https://example.com/dep-a',
    },
    'dev-dep-x': {
      current: '0.5.0',
      wanted: '0.5.1',
      latest: '1.0.0',
      type: 'devDependencies',
      url: 'https://example.com/dev-dep-x',
    },
  });

  const mockAuditOutputNoAnomalies = JSON.stringify({
    advisories: {},
    metadata: {
      vulnerabilities: {
        info: 0,
        low: 0,
        moderate: 0,
        high: 0,
        critical: 0,
      },
    },
  });

  const mockAuditOutputWithAnomalies = JSON.stringify({
    advisories: {
      '123': {
        id: 123,
        title: 'High severity vulnerability in dep-b',
        severity: 'high',
        vulnerable_versions: '<2.1.0',
        patched_versions: '>=2.1.0',
        url: 'https://example.com/vuln/123',
        module_name: 'dep-b',
      },
      '456': {
        id: 456,
        title: 'Moderate severity vulnerability in dep-a',
        severity: 'moderate',
        vulnerable_versions: '<1.0.5',
        patched_versions: '>=1.0.5',
        url: 'https://example.com/vuln/456',
        module_name: 'dep-a',
      },
    },
    metadata: {
      vulnerabilities: {
        info: 0,
        low: 0,
        moderate: 1,
        high: 1,
        critical: 0,
      },
    },
  });

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock rationale: We need to control the file system and external command execution
    // to make tests deterministic and offline. `readFileSync` is mocked to return a static
    // `package.json` content, and `execSync` is mocked to return predefined outputs for
    // `npm outdated` and `npm audit` commands.
    (readFileSync as jest.Mock).mockReturnValue(JSON.stringify(mockPackageJson));

    // Set NODE_ENV to 'test' to prevent commander from parsing process.argv prematurely
    process.env.NODE_ENV = 'test';
  });

  afterAll(() => {
    mockExit.mockRestore();
    mockConsoleLog.mockRestore();
    mockConsoleError.mockRestore();
    delete process.env.NODE_ENV; // Clean up environment variable
  });

  it('should report no drift and no anomalies when everything is up-to-date and secure', async () => {
    (execSync as jest.Mock)
      .mockReturnValueOnce(mockOutdatedOutputNoDrift) // npm outdated
      .mockReturnValueOnce(mockAuditOutputNoAnomalies); // npm audit

    const { program } = require('../src/index'); // Re-import to get fresh commander instance if needed, or ensure it's cleared
    await program.parseAsync([]);

    expect(readFileSync).toHaveBeenCalledWith('./package.json', 'utf8');
    expect(execSync).toHaveBeenCalledWith('npm outdated --json', { stdio: 'pipe' });
    expect(execSync).toHaveBeenCalledWith('npm audit --json', { stdio: 'pipe' });

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('All dependencies are perfectly aligned'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No security anomalies detected'));
    expect(mockConsoleError).not.toHaveBeenCalled();
    expect(mockExit).not.toHaveBeenCalled();
  });

  it('should report outdated packages (drift) but no security anomalies', async () => {
    (execSync as jest.Mock)
      .mockReturnValueOnce(mockOutdatedOutputWithDrift) // npm outdated
      .mockReturnValueOnce(mockAuditOutputNoAnomalies); // npm audit

    const { program } = require('../src/index');
    await program.parseAsync([]);

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('2 packages are drifting out of alignment!'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('dep-a: 1.0.0 -> 2.0.0 (wanted: 1.1.0)'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('dev-dep-x: 0.5.0 -> 1.0.0 (wanted: 0.5.1)'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Consider running `npm update`'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('No security anomalies detected'));
    expect(mockConsoleError).not.toHaveBeenCalled();
    expect(mockExit).not.toHaveBeenCalled();
  });

  it('should report security anomalies but no outdated packages (no drift)', async () => {
    (execSync as jest.Mock)
      .mockReturnValueOnce(mockOutdatedOutputNoDrift) // npm outdated
      .mockImplementationOnce(() => {
        // Mock rationale: npm audit exits with non-zero code if vulnerabilities are found.
        // We simulate this by throwing an error with stdout containing the JSON report,
        // as `execSync` would do in a real scenario.
        const error = new Error('npm audit found vulnerabilities') as any;
        error.stdout = mockAuditOutputWithAnomalies;
        throw error;
      });

    const { program } = require('../src/index');
    await program.parseAsync([]);

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('All dependencies are perfectly aligned'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('2 security anomalies detected!'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('HIGH: dep-b - High severity vulnerability in dep-b'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('MODERATE: dep-a - Moderate severity vulnerability in dep-a'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Run `npm audit fix`'));
    expect(mockConsoleError).not.toHaveBeenCalled();
    expect(mockExit).not.toHaveBeenCalled();
  });

  it('should report both outdated packages and security anomalies', async () => {
    (execSync as jest.Mock)
      .mockReturnValueOnce(mockOutdatedOutputWithDrift) // npm outdated
      .mockImplementationOnce(() => {
        // Mock rationale: Simulate npm audit finding vulnerabilities by throwing an error with stdout.
        const error = new Error('npm audit found vulnerabilities') as any;
        error.stdout = mockAuditOutputWithAnomalies;
        throw error;
      });

    const { program } = require('../src/index');
    await program.parseAsync([]);

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('2 packages are drifting out of alignment!'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('2 security anomalies detected!'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Consider running `npm update`'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Run `npm audit fix`'));
    expect(mockConsoleError).not.toHaveBeenCalled();
    expect(mockExit).not.toHaveBeenCalled();
  });

  it('should handle missing package.json gracefully', async () => {
    (readFileSync as jest.Mock).mockImplementation(() => {
      // Mock rationale: Simulate file not found error for package.json.
      const error = new Error('ENOENT: no such file or directory, open \'./package.json\'') as any;
      error.code = 'ENOENT';
      error.path = 'package.json';
      throw error;
    });

    const { program } = require('../src/index');
    await expect(program.parseAsync([])).rejects.toThrow('Process exited with code 1');

    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('No package.json found'));
    expect(mockExit).toHaveBeenCalledWith(1);
  });

  it('should handle errors from npm commands gracefully', async () => {
    (execSync as jest.Mock).mockImplementationOnce(() => {
      // Mock rationale: Simulate an unexpected error from an npm command (e.g., npm not found or other system error).
      const error = new Error('Command failed: npm outdated') as any;
      error.stderr = 'An unknown npm error occurred.';
      throw error;
    });

    const { program } = require('../src/index');
    await expect(program.parseAsync([])).rejects.toThrow('Process exited with code 1');

    expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining('Cosmic disturbance detected: An unknown npm error occurred.'));
    expect(mockExit).toHaveBeenCalledWith(1);
  });
});
