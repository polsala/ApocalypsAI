const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { addItem, listItems, getExpiringItems } = require('../src/util');

// Mock rationale: Use a temporary data file to avoid polluting real data.
const DATA_FILE = path.join(__dirname, '..', 'data.json');
function resetData() {
  if (fs.existsSync(DATA_FILE)) fs.unlinkSync(DATA_FILE);
  fs.writeFileSync(DATA_FILE, '[]', 'utf8');
}

// Begin tests
resetData();

addItem('Test Food', 5);
addItem('Long Life', 30);
let all = listItems();
assert.strictEqual(all.length, 2, 'Should have 2 items');

let expiring = getExpiringItems(7);
assert.strictEqual(expiring.length, 1, 'Only one item within 7 days');
assert.strictEqual(expiring[0].name, 'Test Food');

resetData();
console.log('All tests passed.');
