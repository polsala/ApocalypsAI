import { getFortune, fortunes, printFortune } from '../src/main';
import assert from 'assert';

describe('Fortune Cookie Utility', () => {
  it('getFortune returns a known fortune', () => {
    // Mock Math.random to return 0.5
    const originalRandom = Math.random;
    Math.random = () => 0.5; // deterministic
    const fortune = getFortune();
    // 0.5 * 5 = 2.5 -> floor 2 -> index 2
    assert.strictEqual(fortune, fortunes[2]);
    Math.random = originalRandom;
  });

  it('printFortune outputs ASCII art', () => {
    const originalConsoleLog = console.log;
    const logs: string[] = [];
    console.log = (msg: string) => logs.push(msg);
    // Mock random
    const originalRandom = Math.random;
    Math.random = () => 0;
    printFortune();
    // Check that logs contain the ASCII art lines
    assert.ok(logs.some(line => line.includes('^__^')));
    assert.ok(logs.some(line => line.includes('(oo)')));
    Math.random = originalRandom;
    console.log = originalConsoleLog;
  });
});
