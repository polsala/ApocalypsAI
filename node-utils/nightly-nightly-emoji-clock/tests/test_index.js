const assert = require('assert');
const { nearestClockEmoji, parseTime } = require('../src/index');

// --- Helper to mock Date globally ---
function withMockedDate(mockHour, mockMinute, fn) {
  const RealDate = Date;
  // Create a fake Date class that returns the mocked time when instantiated without args
  class MockDate extends RealDate {
    constructor(...args) {
      if (args.length === 0) {
        super();
        this.setHours(mockHour);
        this.setMinutes(mockMinute);
        this.setSeconds(0);
        this.setMilliseconds(0);
      } else {
        super(...args);
      }
    }
    static now() {
      return new RealDate(2020, 0, 1, mockHour, mockMinute, 0, 0).getTime();
    }
  }
  global.Date = MockDate;
  try {
    fn();
  } finally {
    global.Date = RealDate; // restore original Date
  }
}

// --- parseTime tests ---
assert.deepStrictEqual(parseTime('09:30'), { hour: 9, minute: 30 });
assert.throws(() => parseTime('25:00'), /Invalid hour/);
assert.throws(() => parseTime('12:60'), /Invalid minute/);
assert.throws(() => parseTime('bad'), /Invalid time format/);

// --- nearestClockEmoji with explicit times ---
assert.strictEqual(nearestClockEmoji('00:00'), '🕛'); // midnight -> 12
assert.strictEqual(nearestClockEmoji('03:15'), '🕒'); // rounds down to 3
assert.strictEqual(nearestClockEmoji('03:45'), '🕓'); // rounds up to 4
assert.strictEqual(nearestClockEmoji('12:30'), '🕐'); // 12:30 rounds up to 1
assert.strictEqual(nearestClockEmoji('23:59'), '🕛'); // 23:59 rounds up to 12

// --- nearestClockEmoji without argument (uses current time) ---
withMockedDate(14, 20, () => {
  // 14:20 -> 2:20 PM -> nearest hour 2
  assert.strictEqual(nearestClockEmoji(), '🕑');
});

withMockedDate(14, 40, () => {
  // 14:40 -> rounds up to 3
  assert.strictEqual(nearestClockEmoji(), '🕒');
});

// If we reach this point, all tests passed.
process.exit(0);
