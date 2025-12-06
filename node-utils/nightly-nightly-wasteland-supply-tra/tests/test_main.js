const assert = require('assert');
const fs = require('fs');
const path = require('path');
const os = require('os');

const {
  addItem,
  removeItem,
  listItems,
  totalWeight,
  loadInventory,
  saveInventory
} = require('../src/main.js');

// Helper to create a temporary inventory file
function withTempInventory(callback) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'supply-tracker-'));
  const invPath = path.join(tmpDir, 'inventory.json');
  try {
    callback(invPath);
  } finally {
    // Cleanup
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  }
}

// Mock rationale: using a temporary file ensures tests are deterministic and do not touch real data.
withTempInventory((invPath) => {
  // Start with empty inventory
  assert.deepStrictEqual(loadInventory(invPath), {});

  // Add items
  addItem('Water Bottle', '2.5', invPath);
  addItem('First-Aid Kit', '1.2', invPath);

  // Verify list
  const items = listItems(invPath);
  assert.strictEqual(items.length, 2);
  const names = items.map(i => i.name).sort();
  assert.deepStrictEqual(names, ['First-Aid Kit', 'Water Bottle']);

  // Verify total weight
  const total = totalWeight(invPath);
  assert.strictEqual(total, 3.7);

  // Remove an item
  removeItem('Water Bottle', invPath);
  const afterRemoval = listItems(invPath);
  assert.strictEqual(afterRemoval.length, 1);
  assert.strictEqual(afterRemoval[0].name, 'First-Aid Kit');
  assert.strictEqual(afterRemoval[0].weight, 1.2);

  // Ensure total updates
  assert.strictEqual(totalWeight(invPath), 1.2);
});

console.log('All tests passed.');
