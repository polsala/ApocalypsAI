const assert = require('assert');
const path = require('path');
const { getMood, colors, moodKeywords } = require('../src/mood-ring.js');

// Mock rationale: fs.readFileSync is mocked to provide deterministic log content
// without relying on actual file system operations, ensuring tests are offline and consistent.
const mockFs = {
    readFileSync: (filePath, encoding) => {
        const mockLogs = {
            'test_happy.log': 'INFO: System startup complete. All services are running. Deployment successful!',
            'test_angry.log': 'ERROR: Failed to connect to database. Critical exception occurred. Panic!',
            'test_anxious.log': 'WARNING: Disk space low. Retrying connection. Attention required.',
            'test_calm.log': 'INFO: User logged in. Status check passed. Monitoring system idle.',
            'test_empty.log': '',
            'test_mixed.log': 'WARNING: Timeout. ERROR: Failed to process. INFO: System running.',
            'test_mysterious.log': 'Unknown signal detected. Anomaly in sector 7. Unidentified object.',
            'test_no_keywords.log': 'This is a log file with no specific keywords to trigger a mood.'
        };
        const fileName = path.basename(filePath);
        if (mockLogs[fileName]) {
            return mockLogs[fileName];
        }
        throw new Error(`ENOENT: no such file or directory, open '${filePath}'`);
    }
};

// Temporarily override fs for testing
const originalFsReadFileSync = require('fs').readFileSync;
require('fs').readFileSync = mockFs.readFileSync;

console.log('Running Mood Ring Terminal tests...');

function testGetMood() {
    console.log('  Testing getMood function...');

    // Test 1: Happy mood
    let mood = getMood(mockFs.readFileSync('test_happy.log', 'utf8'));
    assert.strictEqual(mood.name, 'happy', `Test 1 Failed: Expected happy, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.green, `Test 1 Failed: Expected green color, got ${mood.color}`);
    console.log('    ✅ Test 1: Happy mood detected.');

    // Test 2: Angry mood
    mood = getMood(mockFs.readFileSync('test_angry.log', 'utf8'));
    assert.strictEqual(mood.name, 'angry', `Test 2 Failed: Expected angry, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.red, `Test 2 Failed: Expected red color, got ${mood.color}`);
    console.log('    ✅ Test 2: Angry mood detected.');

    // Test 3: Anxious mood
    mood = getMood(mockFs.readFileSync('test_anxious.log', 'utf8'));
    assert.strictEqual(mood.name, 'anxious', `Test 3 Failed: Expected anxious, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.yellow, `Test 3 Failed: Expected yellow color, got ${mood.color}`);
    console.log('    ✅ Test 3: Anxious mood detected.');

    // Test 4: Calm mood
    mood = getMood(mockFs.readFileSync('test_calm.log', 'utf8'));
    assert.strictEqual(mood.name, 'calm', `Test 4 Failed: Expected calm, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.blue, `Test 4 Failed: Expected blue color, got ${mood.color}`);
    console.log('    ✅ Test 4: Calm mood for calm log.');

    // Test 5: Empty log
    mood = getMood(mockFs.readFileSync('test_empty.log', 'utf8'));
    assert.strictEqual(mood.name, 'calm', `Test 5 Failed: Expected calm for empty log, got ${mood.name}`);
    console.log('    ✅ Test 5: Calm mood for empty log.');

    // Test 6: Mixed log (should result in mysterious due to tied highest scores)
    mood = getMood(mockFs.readFileSync('test_mixed.log', 'utf8'));
    assert.strictEqual(mood.name, 'mysterious', `Test 6 Failed: Expected mysterious for mixed log, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.magenta, `Test 6 Failed: Expected magenta color for mixed log, got ${mood.color}`);
    console.log('    ✅ Test 6: Mysterious mood for mixed log.');

    // Test 7: Mysterious mood
    mood = getMood(mockFs.readFileSync('test_mysterious.log', 'utf8'));
    assert.strictEqual(mood.name, 'mysterious', `Test 7 Failed: Expected mysterious, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.magenta, `Test 7 Failed: Expected magenta color, got ${mood.color}`);
    console.log('    ✅ Test 7: Mysterious mood detected.');

    // Test 8: No specific keywords, should default to calm
    mood = getMood(mockFs.readFileSync('test_no_keywords.log', 'utf8'));
    assert.strictEqual(mood.name, 'calm', `Test 8 Failed: Expected calm for no keywords, got ${mood.name}`);
    assert.strictEqual(mood.color, colors.blue, `Test 8 Failed: Expected blue color for no keywords, got ${mood.color}`);
    console.log('    ✅ Test 8: Calm mood for no specific keywords.');

    console.log('  All getMood tests passed!');
}

// Run tests
try {
    testGetMood();
    console.log('\nAll Mood Ring Terminal tests completed successfully!');
} catch (error) {
    console.error('\nTests failed:', error.message);
    process.exit(1);
} finally {
    // Restore original fs.readFileSync after tests
    require('fs').readFileSync = originalFsReadFileSync;
}
