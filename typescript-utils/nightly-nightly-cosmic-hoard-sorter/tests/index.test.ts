import { classifyContent, CosmicElement, processInput, runCli } from '../src/index';
import * as fs from 'fs'; // # Mock rationale: fs is a core Node.js module for file system operations. Mocking it ensures tests are deterministic and don't rely on actual file system state.
import * as path from 'path'; // # Mock rationale: path is a core Node.js module. Mocking it ensures consistent path resolution across different environments and prevents reliance on actual file system structure.

// Mock fs and path for deterministic tests
jest.mock('fs', () => ({
    existsSync: jest.fn(),
    lstatSync: jest.fn(() => ({ isFile: () => true })),
    promises: {
        readFile: jest.fn(),
    },
}));

jest.mock('path', () => ({
    resolve: jest.fn((...args) => args.join('/')), // Simple join for consistent paths
    // Add other path methods if needed by the utility
}));

describe('classifyContent', () => {
    it('should classify content as Stardust for planning keywords', () => {
        expect(classifyContent("I need to plan my next project.")).toBe(CosmicElement.Stardust);
        expect(classifyContent("Let's organize the tasks.")).toBe(CosmicElement.Stardust);
    });

    it('should classify content as Nebula for idea keywords', () => {
        expect(classifyContent("Brainstorming new features.")).toBe(CosmicElement.Nebula);
        expect(classifyContent("A concept for the future.")).toBe(CosmicElement.Nebula);
    });

    it('should classify content as Quasar for report keywords', () => {
        expect(classifyContent("Here is the quarterly report.")).toBe(CosmicElement.Quasar);
        expect(classifyContent("Data analysis results.")).toBe(CosmicElement.Quasar);
    });

    it('should classify content as Void for bug keywords', () => {
        expect(classifyContent("Found a critical bug in production.")).toBe(CosmicElement.Void);
        expect(classifyContent("Need to fix this issue.")).toBe(CosmicElement.Void);
    });

    it('should classify content as Comet Dust for archival keywords', () => {
        expect(classifyContent("Archive old documents.")).toBe(CosmicElement.CometDust);
        expect(classifyContent("Legacy system documentation.")).toBe(CosmicElement.CometDust);
    });

    it('should classify content as Singularity for urgent keywords', () => {
        expect(classifyContent("Urgent task: deploy now!")).toBe(CosmicElement.Singularity);
        expect(classifyContent("Deadline is tomorrow.")).toBe(CosmicElement.Singularity);
    });

    it('should classify content as Unknown for no matching keywords', () => {
        expect(classifyContent("This is some random text.")).toBe(CosmicElement.Unknown);
        expect(classifyContent("Hello world.")).toBe(CosmicElement.Unknown);
    });

    it('should be case-insensitive', () => {
        expect(classifyContent("PLANNING a trip")).toBe(CosmicElement.Stardust);
        expect(classifyContent("BUG report")).toBe(CosmicElement.Void);
    });
});

describe('processInput', () => {
    beforeEach(() => {
        // Reset mocks before each test
        (fs.existsSync as jest.Mock).mockClear();
        (fs.lstatSync as jest.Mock).mockClear();
        (fs.promises.readFile as jest.Mock).mockClear();
    });

    it('should process a file path and classify its content', async () => {
        const mockFilePath = 'test-file.txt';
        const mockFileContent = 'This is a test file with an idea.';
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.lstatSync as jest.Mock).mockReturnValue({ isFile: () => true });
        (fs.promises.readFile as jest.Mock).mockResolvedValue(mockFileContent);

        const result = await processInput(mockFilePath);
        expect(result.type).toBe('file');
        expect(result.content).toBe(mockFileContent);
        expect(result.element).toBe(CosmicElement.Nebula);
        expect(fs.existsSync).toHaveBeenCalledWith(mockFilePath);
        expect(fs.promises.readFile).toHaveBeenCalledWith(mockFilePath, 'utf8');
    });

    it('should process direct text input', async () => {
        const inputText = 'This is a direct text input about a bug.';
        (fs.existsSync as jest.Mock).mockReturnValue(false); // Simulate not a file
        
        const result = await processInput(inputText);
        expect(result.type).toBe('text');
        expect(result.content).toBe(inputText);
        expect(result.element).toBe(CosmicElement.Void);
        expect(fs.existsSync).toHaveBeenCalledWith(inputText);
        expect(fs.promises.readFile).not.toHaveBeenCalled();
    });

    it('should handle file not found gracefully (as text)', async () => {
        const nonExistentPath = 'non-existent-file.txt';
        (fs.existsSync as jest.Mock).mockReturnValue(false);

        const result = await processInput(nonExistentPath);
        expect(result.type).toBe('text');
        expect(result.content).toBe(nonExistentPath); // The input itself becomes the content
        expect(result.element).toBe(CosmicElement.Unknown); // Classifies the path string
    });
});

describe('runCli', () => {
    let consoleSpy: jest.SpyInstance;
    let processExitSpy: jest.SpyInstance;

    beforeEach(() => {
        consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        jest.spyOn(console, 'error').mockImplementation(() => {});
        // Mock process.exit to throw an error, allowing tests to catch it instead of terminating the test runner
        processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });
        
        // Reset mocks for fs and path
        (fs.existsSync as jest.Mock).mockClear();
        (fs.lstatSync as jest.Mock).mockClear();
        (fs.promises.readFile as jest.Mock).mockClear();
    });

    afterEach(() => {
        consoleSpy.mockRestore();
        (console.error as jest.Mock).mockRestore();
        processExitSpy.mockRestore();
    });

    it('should display usage if no input is provided', async () => {
        await runCli(['node', 'src/index.ts']);
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Usage:"));
        expect(processExitSpy).not.toHaveBeenCalled(); // Should not exit for just usage info
    });

    it('should process a file path and print classification', async () => {
        const mockFilePath = 'test-report.txt';
        const mockFileContent = 'This is a report with important data.';
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.lstatSync as jest.Mock).mockReturnValue({ isFile: () => true });
        (fs.promises.readFile as jest.Mock).mockResolvedValue(mockFileContent);

        await runCli(['node', 'src/index.ts', mockFilePath]);
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Input Type: File"));
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`Assigned Cosmic Element: ${CosmicElement.Quasar}`));
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Suggestion: Consider tagging this with \"quasar\""));
        expect(processExitSpy).not.toHaveBeenCalled();
    });

    it('should process direct text input and print classification', async () => {
        const inputText = 'An urgent bug fix is needed.';
        (fs.existsSync as jest.Mock).mockReturnValue(false);

        await runCli(['node', 'src/index.ts', inputText]);
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Input Type: Text Snippet"));
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining(`Assigned Cosmic Element: ${CosmicElement.Singularity}`));
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Suggestion: Consider tagging this with \"singularity\""));
        expect(processExitSpy).not.toHaveBeenCalled();
    });

    it('should handle errors during file processing', async () => {
        const mockFilePath = 'bad-file.txt';
        const errorMessage = 'Permission denied';
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.lstatSync as jest.Mock).mockReturnValue({ isFile: () => true });
        (fs.promises.readFile as jest.Mock).mockRejectedValue(new Error(errorMessage));

        // Expect the runCli to throw the mocked process.exit error
        await expect(runCli(['node', 'src/index.ts', mockFilePath])).rejects.toThrow('process.exit: 1');
        expect(console.error).toHaveBeenCalledWith(expect.stringContaining(`Error: ${errorMessage}`));
        expect(processExitSpy).toHaveBeenCalledWith(1);
    });
});
