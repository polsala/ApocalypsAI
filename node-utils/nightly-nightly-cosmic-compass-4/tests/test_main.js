const assert = require('assert');
const sinon = require('sinon');

// Mock the Date object to control time
let clock;

// Mock the crypto module to control hash output
let cryptoStub;

// Load the module to be tested
let getCosmicDirection;

describe('Cosmic Compass', () => {
  beforeEach(() => {
    // Stub the Date constructor to return a fixed date and time
    clock = sinon.useFakeTimers({
      toFake: ['Date']
    });

    // Mock the crypto module
    cryptoStub = sinon.stub(require('crypto'), 'createHash');

    // Dynamically require the module to ensure mocks are applied
    getCosmicDirection = require('../src/main').getCosmicDirection;
  });

  afterEach(() => {
    // Restore the original Date object and crypto module
    clock.restore();
    cryptoStub.restore();
    // Clear the require cache to ensure the module is reloaded with fresh mocks on next test
    delete require.cache[require.resolve('../src/main')];
  });

  it('should return North for a specific time and event hash', () => {
    // Mock Date to return a specific time
    const fixedDate = new Date(2023, 10, 20, 10, 30, 0); // Nov 20, 2023, 10:30:00
    clock.setSystemTime(fixedDate.getTime());

    // Mock crypto.createHash to return a predictable hash value
    // This hash, when converted to an angle, should fall into the 'North' range.
    // For example, a hash that results in an angle of ~10 degrees.
    const mockHash = 'a1b2c3d4e5f678901234567890abcdef'; // Example hash
    cryptoStub.returns({
      update: sinon.stub().returnsThis(),
      digest: sinon.stub().returns(mockHash)
    });

    const cosmicEvent = 'Meteor Shower';
    const result = getCosmicDirection(cosmicEvent);

    // Based on the mock hash and time, we expect 'North'
    assert.strictEqual(result.direction, 'North', 'Expected direction to be North');
    assert.ok(result.description.includes('stardust whispers secrets'), 'Expected a North-related description');
  });

  it('should return South-East for a different time and event hash', () => {
    // Mock Date to return a different specific time
    const fixedDate = new Date(2024, 0, 1, 18, 0, 0); // Jan 1, 2024, 18:00:00
    clock.setSystemTime(fixedDate.getTime());

    // Mock crypto.createHash to return a different predictable hash value
    // This hash should result in an angle in the 'South-East' range (112.5 to 157.5 degrees).
    // For example, a hash that results in an angle of ~135 degrees.
    const mockHash = 'f0e1d2c3b4a567890123456789abcdef'; // Example hash
    cryptoStub.returns({
      update: sinon.stub().returnsThis(),
      digest: sinon.stub().returns(mockHash)
    });

    const cosmicEvent = 'Binary Star Merger';
    const result = getCosmicDirection(cosmicEvent);

    // Based on the mock hash and time, we expect 'South-East'
    assert.strictEqual(result.direction, 'South-East', 'Expected direction to be South-East');
    assert.ok(result.description.includes('ancient cosmic knowledge'), 'Expected a South-East-related description');
  });

  it('should return West for another time and event hash', () => {
    // Mock Date to return a different specific time
    const fixedDate = new Date(2025, 5, 15, 2, 45, 30); // Jun 15, 2025, 02:45:30
    clock.setSystemTime(fixedDate.getTime());

    // Mock crypto.createHash to return a different predictable hash value
    // This hash should result in an angle in the 'West' range (247.5 to 292.5 degrees).
    // For example, a hash that results in an angle of ~270 degrees.
    const mockHash = '1234567890abcdef0123456789abcdef'; // Example hash
    cryptoStub.returns({
      update: sinon.stub().returnsThis(),
      digest: sinon.stub().returns(mockHash)
    });

    const cosmicEvent = 'Nebula Formation';
    const result = getCosmicDirection(cosmicEvent);

    // Based on the mock hash and time, we expect 'West'
    assert.strictEqual(result.direction, 'West', 'Expected direction to be West');
    assert.ok(result.description.includes('understanding dawns'), 'Expected a West-related description');
  });

  // Test case for when no cosmic event is provided
  it('should exit with an error if no cosmic event is provided', () => {
    // Mock process.exit to prevent actual exit and check if it's called
    const exitStub = sinon.stub(process, 'exit');
    const errorSpy = sinon.spy(console, 'error');

    // Temporarily remove the argument to simulate no input
    const originalArgv = process.argv;
    process.argv = [process.argv[0], process.argv[1]]; // Only node and script path

    // Re-require the module to pick up the modified process.argv
    delete require.cache[require.resolve('../src/main')];
    getCosmicDirection = require('../src/main').getCosmicDirection;

    // Call the function (it will try to access process.argv[2])
    // We expect it to throw or call process.exit
    try {
      getCosmicDirection();
    } catch (e) {
      // If it throws, we catch it. If it calls process.exit, the stub will catch it.
    }

    assert.ok(exitStub.calledWith(1), 'Expected process.exit(1) to be called');
    assert.ok(errorSpy.calledWith(sinon.match(/Error: Please provide a cosmic event/)), 'Expected an error message to be logged');

    // Restore mocks and original argv
    exitStub.restore();
    errorSpy.restore();
    process.argv = originalArgv;
  });
});
