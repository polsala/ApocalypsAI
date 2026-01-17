const assert = require('assert');
const { getRandomFortune, getFortunes } = require('../src/main');

describe('Fortune Cookie CLI', () => {
  it('should return a fortune from the list', () => {
    const fortunes = getFortunes();
    const fortune = getRandomFortune();
    assert.ok(fortunes.includes(fortune), 'Returned fortune should be in the list');
  });

  it('should print a fortune to stdout', () => {
    const originalLog = console.log;
    let logged = '';
    console.log = (msg) => { logged = msg; };
    const { main } = require('../src/main');
    main();
    console.log = originalLog;
    assert.ok(logged.length > 0, 'Should log something');
    assert.ok(getFortunes().includes(logged), 'Logged fortune should be in list');
  });
});
