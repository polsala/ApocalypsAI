const assert = require('assert');
const fs = require('fs');
const path = require('path');
const sinon = require('sinon');

// Import functions to test
const {
    loadRituals,
    saveRituals,
    getTodayDate,
    addRitual,
    listRituals,
    completeRitual,
    resetRituals,
    _DATA_FILE
} = require('../src/ritual-tracker');

// Mock rationale: We need to control file system interactions to ensure tests are deterministic and offline.
// We also need to control the current date to test ritual completion logic across different "days".
let fsReadFileSyncStub;
let fsWriteFileSyncStub;
let consoleLogStub;
let consoleErrorStub;
let dateStub;

let mockRitualsData = [];

/**
 * Sets up mocks for fs operations, console output, and Date object.
 */
function setupMocks() {
    // Reset mock data before each test run
    mockRitualsData = [];

    // Stub fs.readFileSync to return our mock data or simulate file not found
    fsReadFileSyncStub = sinon.stub(fs, 'readFileSync').callsFake((filePath, encoding) => {
        if (filePath === _DATA_FILE) {
            return JSON.stringify(mockRitualsData);
        }
        // Fallback for other files if needed, though not expected in this util
        return fsReadFileSyncStub.wrappedMethod.call(fs, filePath, encoding);
    });

    // Stub fs.writeFileSync to capture data written and update mock data
    fsWriteFileSyncStub = sinon.stub(fs, 'writeFileSync').callsFake((filePath, data, encoding) => {
        if (filePath === _DATA_FILE) {
            mockRitualsData = JSON.parse(data);
            return;
        }
        // Fallback for other files
        fsWriteFileSyncStub.wrappedMethod.call(fs, filePath, data, encoding);
    });

    // Stub console.log and console.error to prevent actual output during tests
    // and allow checking their calls.
    consoleLogStub = sinon.stub(console, 'log');
    consoleErrorStub = sinon.stub(console, 'error');

    // Stub Date to control the current date for deterministic testing of completion logic.
    dateStub = sinon.stub(global, 'Date');
    dateStub.value(function(dateString) {
        if (dateString) {
            return new dateStub.wrappedMethod(dateString);
        }
        return new dateStub.wrappedMethod('2023-10-27T10:00:00Z'); // Default mock date
    });
    dateStub.value.now = () => new dateStub.wrappedMethod('2023-10-27T10:00:00Z').getTime();
}

/**
 * Restores all stubbed functions to their original implementations.
 */
function teardownMocks() {
    sinon.restore();
}

