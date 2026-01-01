const fs = require('fs');
const path = require('path');
const {
    loadMessages,
    saveMessages,
    isMessageExpired,
    cleanupMessages,
    postMessage,
    listMessages,
    main,
    DATA_FILE,
    DATA_DIR
} = require('../src/index');

// Mock rationale: We mock the 'fs' module to prevent actual file system operations
// during tests, ensuring determinism, speed, and isolation. This allows us to
// control the state of 'messages.json' in memory without touching the disk.
jest.mock('fs', () => ({
    ...jest.requireActual('fs'), // Import and retain default behavior for non-mocked functions
    existsSync: jest.fn(),
    mkdirSync: jest.fn(),
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
}));

// Mock rationale: We mock console.log and console.error to prevent test output
// pollution and to assert on the messages printed by the utility.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Nightly Ephemeral Message Board', () => {
    let mockMessages = [];

    beforeEach(() => {
        // Reset mocks and mock data before each test
        mockMessages = [];
        fs.existsSync.mockReturnValue(true); // Assume data dir and file exist by default
        fs.readFileSync.mockReturnValue(JSON.stringify(mockMessages));
        fs.writeFileSync.mockImplementation((filePath, data) => {
            mockMessages = JSON.parse(data);
        });
        fs.mkdirSync.mockClear();
        mockConsoleLog.mockClear();
        mockConsoleError.mockClear();

        // Mock rationale: Mock Date.now() to ensure deterministic timestamps for message creation
        // and expiry calculations, making tests reliable regardless of when they run.
        jest.spyOn(Date, 'now').mockReturnValue(1678886400000); // March 15, 2023 12:00:00 PM UTC
    });

    afterEach(() => {
        jest.restoreAllMocks(); // Restore Date.now() and console mocks to their original implementations
    });

    it('should create data directory if it does not exist', () => {
        fs.existsSync.mockReturnValueOnce(false); // First call for DATA_DIR
        fs.existsSync.mockReturnValue(false); // Second call for DATA_FILE (if loadMessages is called)
        // Re-require the module to trigger the initial check for DATA_DIR existence
        jest.resetModules();
        require('../src/index');
        expect(fs.mkdirSync).toHaveBeenCalledWith(DATA_DIR, { recursive: true });
    });

    it('loadMessages should return empty array if file does not exist', () => {
        fs.existsSync.mockReturnValueOnce(false); // For DATA_FILE
        expect(loadMessages()).toEqual([]);
    });

    it('loadMessages should return parsed messages if file exists', () => {
        const testMessages = [{ id: '1', content: 'test' }];
        fs.readFileSync.mockReturnValue(JSON.stringify(testMessages));
        expect(loadMessages()).toEqual(testMessages);
    });

    it('saveMessages should write messages to file', () => {
        const testMessages = [{ id: '1', content: 'test' }];
        saveMessages(testMessages);
        expect(fs.writeFileSync).toHaveBeenCalledWith(DATA_FILE, JSON.stringify(testMessages, null, 2), 'utf8');
        expect(mockMessages).toEqual(testMessages);
    });

    describe('isMessageExpired', () => {
        it('should return false for a new message with no expiry', () => {
            const message = { timestamp: Date.now(), views: 0 };
            expect(isMessageExpired(message)).toBe(false);
        });

        it('should return true if TTL has passed', () => {
            // Message posted 5 minutes and 1 millisecond ago, with a 5-minute TTL
            const message = { timestamp: Date.now() - (60 * 1000 * 5) - 1, ttl: 5, views: 0 };
            expect(isMessageExpired(message)).toBe(true);
        });

        it('should return false if TTL has not passed', () => {
            // Message posted 4 minutes ago, with a 5-minute TTL
            const message = { timestamp: Date.now() - (60 * 1000 * 4), ttl: 5, views: 0 };
            expect(isMessageExpired(message)).toBe(false);
        });

        it('should return true if max views reached', () => {
            const message = { timestamp: Date.now(), maxViews: 2, views: 2 };
            expect(isMessageExpired(message)).toBe(true);
        });

        it('should return false if max views not reached', () => {
            const message = { timestamp: Date.now(), maxViews: 2, views: 1 };
            expect(isMessageExpired(message)).toBe(false);
        });

        it('should return true if both TTL and max views reached', () => {
            const message = {
                timestamp: Date.now() - (60 * 1000 * 5) - 1,
                ttl: 5,
                maxViews: 2,
                views: 2
            };
            expect(isMessageExpired(message)).toBe(true);
        });
    });

    it('cleanupMessages should remove expired messages', () => {
        const activeMsg = { id: '1', content: 'active', timestamp: Date.now(), ttl: 10, views: 0 };
        const expiredTtlMsg = { id: '2', content: 'expired ttl', timestamp: Date.now() - (60 * 1000 * 11), ttl: 10, views: 0 };
        const expiredViewsMsg = { id: '3', content: 'expired views', timestamp: Date.now(), maxViews: 1, views: 1 };

        const messages = [activeMsg, expiredTtlMsg, expiredViewsMsg];
        const cleaned = cleanupMessages(messages);
        expect(cleaned).toEqual([activeMsg]);
    });

    it('postMessage should add a new message and save it', () => {
        postMessage("Hello World", 5, 2);
        expect(mockMessages.length).toBe(1);
        expect(mockMessages[0]).toMatchObject({
            content: "Hello World",
            ttl: 5,
            maxViews: 2,
            views: 0,
            timestamp: Date.now()
        });
        expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
        expect(mockConsoleLog).toHaveBeenCalledWith("Message posted successfully.");
    });

    describe('listMessages', () => {
        it('should display "No active messages found." if none exist', () => {
            listMessages();
            expect(mockConsoleLog).toHaveBeenCalledWith("No active messages found.");
            expect(fs.writeFileSync).not.toHaveBeenCalled(); // No messages, no save
        });

        it('should display active messages and increment views', () => {
            const msg1 = { id: '1', content: 'Msg 1', timestamp: Date.now(), ttl: 10, views: 0 };
            const msg2 = { id: '2', content: 'Msg 2', timestamp: Date.now(), maxViews: 2, views: 0 };
            mockMessages = [msg1, msg2];
            fs.readFileSync.mockReturnValue(JSON.stringify(mockMessages));

            listMessages();

            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("--- Active Ephemeral Messages ---"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Content: Msg 1"));
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Content: Msg 2"));
            expect(mockMessages[0].views).toBe(1); // View count incremented
            expect(mockMessages[1].views).toBe(1); // View count incremented
            expect(fs.writeFileSync).toHaveBeenCalledTimes(1); // Saved updated views
        });

        it('should clean up expired messages before displaying', () => {
            const activeMsg = { id: '1', content: 'Active', timestamp: Date.now(), ttl: 10, views: 0 };
            const expiredMsg = { id: '2', content: 'Expired', timestamp: Date.now() - (60 * 1000 * 11), ttl: 10, views: 0 };
            mockMessages = [activeMsg, expiredMsg];
            fs.readFileSync.mockReturnValue(JSON.stringify(mockMessages));

            listMessages();

            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Content: Active"));
            expect(mockConsoleLog).not.toHaveBeenCalledWith(expect.stringContaining("Content: Expired"));
            expect(mockMessages.length).toBe(1); // Expired message removed
            expect(mockMessages[0].content).toBe('Active');
            expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
        });
    });

    describe('main CLI function', () => {
        // Mock rationale: We mock process.exit to prevent the test runner from exiting
        // prematurely when the CLI utility encounters an error or finishes its execution.
        const mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {});

        afterEach(() => {
            mockExit.mockClear();
        });

        it('should call postMessage for "post" command', () => {
            const postSpy = jest.spyOn(module.exports, 'postMessage').mockImplementation(() => {});
            main(['node', 'src/index.js', 'post', 'Test message', '--ttl', '10', '--max-views', '5']);
            expect(postSpy).toHaveBeenCalledWith('Test message', '10', '5');
            postSpy.mockRestore();
        });

        it('should call listMessages for "list" command', () => {
            const listSpy = jest.spyOn(module.exports, 'listMessages').mockImplementation(() => {});
            main(['node', 'src/index.js', 'list']);
            expect(listSpy).toHaveBeenCalled();
            listSpy.mockRestore();
        });

        it('should call cleanupMessages for "clean" command', () => {
            const msg1 = { id: '1', content: 'Active', timestamp: Date.now(), ttl: 10, views: 0 };
            const msg2 = { id: '2', content: 'Expired', timestamp: Date.now() - (60 * 1000 * 11), ttl: 10, views: 0 };
            mockMessages = [msg1, msg2];
            fs.readFileSync.mockReturnValue(JSON.stringify(mockMessages));

            main(['node', 'src/index.js', 'clean']);
            expect(mockMessages.length).toBe(1); // One message should be cleaned
            expect(mockConsoleLog).toHaveBeenCalledWith("Cleaned up 1 expired messages.");
            expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
        });

        it('should handle "clean" command with no expired messages', () => {
            const msg1 = { id: '1', content: 'Active', timestamp: Date.now(), ttl: 10, views: 0 };
            mockMessages = [msg1];
            fs.readFileSync.mockReturnValue(JSON.stringify(mockMessages));

            main(['node', 'src/index.js', 'clean']);
            expect(mockMessages.length).toBe(1); // No messages should be cleaned
            expect(mockConsoleLog).toHaveBeenCalledWith("No expired messages to clean up.");
            expect(fs.writeFileSync).not.toHaveBeenCalled(); // No save if nothing changed
        });

        it('should show usage and exit for unknown command', () => {
            main(['node', 'src/index.js', 'unknown-command']);
            expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining("Usage:"));
            expect(mockExit).toHaveBeenCalledWith(1);
        });

        it('should show error and exit if post command is missing content', () => {
            main(['node', 'src/index.js', 'post']);
            expect(mockConsoleError).toHaveBeenCalledWith(expect.stringContaining("Error: Message content is required"));
            expect(mockExit).toHaveBeenCalledWith(1);
        });
    });
});
