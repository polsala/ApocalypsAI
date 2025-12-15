const assert = require('assert');
const { getRandomNudge, defaultNudges } = require('../src/index');

// Mock rationale: Math.random needs to be mocked to ensure deterministic test results.
// Without mocking, the tests would be flaky as the random selection would change on each run.
// This mock allows us to control the "random" outcome for predictable testing.

function runTests() {
    console.log('Running Nightly Cosmic Nudge tests...');

    // Test Case 1: Default nudges - should pick the first item when Math.random is 0
    (function testDefaultNudgesFirstItem() {
        const originalRandom = Math.random;
        Math.random = () => 0; // Mock Math.random to always return 0
        const nudge = getRandomNudge(defaultNudges);
        assert.strictEqual(nudge, defaultNudges[0], 'Test Case 1 Failed: Should pick the first default nudge.');
        Math.random = originalRandom; // Restore original Math.random
        console.log('  ✔ Test Case 1: Default nudges (first item) passed.');
    })();

    // Test Case 2: Default nudges - should pick the last item when Math.random is close to 1
    (function testDefaultNudgesLastItem() {
        const originalRandom = Math.random;
        Math.random = () => 0.999999999; // Mock Math.random to return a value close to 1
        const nudge = getRandomNudge(defaultNudges);
        assert.strictEqual(nudge, defaultNudges[defaultNudges.length - 1], 'Test Case 2 Failed: Should pick the last default nudge.');
        Math.random = originalRandom;
        console.log('  ✔ Test Case 2: Default nudges (last item) passed.');
    })();

    // Test Case 3: Custom nudges - should pick the first item
    (function testCustomNudgesFirstItem() {
        const customOptions = ["Option A", "Option B", "Option C"];
        const originalRandom = Math.random;
        Math.random = () => 0;
        const nudge = getRandomNudge(customOptions);
        assert.strictEqual(nudge, customOptions[0], 'Test Case 3 Failed: Should pick the first custom nudge.');
        Math.random = originalRandom;
        console.log('  ✔ Test Case 3: Custom nudges (first item) passed.');
    })();

    // Test Case 4: Custom nudges - should pick the last item
    (function testCustomNudgesLastItem() {
        const customOptions = ["Option X", "Option Y", "Option Z"];
        const originalRandom = Math.random;
        Math.random = () => 0.999999999;
        const nudge = getRandomNudge(customOptions);
        assert.strictEqual(nudge, customOptions[customOptions.length - 1], 'Test Case 4 Failed: Should pick the last custom nudge.');
        Math.random = originalRandom;
        console.log('  ✔ Test Case 4: Custom nudges (last item) passed.');
    })();

    // Test Case 5: Empty options array
    (function testEmptyOptions() {
        const nudge = getRandomNudge([]);
        assert.strictEqual(nudge, "Contemplate the infinite emptiness.", 'Test Case 5 Failed: Should return default message for empty array.');
        console.log('  ✔ Test Case 5: Empty options array passed.');
    })();

    // Test Case 6: Null options array
    (function testNullOptions() {
        const nudge = getRandomNudge(null);
        assert.strictEqual(nudge, "Contemplate the infinite emptiness.", 'Test Case 6 Failed: Should return default message for null array.');
        console.log('  ✔ Test Case 6: Null options array passed.');
    })();

    // Test Case 7: Undefined options array
    (function testUndefinedOptions() {
        const nudge = getRandomNudge(undefined);
        assert.strictEqual(nudge, "Contemplate the infinite emptiness.", 'Test Case 7 Failed: Should return default message for undefined array.');
        console.log('  ✔ Test Case 7: Undefined options array passed.');
    })();

    console.log('\nAll Nightly Cosmic Nudge tests passed!');
}

runTests();
