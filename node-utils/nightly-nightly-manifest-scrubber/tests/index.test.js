const { scrubFileContent } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to test file system operations (read/write)
// without actually touching the disk during unit tests. This ensures
// tests are deterministic, fast, and don't leave artifacts.
jest.mock('fs', () => ({
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
}));

describe('scrubFileContent', () => {
    const mockFilePath = '/tmp/test_config.txt';
    const mockOutputFilePath = '/tmp/output_config.txt';

    beforeEach(() => {
        fs.readFileSync.mockClear();
        fs.writeFileSync.mockClear();
    });

    test('should remove comments and empty lines by default', () => {
        const content = `\n# This is a comment\nKEY1=value1\n\n// Another comment\nKEY2=value2\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath);
        expect(scrubbed).toBe('KEY1=value1\nKEY2=value2');
        expect(fs.readFileSync).toHaveBeenCalledWith(mockFilePath, 'utf8');
        expect(fs.writeFileSync).not.toHaveBeenCalled();
    });

    test('should keep comments if removeComments is false', () => {
        const content = `\n# This is a comment\nKEY1=value1\n// Another comment\nKEY2=value2\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, { removeComments: false });
        expect(scrubbed).toBe('# This is a comment\nKEY1=value1\n// Another comment\nKEY2=value2');
    });

    test('should keep empty lines if removeEmptyLines is false', () => {
        const content = `\nKEY1=value1\n\nKEY2=value2\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, { removeEmptyLines: false });
        expect(scrubbed).toBe('\nKEY1=value1\n\nKEY2=value2');
    });

    test('should redact specified patterns', () => {
        const content = `\nAPI_KEY=supersecretkey123\nDATABASE_URL=postgres://user:pass@host:port/db\nUSER_TOKEN=abc-123-def\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, {
            redactPatterns: ['API_KEY=.*', 'USER_TOKEN=.*']
        });
        expect(scrubbed).toBe('[REDACTED]\nDATABASE_URL=postgres://user:pass@host:port/db\n[REDACTED]');
    });

    test('should use custom redaction placeholder', () => {
        const content = `API_KEY=supersecretkey123`;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, {
            redactPatterns: ['API_KEY=.*'],
            redactionPlaceholder: '***HIDDEN***'
        });
        expect(scrubbed).toBe('***HIDDEN***');
    });

    test('should write to output file if specified', () => {
        const content = `KEY1=value1\n#comment`;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, { outputFile: mockOutputFilePath });
        expect(scrubbed).toBe('KEY1=value1'); // Still returns the content
        expect(fs.writeFileSync).toHaveBeenCalledWith(mockOutputFilePath, 'KEY1=value1', 'utf8');
    });

    test('should handle file read errors', () => {
        fs.readFileSync.mockImplementation(() => {
            throw new Error('File not found');
        });

        expect(() => scrubFileContent(mockFilePath)).toThrow('Failed to read file /tmp/test_config.txt: File not found');
    });

    test('should handle file write errors', () => {
        const content = `KEY1=value1`;
        fs.readFileSync.mockReturnValue(content);
        fs.writeFileSync.mockImplementation(() => {
            throw new Error('Permission denied');
        });

        expect(() => scrubFileContent(mockFilePath, { outputFile: mockOutputFilePath })).toThrow('Failed to write to output file /tmp/output_config.txt: Permission denied');
    });

    test('should handle mixed options correctly', () => {
        const content = `\n# This is a comment\nAPI_KEY=secret123\n\nKEY1=value1\n// Another comment\nPASSWORD=supersecret\n\nKEY2=value2\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, {
            removeComments: true,
            removeEmptyLines: false, // Keep empty lines
            redactPatterns: ['API_KEY=.*', 'PASSWORD=.*'],
            redactionPlaceholder: '[[REDACTED]]'
        });
        expect(scrubbed).toBe('[[REDACTED]]\n\nKEY1=value1\n\n[[REDACTED]]\n\nKEY2=value2');
    });

    test('should handle no scrubbing options (only redaction if specified)', () => {
        const content = `\n# Comment\nKEY=value\n        `;
        fs.readFileSync.mockReturnValue(content);

        const scrubbed = scrubFileContent(mockFilePath, {
            removeComments: false,
            removeEmptyLines: false,
            redactPatterns: [],
        });
        expect(scrubbed).toBe('\n# Comment\nKEY=value');
    });

    test('should handle invalid regex patterns gracefully', () => {
        const content = `KEY=value`;
        fs.readFileSync.mockReturnValue(content);
        const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

        const scrubbed = scrubFileContent(mockFilePath, {
            redactPatterns: ['[invalid-regex'],
        });
        expect(scrubbed).toBe('KEY=value');
        expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Warning: Invalid regex pattern'));
        consoleWarnSpy.mockRestore();
    });
});
