const assert = require('assert');
const path = require('path');
const fs = require('fs');
const {
    loadSupplies,
    saveSupplies,
    addSupply,
    listSupplies,
    useSupply,
    getExpiringSupplies,
    _DATA_FILE
} = require('../src/index');

// Mock rationale: We need to prevent actual file system operations during tests
// to ensure determinism and isolation. Mocking fs.readFileSync, fs.writeFileSync,
// and fs.existsSync allows us to control the "state" of the supplies.json file
// in memory for each test case. This ensures tests are fast, repeatable, and don't
// leave artifacts on the file system.
let mockFileContent = '[]';
let fileExists = false;

// Store original fs methods to restore them after tests
const originalFs = {
    readFileSync: fs.readFileSync,
    writeFileSync: fs.writeFileSync,
    existsSync: fs.existsSync
};

// Mock fs module methods
const mockFs = {
    readFileSync: (filePath, encoding) => {
        if (filePath === _DATA_FILE) {
            return mockFileContent;
        }
        // Fallback for other files if needed, though not expected for this utility
        return originalFs.readFileSync(filePath, encoding);
    },
    writeFileSync: (filePath, data, encoding) => {
        if (filePath === _DATA_FILE) {
            mockFileContent = data;
        } else {
            // Fallback for other files if needed
            originalFs.writeFileSync(filePath, data, encoding);
        }
    },
    existsSync: (filePath) => {
        if (filePath === _DATA_FILE) {
            return fileExists;
        }
        return originalFs.existsSync(filePath); // Fallback for other files if needed
    }
};

// Replace fs with mockFs for the duration of tests
Object.assign(fs, mockFs);

function setupMockData(data, exists = true) {
    mockFileContent = JSON.stringify(data, null, 2);
    fileExists = exists;
}

function resetMocks() {
    mockFileContent = '[]';
    fileExists = false;
}

// Helper to get a consistent date string for testing relative to 'today'
function getTestDate(offsetDays = 0) {
    const d = new Date();
    d.setDate(d.getDate() + offsetDays);
    return d.toISOString().split('T')[0];
}

console.log('Running tests for nightly-temporal-supply-rotator...');

