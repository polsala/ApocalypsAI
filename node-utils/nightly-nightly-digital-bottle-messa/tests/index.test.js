const { bottleMessage, uncorkMessage, BOTTLES_DIR } = require('../src/index');
const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid'); // To mock uuid

// Mock rationale: We need to control file system operations and UUID generation
// to ensure tests are deterministic and don't create actual files or rely on random IDs.
jest.mock('fs');
jest.mock('uuid', () => ({
  v4: jest.fn(),
}));

describe('Digital Message in a Bottle Utility', () => {
  const mockMessage = 'Hello, future! This is a test message.';
  const mockBottleId = 'test-bottle-123';
  const mockTimestamp = '2023-10-27T10:00:00.000Z';
  const encodedMockMessage = Buffer.from(mockMessage).toString('base64');

  beforeEach(() => {
    // Reset mocks before each test
    fs.existsSync.mockReturnValue(true); // Assume bottles dir exists for most tests
    fs.mkdirSync.mockClear();
    fs.writeFileSync.mockClear();
    fs.readFileSync.mockClear();
    uuidv4.mockReturnValue(mockBottleId);
    jest.spyOn(Date.prototype, 'toISOString').mockReturnValue(mockTimestamp);
    jest.spyOn(console, 'log').mockImplementation(() => {}); // Suppress console.log
    jest.spyOn(console, 'error').mockImplementation(() => {}); // Suppress console.error
    jest.spyOn(process, 'exit').mockImplementation(() => { throw new Error('process.exit was called'); }); // Mock process.exit to prevent actual exit
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore console.log, error, and process.exit
  });

  test('bottleMessage should create a bottle file with correct content', () => {
    const expectedFilename = path.join(BOTTLES_DIR, `bottle-${mockBottleId}.json`);
    const expectedBottleContent = JSON.stringify({
      id: mockBottleId,
      timestamp: mockTimestamp,
      encodedMessage: encodedMockMessage,
      originalLength: mockMessage.length,
      encoding: 'base64',
    }, null, 2);

    const result = bottleMessage(mockMessage);

    expect(fs.writeFileSync).toHaveBeenCalledTimes(1);
    expect(fs.writeFileSync).toHaveBeenCalledWith(expectedFilename, expectedBottleContent, 'utf8');
    expect(result).toEqual({ id: mockBottleId, filename: expectedFilename });
    expect(console.log).toHaveBeenCalledWith(`Message bottled! ID: ${mockBottleId}`);
    expect(console.log).toHaveBeenCalledWith(`File: ${expectedFilename}`);
  });

  test('uncorkMessage should retrieve and decode a message from a bottle ID', () => {
    const bottleFilename = path.join(BOTTLES_DIR, `bottle-${mockBottleId}.json`);
    const mockBottleContent = JSON.stringify({
      id: mockBottleId,
      timestamp: mockTimestamp,
      encodedMessage: encodedMockMessage,
      originalLength: mockMessage.length,
      encoding: 'base64',
    });

    fs.readFileSync.mockReturnValue(mockBottleContent);

    const result = uncorkMessage(mockBottleId);

    expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    expect(fs.readFileSync).toHaveBeenCalledWith(bottleFilename, 'utf8');
    expect(result).toEqual({ id: mockBottleId, message: mockMessage });
    expect(console.log).toHaveBeenCalledWith('--- Uncorked Message ---');
    expect(console.log).toHaveBeenCalledWith(`ID: ${mockBottleId}`);
    expect(console.log).toHaveBeenCalledWith(mockMessage);
  });

  test('uncorkMessage should retrieve and decode a message from a full file path', () => {
    const customBottlePath = '/tmp/my-custom-bottle.json';
    const mockBottleContent = JSON.stringify({
      id: 'custom-id-456',
      timestamp: mockTimestamp,
      encodedMessage: encodedMockMessage,
      originalLength: mockMessage.length,
      encoding: 'base64',
    });

    fs.existsSync.mockImplementation((p) => p === customBottlePath); // Mock only for this specific path
    fs.readFileSync.mockReturnValue(mockBottleContent);

    const result = uncorkMessage(customBottlePath);

    expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    expect(fs.readFileSync).toHaveBeenCalledWith(customBottlePath, 'utf8');
    expect(result).toEqual({ id: 'custom-id-456', message: mockMessage });
  });

  test('uncorkMessage should handle bottle not found error', () => {
    fs.existsSync.mockReturnValue(false); // Bottle does not exist

    expect(() => uncorkMessage('non-existent-bottle')).toThrow('process.exit was called');
    expect(console.error).toHaveBeenCalledWith("Error: Bottle 'non-existent-bottle' not found.");
  });

  test('bottles directory is created if it does not exist', () => {
    fs.existsSync.mockReturnValueOnce(false); // First call for BOTTLES_DIR should return false
    fs.existsSync.mockReturnValue(true); // Subsequent calls for bottle files should return true
    fs.mkdirSync.mockClear(); // Clear any calls from initial setup of the test suite

    // Re-require the module to trigger the directory check logic again
    jest.resetModules();
    const { bottleMessage: newBottleMessage, BOTTLES_DIR: newBOTTLES_DIR } = require('../src/index');
    newBottleMessage(mockMessage);

    expect(fs.mkdirSync).toHaveBeenCalledTimes(1);
    expect(fs.mkdirSync).toHaveBeenCalledWith(newBOTTLES_DIR, { recursive: true });
  });
});
