const { purifyText, main } = require('../src/index');
const fs = require('fs').promises; // Mock this

// Mock rationale: We need to control file system interactions to ensure tests are
// deterministic, fast, and don't rely on actual file creation/deletion.
// This allows us to simulate various file contents without side effects.
jest.mock('fs', () => ({
    promises: {
        readFile: jest.fn(),
        writeFile: jest.fn(),
    },
}));

// Mock rationale: We need to control process.exit to prevent tests from terminating
// prematurely and to assert that the correct exit code is called.
const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});
// Mock rationale: We need to capture console output to assert that the utility
// prints the correct messages or purified content when no output file is specified.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('purifyText', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should trim whitespace from each line', () => {
        const input = '  line 1  \n\tline 2\t\nline 3   ';
        const expected = 'line 1\nline 2\nline 3';
        expect(purifyText(input)).toBe(expected);
    });

    test('should reduce multiple empty lines to a single empty line', () => {
        const input = 'line 1\n\n\nline 2\n\n\n\nline 3';
        const expected = 'line 1\n\nline 2\n\nline 3';
        expect(purifyText(input)).toBe(expected);
    });

    test('should handle content with leading/trailing empty lines', () => {
        const input = '\n\n  line 1  \n\n\nline 2\n\n';
        const expected = '\nline 1\n\nline 2\n'; // Leading/trailing empty lines are preserved as single ones
        expect(purifyText(input)).toBe(expected);
    });

    test('should remove non-printable ASCII characters', () => {
        const input = 'line\x01with\x07control\x1Fchars\x7Fand\x9Fmore';
        const expected = 'linewithcontrolcharsandmore';
        expect(purifyText(input)).toBe(expected);
    });

    test('should handle a mix of all purification types', () => {
        const input = '  Hello World!  \n\n\n\x00This is a test.\x08\n  Another line.  \n\n';
        const expected = 'Hello World!\n\nThis is a test.\nAnother line.\n';
        expect(purifyText(input)).toBe(expected);
    });

    test('should return an empty string for an empty input string', () => {
        expect(purifyText('')).toBe('');
    });

    test('should return an empty string for input with only empty lines/whitespace', () => {
        const input = '   \n\n\t\n  \n';
        expect(purifyText(input)).toBe(''); // All lines become empty, then reduced to one, then trimmed.
    });

    test('should handle content with only non-printable characters', () => {
        const input = '\x01\x02\x03\x04';
        expect(purifyText(input)).toBe('');
    });
});

describe('main', () => {
    const mockInputPath = 'input.txt';
    const mockOutputPath = 'output.txt';
    const mockRawContent = '  test content  \n\n\n\x01with dust\n';
    const mockPurifiedContent = 'test content\n\nwith dust';

    beforeEach(() => {
        jest.clearAllMocks();
        // Reset process.argv for each test
        process.argv = ['node', 'src/index.js'];
    });

    test('should read from input file and print to stdout if no output file is given', async () => {
        process.argv.push(mockInputPath);
        fs.promises.readFile.mockResolvedValue(mockRawContent);

        await main();

        expect(fs.promises.readFile).toHaveBeenCalledWith(mockInputPath, 'utf8');
        expect(fs.promises.writeFile).not.toHaveBeenCalled();
        expect(mockConsoleLog).toHaveBeenCalledWith(mockPurifiedContent);
        expect(mockConsoleError).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should read from input file and write to output file if given', async () => {
        process.argv.push(mockInputPath, mockOutputPath);
        fs.promises.readFile.mockResolvedValue(mockRawContent);

        await main();

        expect(fs.promises.readFile).toHaveBeenCalledWith(mockInputPath, 'utf8');
        expect(fs.promises.writeFile).toHaveBeenCalledWith(mockOutputPath, mockPurifiedContent, 'utf8');
        expect(mockConsoleLog).toHaveBeenCalledWith(`Purified content saved to: ${mockOutputPath}`);
        expect(mockConsoleError).not.toHaveBeenCalled();
        expect(mockExit).not.toHaveBeenCalled();
    });

    test('should exit with error if too few arguments are provided', async () => {
        // No arguments provided
        await main();
        expect(mockConsoleError).toHaveBeenCalledWith('Usage: node src/index.js <input_file_path> [output_file_path]');
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    test('should exit with error if too many arguments are provided', async () => {
        process.argv.push(mockInputPath, mockOutputPath, 'extra_arg.txt');
        await main();
        expect(mockConsoleError).toHaveBeenCalledWith('Usage: node src/index.js <input_file_path> [output_file_path]');
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    test('should exit with error if input file cannot be read', async () => {
        process.argv.push(mockInputPath);
        const errorMessage = 'File not found';
        fs.promises.readFile.mockRejectedValue(new Error(errorMessage));

        await main();

        expect(fs.promises.readFile).toHaveBeenCalledWith(mockInputPath, 'utf8');
        expect(mockConsoleError).toHaveBeenCalledWith(`Error purifying file: ${errorMessage}`);
        expect(mockExit).toHaveBeenCalledWith(1);
    });

    test('should exit with error if output file cannot be written', async () => {
        process.argv.push(mockInputPath, mockOutputPath);
        const errorMessage = 'Permission denied';
        fs.promises.readFile.mockResolvedValue(mockRawContent);
        fs.promises.writeFile.mockRejectedValue(new Error(errorMessage));

        await main();

        expect(fs.promises.readFile).toHaveBeenCalledWith(mockInputPath, 'utf8');
        expect(fs.promises.writeFile).toHaveBeenCalledWith(mockOutputPath, mockPurifiedContent, 'utf8');
        expect(mockConsoleError).toHaveBeenCalledWith(`Error purifying file: ${errorMessage}`);
        expect(mockExit).toHaveBeenCalledWith(1);
    });
});
