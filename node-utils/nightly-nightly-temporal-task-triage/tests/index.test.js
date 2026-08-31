const assert = require('assert');
const fs = require('fs');
const { calculateTriageScore, readTasksFromFile, triageTasks, RESONANCE_WEIGHTS, PRIORITY_WEIGHTS } = require('../src/index');

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure deterministic and offline tests. This mock replaces fs.readFileSync.
const mockFsContent = {
    'mock_tasks.json': JSON.stringify([
        { "id": "task-1", "description": "Repair Chrono-Stabilizer", "resonance": "Rumbles of the Imminent", "priority": "critical" },
        { "id": "task-2", "description": "Archive ancient data logs", "resonance": "Echoes of Yesteryear", "priority": "low" },
        { "id": "task-3", "description": "Prepare for next temporal shift", "resonance": "Shadows of Tomorrow", "priority": "medium" },
        { "id": "task-4", "description": "Respond to current void whispers", "resonance": "Whispers of Now", "priority": "high" },
        { "id": "task-5", "description": "Plan for interstellar colonization", "resonance": "Flickers of the Distant", "priority": "none" },
        { "id": "task-6", "description": "Calibrate temporal sensors", "resonance": "Rumbles of the Imminent", "priority": "high" },
        { "id": "task-7", "description": "Unknown resonance/priority", "resonance": "NonExistent", "priority": "Urgent" },
        { "id": "task-8", "description": "Missing resonance", "priority": "high" },
        { "id": "task-9", "description": "Missing priority", "resonance": "Whispers of Now" },
        { "id": "task-10", "description": "Completely malformed task" }
    ]),
    'empty_tasks.json': '[]',
    'invalid_json.json': '{ "tasks": [ { "id": "bad" }', // Malformed JSON
    'non_array_json.json': '{ "id": "single_task" }' // Valid JSON, but not an array
};

// Store original fs.readFileSync to restore it later
const originalReadFileSync = fs.readFileSync;

// Override fs.readFileSync for testing purposes
fs.readFileSync = (filePath, encoding) => {
    if (mockFsContent[filePath]) {
        return mockFsContent[filePath];
    }
    // Simulate file not found for other paths
    const error = new Error(`ENOENT: no such file or directory, open '${filePath}'`);
    error.code = 'ENOENT';
    throw error;
};

console.log('Running tests for nightly-temporal-task-triage...');

