import * as fs from 'fs';
import * as path from 'path';
import { main as runMain } from '../src/index'; // Import main for testing

// Mock rationale: To ensure deterministic tests, file system operations (reading/writing ration data) are mocked.
// Date-related calculations are tested by injecting specific dates or by mocking `Date.now()` to control the "current" time.
jest.mock('fs');
const mockFs = fs as jest.Mocked<typeof fs>;

describe('Nightly Temporal Ration Rot Reporter', () => {
    let consoleSpy: jest.SpyInstance;
    let exitSpy: jest.SpyInstance;
    let mockDate: Date;

    beforeEach(() => {
        consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock error too
        exitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });

        // Set a fixed current date for deterministic tests
        mockDate = new Date('2024-07-20T12:00:00.000Z');
        jest.spyOn(global, 'Date').mockImplementation((dateString?: string | number | Date) => {
            if (dateString) {
                return new Date(dateString);
            }
            return mockDate;
        }) as jest.Mock;

        mockFs.existsSync.mockReturnValue(false);
        mockFs.readFileSync.mockReturnValue('[]');
        mockFs.writeFileSync.mockClear();
    });

    afterEach(() => {
        consoleSpy.mockRestore();
        exitSpy.mockRestore();
        jest.restoreAllMocks(); // Restore Date mock
    });

    it('should add a ration item correctly', () => {
        runMain(['node', 'index.js', 'add', 'Survival Biscuits', '2024-12-31', '10']);

        expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1);
        const writtenData = JSON.parse(mockFs.writeFileSync.mock.calls[0][1] as string);
        expect(writtenData).toEqual([{ name: 'Survival Biscuits', expiryDate: '2024-12-31', quantity: 10 }]);
        expect(consoleSpy).toHaveBeenCalledWith('Added "Survival Biscuits" (x10) expiring on 2024-12-31.');
    });

    it('should report rations with correct rot levels', () => {
        const rations = [
            { name: 'Fresh Apples', expiryDate: '2024-08-01', quantity: 3 }, // 12 days left
            { name: 'Canned Beans', expiryDate: '2025-07-20', quantity: 12 }, // 365 days left
            { name: 'Mystery Meat', expiryDate: '2024-07-22', quantity: 1 }, // 2 days left
            { name: 'Ancient Jerky', expiryDate: '2024-07-19', quantity: 5 } // -1 day (expired)
        ];
        mockFs.existsSync.mockReturnValue(true);
        mockFs.readFileSync.mockReturnValue(JSON.stringify(rations));

        runMain(['node', 'index.js', 'report']);

        expect(consoleSpy).toHaveBeenCalledWith('--- Ration Rot Report (Current Date: 2024-07-20) ---');
        expect(consoleSpy).toHaveBeenCalledWith('[Biohazard!] Ancient Jerky (x5) - Expires: 2024-07-19 (EXPIRED!)');
        expect(consoleSpy).toHaveBeenCalledWith('[Impending Doom!] Mystery Meat (x1) - Expires: 2024-07-22 (2 days left)');
        expect(consoleSpy).toHaveBeenCalledWith('[Slightly Wilted] Fresh Apples (x3) - Expires: 2024-08-01 (12 days left)');
        expect(consoleSpy).toHaveBeenCalledWith('[Fresh as a Daisy] Canned Beans (x12) - Expires: 2025-07-20 (365 days left)');
    });

    it('should handle no rations when reporting', () => {
        mockFs.existsSync.mockReturnValue(false); // No rations.json
        runMain(['node', 'index.js', 'report']);
        expect(consoleSpy).toHaveBeenCalledWith('--- Ration Rot Report (Current Date: 2024-07-20) ---');
        expect(consoleSpy).toHaveBeenCalledWith("No rations tracked yet. Add some with 'add' command!");
    });

    it('should exit with error for invalid add command arguments', () => {
        expect(() => runMain(['node', 'index.js', 'add', 'Item', '2024-12-31'])).toThrow('process.exit: 1');
        expect(console.error).toHaveBeenCalledWith("Usage: add <name> <YYYY-MM-DD> <quantity>");
    });

    it('should exit with error for invalid expiry date format', () => {
        expect(() => runMain(['node', 'index.js', 'add', 'Item', '12-31-2024', '1'])).toThrow('process.exit: 1');
        expect(console.error).toHaveBeenCalledWith("Error: Expiry date must be in YYYY-MM-DD format.");
    });

    it('should exit with error for unknown command', () => {
        expect(() => runMain(['node', 'index.js', 'unknown-command'])).toThrow('process.exit: 1');
        expect(console.log).toHaveBeenCalledWith("Usage: node dist/index.js <command>");
    });
});