// Define test cases
const tests = [
    {
        name: 'should add a new ritual',
        run: () => {
            addRitual('Scavenge for rations');
            assert.strictEqual(mockRitualsData.length, 1);
            assert.strictEqual(mockRitualsData[0].name, 'Scavenge for rations');
            assert.strictEqual(mockRitualsData[0].lastCompleted, null);
            assert.ok(consoleLogStub.calledWith("Ritual 'Scavenge for rations' added to your apocalyptic regimen."));
        }
    },
    {
        name: 'should list rituals as pending if not completed today',
        run: () => {
            mockRitualsData = [{ id: '1', name: 'Check perimeter', lastCompleted: null }];
            listRituals();
            assert.ok(consoleLogStub.calledWithMatch('- [⏳ PENDING] Check perimeter'));
        }
    },
    {
        name: 'should list rituals as completed if completed today',
        run: () => {
            const today = getTodayDate(); // This will use the mocked date
            mockRitualsData = [{ id: '2', name: 'Repair shelter', lastCompleted: today }];
            listRituals();
            assert.ok(consoleLogStub.calledWithMatch('- [✅ COMPLETED] Repair shelter'));
        }
    },
    {
        name: 'should mark a ritual as complete by name',
        run: () => {
            mockRitualsData = [{ id: '3', name: 'Water crops', lastCompleted: null }];
            completeRitual('Water crops');
            const today = getTodayDate();
            assert.strictEqual(mockRitualsData[0].lastCompleted, today);
            assert.ok(consoleLogStub.calledWith("Ritual 'Water crops' marked as completed for today."));
        }
    },
    {
        name: 'should mark a ritual as complete by ID',
        run: () => {
            mockRitualsData = [{ id: '4', name: 'Sharpen tools', lastCompleted: null }];
            completeRitual('4');
            const today = getTodayDate();
            assert.strictEqual(mockRitualsData[0].lastCompleted, today);
            assert.ok(consoleLogStub.calledWith("Ritual 'Sharpen tools' marked as completed for today."));
        }
    },
    {
        name: 'should handle completing a non-existent ritual',
        run: () => {
            mockRitualsData = [{ id: '5', name: 'Gather firewood', lastCompleted: null }];
            completeRitual('NonExistent');
            assert.ok(consoleErrorStub.calledWith("Ritual 'NonExistent' not found. Use 'list' to see available rituals."));
            assert.strictEqual(mockRitualsData[0].lastCompleted, null); // Should not change
        }
    },
    {
        name: 'should reset all rituals to pending',
        run: () => {
            const yesterday = '2023-10-26';
            mockRitualsData = [
                { id: '6', name: 'Clean water filter', lastCompleted: yesterday },
                { id: '7', name: 'Check traps', lastCompleted: getTodayDate() } // Completed today
            ];
            resetRituals();
            assert.strictEqual(mockRitualsData[0].lastCompleted, null);
            assert.strictEqual(mockRitualsData[1].lastCompleted, null);
            assert.ok(consoleLogStub.calledWith('All rituals reset to pending. A new day, a new struggle!'));
        }
    },
    {
        name: 'should list rituals as pending if completed on a previous day',
        run: () => {
            const previousDay = '2023-10-26';
            mockRitualsData = [{ id: '8', name: 'Fortify defenses', lastCompleted: previousDay }];

            // Change the mocked date to a new day to simulate a day passing
            dateStub.value(function(dateString) {
                if (dateString) {
                    return new dateStub.wrappedMethod(dateString);
                }
                return new dateStub.wrappedMethod('2023-10-27T10:00:00Z'); // New default mock date
            });
            dateStub.value.now = () => new dateStub.wrappedMethod('2023-10-27T10:00:00Z').getTime();

            listRituals();
            assert.ok(consoleLogStub.calledWithMatch('- [⏳ PENDING] Fortify defenses'));
        }
    },
    {
        name: 'should create an empty data file if it does not exist',
        run: () => {
            // Simulate file not existing by making readFileSync throw ENOENT
            fsReadFileSyncStub.restore(); // Restore original to re-stub with specific error
            fsReadFileSyncStub = sinon.stub(fs, 'readFileSync').callsFake((filePath, encoding) => {
                if (filePath === _DATA_FILE) {
                    const error = new Error('File not found');
                    error.code = 'ENOENT';
                    throw error;
                }
                return fsReadFileSyncStub.wrappedMethod.call(fs, filePath, encoding);
            });

            const rituals = loadRituals();
            assert.deepStrictEqual(rituals, []);
            assert.ok(fsReadFileSyncStub.calledWith(_DATA_FILE, 'utf8'));
        }
    },
    {
        name: 'should handle JSON parsing errors gracefully',
        run: () => {
            fsReadFileSyncStub.restore();
            fsReadFileSyncStub = sinon.stub(fs, 'readFileSync').callsFake((filePath, encoding) => {
                if (filePath === _DATA_FILE) {
                    return '{"invalid json"'; // Malformed JSON
                }
                return fsReadFileSyncStub.wrappedMethod.call(fs, filePath, encoding);
            });

            const rituals = loadRituals();
            assert.deepStrictEqual(rituals, []);
            assert.ok(consoleErrorStub.calledWithMatch('Error loading rituals:'));
        }
    }
];

let passedTests = 0;
let failedTests = 0;

console.log('Running Nightly Apocalyptic Rituals Tracker tests...');

// Execute each test case
for (const test of tests) {
    try {
        setupMocks(); // Setup mocks before each test
        test.run();
        console.log(`✅ ${test.name}`);
        passedTests++;
    } catch (error) {
        console.error(`❌ ${test.name}`);
        console.error(error);
        failedTests++;
    } finally {
        teardownMocks(); // Restore mocks after each test
    }
}

console.log(`\n--- Test Summary ---`);
console.log(`Passed: ${passedTests}`);
console.log(`Failed: ${failedTests}`);

// Exit with appropriate status code
if (failedTests > 0) {
    process.exit(1);
} else {
    process.exit(0);
}