// Test Suite
(function() {
    console.log('  Testing calculateTriageScore...');

    // Test 1: Standard task with known resonance and priority
    const task1 = { resonance: 'Rumbles of the Imminent', priority: 'critical' };
    assert.strictEqual(calculateTriageScore(task1), 55, 'Test 1 Failed: Critical imminent task score incorrect');

    // Test 2: Another standard task
    const task2 = { resonance: 'Echoes of Yesteryear', priority: 'low' };
    assert.strictEqual(calculateTriageScore(task2), 22, 'Test 2 Failed: Low yesteryear task score incorrect');

    // Test 3: Task with unknown resonance, known priority
    const task3 = { resonance: 'NonExistent', priority: 'high' };
    assert.strictEqual(calculateTriageScore(task3), (RESONANCE_WEIGHTS.unknown * 10) + PRIORITY_WEIGHTS.high, 'Test 3 Failed: Unknown resonance score incorrect');

    // Test 4: Task with known resonance, unknown priority
    const task4 = { resonance: 'Whispers of Now', priority: 'Urgent' };
    assert.strictEqual(calculateTriageScore(task4), (RESONANCE_WEIGHTS['Whispers of Now'] * 10) + PRIORITY_WEIGHTS.unknown, 'Test 4 Failed: Unknown priority score incorrect');

    // Test 5: Task with missing resonance field
    const task5 = { priority: 'medium' };
    assert.strictEqual(calculateTriageScore(task5), (RESONANCE_WEIGHTS.unknown * 10) + PRIORITY_WEIGHTS.medium, 'Test 5 Failed: Missing resonance field score incorrect');

    // Test 6: Task with missing priority field
    const task6 = { resonance: 'Shadows of Tomorrow' };
    assert.strictEqual(calculateTriageScore(task6), (RESONANCE_WEIGHTS['Shadows of Tomorrow'] * 10) + PRIORITY_WEIGHTS.unknown, 'Test 6 Failed: Missing priority field score incorrect');

    // Test 7: Task with both missing resonance and priority fields
    const task7 = {};
    assert.strictEqual(calculateTriageScore(task7), (RESONANCE_WEIGHTS.unknown * 10) + PRIORITY_WEIGHTS.unknown, 'Test 7 Failed: Both missing fields score incorrect');

    console.log('    calculateTriageScore tests passed.');

    console.log('  Testing readTasksFromFile...');

    // Test 8: Read valid tasks file
    const validTasks = readTasksFromFile('mock_tasks.json');
    assert.strictEqual(validTasks.length, 10, 'Test 8 Failed: Should read 10 tasks from mock_tasks.json');
    assert.strictEqual(validTasks[0].id, 'task-1', 'Test 8 Failed: First task ID incorrect');

    // Test 9: Read empty tasks file
    const emptyTasks = readTasksFromFile('empty_tasks.json');
    assert.strictEqual(emptyTasks.length, 0, 'Test 9 Failed: Should read 0 tasks from empty_tasks.json');

    // Test 10: File not found error
    assert.throws(() => readTasksFromFile('non_existent_file.json'), /Error: Task file not found/, 'Test 10 Failed: Should throw file not found error');

    // Test 11: Invalid JSON format error
    assert.throws(() => readTasksFromFile('invalid_json.json'), /Error: Invalid JSON/, 'Test 11 Failed: Should throw invalid JSON error');

    // Test 12: JSON is not an array error
    assert.throws(() => readTasksFromFile('non_array_json.json'), /Error: Invalid JSON format: Expected an array of tasks./, 'Test 12 Failed: Should throw non-array JSON error');

    console.log('    readTasksFromFile tests passed.');

    console.log('  Testing triageTasks...');

    // Test 13: Triage a list of tasks and check sorting order
    const sampleTasks = [
        { "id": "A", "description": "Task A", "resonance": "Whispers of Now", "priority": "high" }, // Score: 44
        { "id": "B", "description": "Task B", "resonance": "Rumbles of the Imminent", "priority": "critical" }, // Score: 55
        { "id": "C", "description": "Task C", "resonance": "Echoes of Yesteryear", "priority": "low" } // Score: 22
    ];
    const sortedSampleTasks = triageTasks(sampleTasks);
    assert.strictEqual(sortedSampleTasks.length, 3, 'Test 13 Failed: Should have 3 tasks after triage');
    assert.strictEqual(sortedSampleTasks[0].id, 'B', 'Test 13 Failed: Task B should be first');
    assert.strictEqual(sortedSampleTasks[0].score, 55, 'Test 13 Failed: Task B score incorrect');
    assert.strictEqual(sortedSampleTasks[1].id, 'A', 'Test 13 Failed: Task A should be second');
    assert.strictEqual(sortedSampleTasks[1].score, 44, 'Test 13 Failed: Task A score incorrect');
    assert.strictEqual(sortedSampleTasks[2].id, 'C', 'Test 13 Failed: Task C should be third');
    assert.strictEqual(sortedSampleTasks[2].score, 22, 'Test 13 Failed: Task C score incorrect');

    // Test 14: Triage tasks with some malformed entries (missing id/description)
    const tasksWithMalformed = [
        { "id": "GoodTask", "description": "A valid task", "resonance": "Whispers of Now", "priority": "high" },
        { "resonance": "Rumbles of the Imminent", "priority": "critical" }, // Missing id/description
        { "id": "AnotherGoodTask", "description": "Another valid task", "resonance": "Shadows of Tomorrow", "priority": "medium" }
    ];
    // We expect a console.warn for the malformed task, but triageTasks should return only valid ones.
    const originalWarn = console.warn;
    let warnCalled = false;
    console.warn = (message) => {
        if (message.includes('Skipping malformed task')) {
            warnCalled = true;
        }
    };
    const sortedFilteredTasks = triageTasks(tasksWithMalformed);
    console.warn = originalWarn; // Restore original warn

    assert.strictEqual(sortedFilteredTasks.length, 2, 'Test 14 Failed: Should filter out malformed tasks');
    assert.ok(warnCalled, 'Test 14 Failed: console.warn should have been called for malformed task');
    assert.strictEqual(sortedFilteredTasks[0].id, 'GoodTask', 'Test 14 Failed: GoodTask should be first');
    assert.strictEqual(sortedFilteredTasks[1].id, 'AnotherGoodTask', 'Test 14 Failed: AnotherGoodTask should be second');

    // Test 15: Triage an empty array of tasks
    const emptyTriaged = triageTasks([]);
    assert.strictEqual(emptyTriaged.length, 0, 'Test 15 Failed: Triage of empty array should return empty array');

    console.log('    triageTasks tests passed.');

    console.log('\nAll tests passed!\n');

})().finally(() => {
    // Restore original fs.readFileSync after all tests are done
    fs.readFileSync = originalReadFileSync;
});
