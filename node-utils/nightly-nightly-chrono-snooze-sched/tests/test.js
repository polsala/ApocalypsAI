const assert = require('assert');
const sinon = require('sinon');
const { getSnoozeDuration, formatDateTime, WHIMSICAL_MESSAGES, SNOOZE_TYPES, getRandomInt, main } = require('../src/index');

describe('Nightly Chrono-Snooze Scheduler', () => {

  let clock;
  let mathRandomStub;
  let consoleLogStub;
  let consoleErrorStub;
  let processExitStub;

  beforeEach(() => {
    // Mock rationale: Ensure deterministic time for calculations.
    clock = sinon.useFakeTimers(new Date('2023-10-27T10:00:00.000Z').getTime());
    // Mock rationale: Ensure deterministic random number for snooze duration and message selection.
    mathRandomStub = sinon.stub(Math, 'random');
    // Mock rationale: Capture console output for verification without polluting test runner output.
    consoleLogStub = sinon.stub(console, 'log');
    // Mock rationale: Capture console error output for verification.
    consoleErrorStub = sinon.stub(console, 'error');
    // Mock rationale: Prevent process from exiting during tests.
    processExitStub = sinon.stub(process, 'exit');
  });

  afterEach(() => {
    clock.restore();
    mathRandomStub.restore();
    consoleLogStub.restore();
    consoleErrorStub.restore();
    processExitStub.restore();
  });

  it('should calculate power snooze duration correctly (default 20 min)', () => {
    mathRandomStub.returns(0); // Will pick the lowest value in range
    const duration = getSnoozeDuration('power');
    assert.strictEqual(duration, SNOOZE_TYPES.power.min);
  });

  it('should calculate light snooze duration correctly (default 45 min)', () => {
    mathRandomStub.returns(0); // Will pick the lowest value in range
    const duration = getSnoozeDuration('light');
    assert.strictEqual(duration, SNOOZE_TYPES.light.min);
  });

  it('should calculate full snooze duration correctly (default 90 min)', () => {
    mathRandomStub.returns(0); // Will pick the lowest value in range
    const duration = getSnoozeDuration('full');
    assert.strictEqual(duration, SNOOZE_TYPES.full.min);
  });

  it('should calculate custom snooze duration correctly', () => {
    const duration = getSnoozeDuration(null, 30);
    assert.strictEqual(duration, 30);
  });

  it('should throw error for invalid custom duration', () => {
    assert.throws(() => getSnoozeDuration(null, 'abc'), /Custom duration must be a positive number/);
    assert.throws(() => getSnoozeDuration(null, 0), /Custom duration must be a positive number/);
    assert.throws(() => getSnoozeDuration(null, -10), /Custom duration must be a positive number/);
  });

  it('should throw error for invalid snooze type', () => {
    assert.throws(() => getSnoozeDuration('invalid-type'), /Invalid snooze type/);
  });

  it('should format date and time correctly', () => {
    const date = new Date('2023-01-01T09:05:03.123Z');
    assert.strictEqual(formatDateTime(date), '2023-01-01 09:05:03');
  });

  it('should return a random integer within range', () => {
    mathRandomStub.returns(0.5);
    const result = getRandomInt(10, 20);
    assert.strictEqual(result, 15);

    mathRandomStub.returns(0.0);
    const resultMin = getRandomInt(10, 20);
    assert.strictEqual(resultMin, 10);

    mathRandomStub.returns(0.9999999999999999);
    const resultMax = getRandomInt(10, 20);
    assert.strictEqual(resultMax, 20);
  });

  it('main function should calculate wake-up time correctly for power nap', () => {
    mathRandomStub.returns(0); // Ensures 20 min for power nap and first message
    main({ type: 'power' }); // Call main with mocked argv

    assert.ok(consoleLogStub.calledWithMatch('Initiating a power Chrono-Snooze...'));
    assert.ok(consoleLogStub.calledWithMatch('Current time: 2023-10-27 10:00:00'));
    assert.ok(consoleLogStub.calledWithMatch('Wake-up time: 2023-10-27 10:20:00'));
    assert.ok(consoleLogStub.calledWithMatch(`Message: ${WHIMSICAL_MESSAGES[0]}`));
  });

  it('main function should calculate wake-up time correctly for custom duration', () => {
    mathRandomStub.returns(0); // Ensures first message
    main({ duration: '40' }); // Call main with mocked argv

    assert.ok(consoleLogStub.calledWithMatch('Initiating a Custom Chrono-Snooze (40 minutes)...'));
    assert.ok(consoleLogStub.calledWithMatch('Current time: 2023-10-27 10:00:00'));
    assert.ok(consoleLogStub.calledWithMatch('Wake-up time: 2023-10-27 10:40:00'));
    assert.ok(consoleLogStub.calledWithMatch(`Message: ${WHIMSICAL_MESSAGES[0]}`));
  });

  it('main function should handle errors gracefully for invalid duration argument', () => {
    main({ duration: 'invalid' }); // Call main with mocked argv

    assert.ok(consoleErrorStub.calledWithMatch('Error: Custom duration must be a positive number of minutes.'));
    assert.ok(processExitStub.calledWith(1));
  });
});
