const assert = require('assert');
const path = require('path');
const fs = require('fs').promises;
const { getRandomTip, fetchTip, readCache, writeCache, getTip } = require('../src/main.js');

async function mockFetch(response) {
  global.fetch = async () => ({
    ok: true,
    json: async () => response
  });
}

async function restoreFetch() {
  delete global.fetch;
}

async function mockFs(readContent, writeCallback) {
  const originalReadFile = fs.readFile;
  const originalWriteFile = fs.writeFile;
  fs.readFile = async (file, encoding) => {
    if (file.includes('.apocalypse_tip_cache')) {
      if (readContent === null) throw new Error('ENOENT');
      return readContent;
    }
    return originalReadFile(file, encoding);
  };
  fs.writeFile = async (file, data, encoding) => {
    if (file.includes('.apocalypse_tip_cache')) {
      writeCallback(data);
      return;
    }
    return originalWriteFile(file, data, encoding);
  };
  return () => {
    fs.readFile = originalReadFile;
    fs.writeFile = originalWriteFile;
  };
}

(async () => {
  // Test random local tip
  const tip = await getRandomTip();
  assert.ok(tip, 'Tip should not be empty');

  // Test fetchTip with mock
  await mockFetch({ slip: { advice: 'Mocked advice' } });
  const apiTip = await fetchTip();
  assert.strictEqual(apiTip, 'Mocked advice', 'Should return mocked advice');
  await restoreFetch();

  // Test caching
  let writtenData = null;
  const restoreFs = await mockFs(null, (data) => { writtenData = data; });
  await writeCache('Cached tip');
  const parsed = JSON.parse(writtenData);
  assert.strictEqual(parsed.tip, 'Cached tip', 'Cache should contain the tip');
  restoreFs();

  // Test getTip with cache hit
  const restoreFs2 = await mockFs(JSON.stringify({ tip: 'Cached tip', timestamp: Date.now() }), () => {});
  const cachedTip = await getTip();
  assert.strictEqual(cachedTip, 'Cached tip', 'Should return cached tip');
  restoreFs2();

  // Test getTip with API
  await mockFetch({ slip: { advice: 'API tip' } });
  const apiFetchedTip = await getTip({ useApi: true });
  assert.strictEqual(apiFetchedTip, 'API tip', 'Should fetch from API');
  await restoreFetch();

  console.log('All tests passed');
})();
