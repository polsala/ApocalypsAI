const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Mock child_process and fs
jest.mock('child_process');
jest.mock('fs');

// Mock process.exit to prevent tests from terminating
const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
const mockStdoutWrite = jest.spyOn(process.stdout, 'write').mockImplementation(() => {});
const mockStderrWrite = jest.spyOn(process.stderr, 'write').mockImplementation(() => {});
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Nightly Chrono-Echo CLI', () => {
    let originalArgv;

    beforeEach(() => {
        originalArgv = process.argv;
        jest.clearAllMocks();
        // Reset mocks for each test
        mockExit.mockClear();
        mockStdoutWrite.mockClear();
        mockStderrWrite.mockClear();
        mockConsoleLog.mockClear();
        mockConsoleError.mockClear();
    });

    afterEach(() => {
        process.argv = originalArgv;
    });

    // Mock rationale: Simulates child process behavior without actually running external commands.
    const mockSpawn = (stdoutData, stderrData, exitCode) => {
        const mockChild = {
            stdout: { on: jest.fn((event, cb) => { if (event === 'data') cb(Buffer.from(stdoutData)); }) },
            stderr: { on: jest.fn((event, cb) => { if (event === 'data') cb(Buffer.from(stderrData)); }) },
            on: jest.fn((event, cb) => {
                if (event === 'close') cb(exitCode);
                if (event === 'error') {} // No error by default
            }),
        };
        spawn.mockReturnValue(mockChild);
    };

    // Mock rationale: Simulates file system operations without touching the actual disk.
    const mockFs = (fileContent = null) => {
        fs.readFileSync.mockReturnValue(fileContent);
        fs.writeFileSync.mockReturnValue(true);
    };

    it('should display usage if no mode is specified', async () => {
        process.argv = ['node', 'index.js'];
        require('../src/index'); // Load the script
        await new Promise(resolve => setTimeout(resolve, 10)); // Allow async operations to settle
        expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Usage:"));
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    describe('Capture Mode', () => {
        it('should capture command output and save to file', async () => {
            process.argv = ['node', 'index.js', '--capture', '--command', 'echo hello'];
            mockSpawn('hello from stdout', 'hello from stderr', 0);
            mockFs(); // No initial file content needed

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 100)); // Allow async operations to settle

            expect(spawn).toHaveBeenCalledWith('echo', ['hello'], { shell: true });
            expect(mockStdoutWrite).toHaveBeenCalledWith('hello from stdout');
            expect(mockStderrWrite).toHaveBeenCalledWith('hello from stderr');
            expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
            const writtenData = JSON.parse(fs.writeFileSync.mock.calls[0][1]);
            expect(writtenData.stdout).toBe('hello from stdout');
            expect(writtenData.stderr).toBe('hello from stderr');
            expect(writtenData.exitCode).toBe(0);
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Capture complete."));
            expect(mockExit).not.toHaveBeenCalled(); // Should not exit on success
        });

        it('should exit with error if --command is missing in capture mode', async () => {
            process.argv = ['node', 'index.js', '--capture'];
            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 10));
            expect(mockConsoleError).toHaveBeenCalledWith("Error: --command is required for capture mode.");
            expect(mockExit).toHaveBeenCalledWith(1);
        });
    });

    describe('Replay Mode', () => {
        const mockEchoData = {
            command: 'echo test',
            timestamp: new Date().toISOString(),
            stdout: 'replayed stdout',
            stderr: 'replayed stderr',
            exitCode: 0,
        };

        it('should replay captured output from file', async () => {
            process.argv = ['node', 'index.js', '--replay'];
            mockFs(JSON.stringify(mockEchoData));

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 100)); // Allow async operations to settle

            expect(fs.readFileSync).toHaveBeenCalledTimes(1);
            expect(mockStdoutWrite).toHaveBeenCalledWith('replayed stdout');
            expect(mockStderrWrite).toHaveBeenCalledWith('replayed stderr');
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Replay complete."));
            expect(mockExit).toHaveBeenCalledWith(0);
        });

        it('should apply delay during replay', async () => {
            process.argv = ['node', 'index.js', '--replay', '--delay', '50'];
            mockFs(JSON.stringify(mockEchoData));

            const startTime = Date.now();
            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 200)); // Wait longer than total delay

            const endTime = Date.now();
            // Expect at least 2 delays (stdout + stderr)
            expect(endTime - startTime).toBeGreaterThanOrEqual(100);
            expect(mockStdoutWrite).toHaveBeenCalledWith('replayed stdout');
            expect(mockStderrWrite).toHaveBeenCalledWith('replayed stderr');
            expect(mockExit).toHaveBeenCalledWith(0);
        });

        it('should apply character shift distortion', async () => {
            process.argv = ['node', 'index.js', '--replay', '--distort', 'shift'];
            mockFs(JSON.stringify({ ...mockEchoData, stdout: 'abc123XYZ' }));

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 100));

            // Due to randomness, we can't assert exact output, but we can check it's not identical
            const output = mockStdoutWrite.mock.calls[0][0];
            expect(output).not.toBe('abc123XYZ');
            expect(output.length).toBe('abc123XYZ'.length); // Length should remain same
            expect(mockExit).toHaveBeenCalledWith(0);
        });

        it('should apply ghost echo distortion', async () => {
            process.argv = ['node', 'index.js', '--replay', '--distort', 'ghost'];
            mockFs(JSON.stringify(mockEchoData));

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 100));

            expect(mockStdoutWrite).toHaveBeenCalledWith(expect.stringContaining('replayed stdout\n[...a faint echo of the past whispers...]\n'));
            expect(mockExit).toHaveBeenCalledWith(0);
        });

        it('should exit with original exit code', async () => {
            process.argv = ['node', 'index.js', '--replay'];
            mockFs(JSON.stringify({ ...mockEchoData, exitCode: 127 }));

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 100));

            expect(mockExit).toHaveBeenCalledWith(127);
        });

        it('should handle file not found during replay', async () => {
            process.argv = ['node', 'index.js', '--replay', '--file', 'nonexistent.json'];
            fs.readFileSync.mockImplementation(() => {
                throw new Error('ENOENT: no such file or directory');
            });

            require('../src/index');
            await new Promise(resolve => setTimeout(resolve, 10));

            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining("Error during replay: ENOENT"));
            expect(mockExit).toHaveBeenCalledWith(1);
        });
    });
});
