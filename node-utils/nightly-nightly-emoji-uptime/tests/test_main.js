const assert = require('assert');
const { getUptimeMessage } = require('../src/main');

function runTests() {
  let passed = 0;
  let failed = 0;

  function test(name, fn) {
    try {
      fn();
      console.log(`â ${name}`);
      passed++;
    } catch (err) {
      console.error(`â ${name}`);
      console.error(err);
      failed++;
    }
  }

  test('formats 90061 seconds correctly', () => {
    const msg = getUptimeMessage(90061); // 1 day 1 hour 1 minute 1 second
    assert.strictEqual(msg, 'ð¢ Uptime: 1 day 1 hour 1 minute 1 second');
  });

  test('omits zero parts', () => {
    const msg = getUptimeMessage(60); // 1 minute
    assert.strictEqual(msg, 'ð¢ Uptime: 1 minute');
  });

  console.log(`
${passed} passed, ${failed} failed`);
  process.exit(failed ? 1 : 0);
}

runTests();