// Test Suite
(function() {
    // Test 1: addSupply - new item
    resetMocks();
    const date1 = getTestDate(10);
    const addResult1 = addSupply('Canned Beans', 5, date1);
    assert.ok(addResult1.includes('Added 5x Canned Beans'), 'Test 1 Failed: addSupply should add a new item.');
    let supplies = JSON.parse(mockFileContent);
    assert.strictEqual(supplies.length, 1, 'Test 1 Failed: Should have 1 supply after adding.');
    assert.strictEqual(supplies[0].name, 'Canned Beans', 'Test 1 Failed: Item name mismatch.');
    assert.strictEqual(supplies[0].quantity, 5, 'Test 1 Failed: Item quantity mismatch.');
    assert.strictEqual(supplies[0].expiration, date1, 'Test 1 Failed: Item expiration mismatch.');
    console.log('Test 1 Passed: addSupply - new item');

    // Test 2: addSupply - another item
    const date2 = getTestDate(2);
    const addResult2 = addSupply('Water Purifier Tablets', 100, date2);
    assert.ok(addResult2.includes('Added 100x Water Purifier Tablets'), 'Test 2 Failed: addSupply should add another item.');
    supplies = JSON.parse(mockFileContent);
    assert.strictEqual(supplies.length, 2, 'Test 2 Failed: Should have 2 supplies after adding.');
    console.log('Test 2 Passed: addSupply - another item');

    // Test 3: listSupplies - check order and format
    const listOutput = listSupplies();
    assert.ok(listOutput.includes('--- Temporal Larder Inventory ---'), 'Test 3 Failed: listSupplies header missing.');
    assert.ok(listOutput.includes('Water Purifier Tablets (x100)'), 'Test 3 Failed: Water Purifier Tablets missing from list.');
    assert.ok(listOutput.includes('Canned Beans (x5)'), 'Test 3 Failed: Canned Beans missing from list.');
    assert.ok(listOutput.indexOf('Water Purifier Tablets') < listOutput.indexOf('Canned Beans'), 'Test 3 Failed: listSupplies should be sorted by expiration.');
    assert.ok(listOutput.includes(`Expires in 2 day`), 'Test 3 Failed: Water Purifier Tablets status incorrect.'); // 'day' vs 'days' for 1 day left
    assert.ok(listOutput.includes(`Expires in 10 days`), 'Test 3 Failed: Canned Beans status incorrect.');
    console.log('Test 3 Passed: listSupplies - check order and format');

    // Test 4: useSupply - partial use
    const itemIdToUse = supplies.find(s => s.name === 'Canned Beans').id;
    const useResult1 = useSupply(itemIdToUse, 2);
    assert.ok(useResult1.includes('Used 2x Canned Beans. Remaining: 3.'), 'Test 4 Failed: useSupply partial use message incorrect.');
    supplies = JSON.parse(mockFileContent);
    const updatedBeans = supplies.find(s => s.name === 'Canned Beans');
    assert.strictEqual(updatedBeans.quantity, 3, 'Test 4 Failed: Canned Beans quantity not updated correctly.');
    console.log('Test 4 Passed: useSupply - partial use');

    // Test 5: useSupply - full depletion
    const useResult2 = useSupply(itemIdToUse, 3);
    assert.ok(useResult2.includes('Used 3x Canned Beans. Remaining: 0. Canned Beans fully depleted and removed from inventory.'), 'Test 5 Failed: useSupply full depletion message incorrect.');
    supplies = JSON.parse(mockFileContent);
    assert.strictEqual(supplies.length, 1, 'Test 5 Failed: Canned Beans should be removed after full depletion.');
    assert.strictEqual(supplies[0].name, 'Water Purifier Tablets', 'Test 5 Failed: Only Water Purifier Tablets should remain.');
    console.log('Test 5 Passed: useSupply - full depletion');

    // Test 6: getExpiringSupplies - within threshold
    resetMocks();
    setupMockData([
        { id: 1, name: 'Ration Pack A', quantity: 10, expiration: getTestDate(1) },
        { id: 2, name: 'Ration Pack B', quantity: 5, expiration: getTestDate(5) },
        { id: 3, name: 'Ration Pack C', quantity: 20, expiration: getTestDate(15) }
    ]);
    const expiringOutput = getExpiringSupplies(7);
    assert.ok(expiringOutput.includes('Ration Pack A'), 'Test 6 Failed: Ration Pack A should be in expiring list.');
    assert.ok(expiringOutput.includes('Ration Pack B'), 'Test 6 Failed: Ration Pack B should be in expiring list.');
    assert.ok(!expiringOutput.includes('Ration Pack C'), 'Test 6 Failed: Ration Pack C should NOT be in expiring list.');
    assert.ok(expiringOutput.indexOf('Ration Pack A') < expiringOutput.indexOf('Ration Pack B'), 'Test 6 Failed: Expiring supplies should be sorted.');
    assert.ok(expiringOutput.includes(`Expires in 1 day`), 'Test 6 Failed: Ration Pack A status incorrect.');
    assert.ok(expiringOutput.includes(`Expires in 5 days`), 'Test 6 Failed: Ration Pack B status incorrect.');
    console.log('Test 6 Passed: getExpiringSupplies - within threshold');

    // Test 7: getExpiringSupplies - no expiring items
    resetMocks();
    setupMockData([
        { id: 1, name: 'Long-term MRE', quantity: 50, expiration: getTestDate(365) }
    ]);
    const noExpiringOutput = getExpiringSupplies(7);
    assert.ok(noExpiringOutput.includes('No supplies are nearing temporal decay'), 'Test 7 Failed: Should indicate no expiring supplies.');
    console.log('Test 7 Passed: getExpiringSupplies - no expiring items');

    // Test 8: listSupplies - empty larder
    resetMocks();
    const emptyLarderOutput = listSupplies();
    assert.ok(emptyLarderOutput.includes('Your temporal larder is empty'), 'Test 8 Failed: Empty larder message incorrect.');
    console.log('Test 8 Passed: listSupplies - empty larder');

    // Test 9: addSupply - invalid date
    resetMocks();
    assert.throws(() => addSupply('Bad Food', 1, 'not-a-date'), /Invalid expiration date format/, 'Test 9 Failed: Should throw error for invalid date.');
    assert.throws(() => addSupply('Bad Food', 1, '2023-13-01'), /Invalid expiration date format/, 'Test 9 Failed: Should throw error for invalid month in date.');
    console.log('Test 9 Passed: addSupply - invalid date');

    // Test 10: useSupply - item not found
    resetMocks();
    setupMockData([
        { id: 100, name: 'Valid Item', quantity: 1, expiration: getTestDate(1) }
    ]);
    assert.throws(() => useSupply(999, 1), /Supply with ID 999 not found/, 'Test 10 Failed: Should throw error for item not found.');
    console.log('Test 10 Passed: useSupply - item not found');

    // Test 11: useSupply - not enough quantity
    resetMocks();
    setupMockData([
        { id: 100, name: 'Valid Item', quantity: 1, expiration: getTestDate(1) }
    ]);
    assert.throws(() => useSupply(100, 2), /Not enough Valid Item/, 'Test 11 Failed: Should throw error for not enough quantity.');
    console.log('Test 11 Passed: useSupply - not enough quantity');

    // Test 12: useSupply - invalid quantity
    resetMocks();
    setupMockData([
        { id: 100, name: 'Valid Item', quantity: 1, expiration: getTestDate(1) }
    ]);
    assert.throws(() => useSupply(100, 'abc'), /Quantity to use must be a positive number/, 'Test 12 Failed: Should throw error for invalid quantity string.');
    assert.throws(() => useSupply(100, 0), /Quantity to use must be a positive number/, 'Test 12 Failed: Should throw error for zero quantity.');
    assert.throws(() => addSupply('Invalid Qty Item', 'abc', getTestDate(1)), /Quantity must be a positive number/, 'Test 12 Failed: Should throw error for invalid quantity in addSupply.');
    console.log('Test 12 Passed: useSupply - invalid quantity');

    // Test 13: getExpiringSupplies - expired items should not be listed
    resetMocks();
    setupMockData([
        { id: 1, name: 'Expired Ration', quantity: 1, expiration: getTestDate(-1) },
        { id: 2, name: 'Expiring Soon', quantity: 1, expiration: getTestDate(2) }
    ]);
    const expiringOutput2 = getExpiringSupplies(7);
    assert.ok(!expiringOutput2.includes('Expired Ration'), 'Test 13 Failed: Expired items should not be in expiring list.');
    assert.ok(expiringOutput2.includes('Expiring Soon'), 'Test 13 Failed: Expiring soon item should be in list.');
    console.log('Test 13 Passed: getExpiringSupplies - expired items not listed');

    // Test 14: loadSupplies - empty file content
    resetMocks();
    fileExists = true; // Simulate file exists but is empty
    mockFileContent = '';
    const emptyLoad = loadSupplies();
    assert.deepStrictEqual(emptyLoad, [], 'Test 14 Failed: Should return empty array for empty file content.');
    console.log('Test 14 Passed: loadSupplies - empty file content');

    // Test 15: loadSupplies - corrupted JSON
    resetMocks();
    fileExists = true;
    mockFileContent = '{ "invalid": "json"';
    // Expecting an error message to console, but function should return empty array
    const corruptedLoad = loadSupplies();
    assert.deepStrictEqual(corruptedLoad, [], 'Test 15 Failed: Should return empty array for corrupted JSON.');
    console.log('Test 15 Passed: loadSupplies - corrupted JSON');

})();

// Restore original fs module after tests
Object.assign(fs, originalFs);

console.log('All tests completed.');
