const assert = require('assert');
const { classifyInput, getRandomMoodKey, moods, run } = require('../src/index');

// Mock rationale: Math.random is mocked to ensure getRandomMoodKey is deterministic.
// console.log is mocked to prevent test output from cluttering the console and to capture it for assertion.
// process.argv is mocked to simulate command-line arguments.
// The readline module is mocked to prevent interactive prompts during tests.

const originalRandom = Math.random;
const originalConsoleLog = console.log;
let consoleOutput = [];

function mockConsoleLog(...args) {
    consoleOutput.push(args.join(' '));
}

// Helper for running tests
function test(name, fn) {
    try {
        fn();
        console.log(`✓ ${name}`);
    } catch (error) {
        console.error(`✗ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

// Helper for async tests
async function testAsync(name, fn) {
    try {
        await fn();
        console.log(`✓ ${name}`);
    } catch (error) {
        console.error(`✗ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

// Setup and Teardown
function beforeEachTest() {
    consoleOutput = [];
    console.log = mockConsoleLog;
}

function afterEachTest() {
    console.log = originalConsoleLog;
    Math.random = originalRandom; // Restore Math.random
}

console.log('Running tests for Nightly Wasteland Mood Ring Utility...');

// --- Test classifyInput function ---

beforeEachTest();
test('classifyInput should classify "rainy day" as gloomy', () => {
    const mood = classifyInput('rainy day');
    assert.strictEqual(mood, 'gloomy');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify "sunny adventure" as energetic', () => {
    const mood = classifyInput('sunny adventure');
    assert.strictEqual(mood, 'energetic');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify "secret whispers" as mysterious', () => {
    const mood = classifyInput('secret whispers');
    assert.strictEqual(mood, 'mysterious');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify "quiet evening" as calm', () => {
    const mood = classifyInput('quiet evening');
    assert.strictEqual(mood, 'calm');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify "utter chaos" as chaotic', () => {
    const mood = classifyInput('utter chaos');
    assert.strictEqual(mood, 'chaotic');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify "hope for tomorrow" as hopeful', () => {
    const mood = classifyInput('hope for tomorrow');
    assert.strictEqual(mood, 'hopeful');
});
afterEachTest();

beforeEachTest();
test('classifyInput should classify an unmatching input deterministically using hash', () => {
    // Mock rationale: The hash function is deterministic, so for a given input, the output mood should be consistent.
    const mood = classifyInput('random word that does not match keywords');
    let testHash = 0;
    const testInput = 'random word that does not match keywords';
    for (let i = 0; i < testInput.length; i++) {
        testHash = testInput.charCodeAt(i) + ((testHash << 5) - testHash);
    }
    const expectedMoodKey = Object.keys(moods)[Math.abs(testHash) % Object.keys(moods).length];
    assert.strictEqual(mood, expectedMoodKey);
});
afterEachTest();

// --- Test getRandomMoodKey function ---

beforeEachTest();
test('getRandomMoodKey should return a deterministic mood key when Math.random is mocked', () => {
    // Mock rationale: Math.random is mocked to ensure getRandomMoodKey is deterministic.
    Math.random = () => 0.0; // Force the first mood ('gloomy')
    const moodKey = getRandomMoodKey();
    assert.strictEqual(moodKey, 'gloomy');

    Math.random = () => 0.99; // Force the last mood ('hopeful')
    const moodKey2 = getRandomMoodKey();
    assert.strictEqual(moodKey2, 'hopeful');
});
afterEachTest();

// --- Test run function (integration tests) ---

(async () => {
    beforeEachTest();
    await testAsync('run should output a mood and suggestion based on argv input', async () => {
        // Mock rationale: process.argv is mocked to simulate command-line input.
        // The readlineInterface is not used when argv is present, so no need to mock it for this specific test.
        const mockArgv = ['node', 'index.js', 'dark', 'clouds']; // Simulate input
        
        await run(mockArgv); // Call run with mocked argv

        assert.ok(consoleOutput.some(line => line.includes('Mood: Gloomy')), `Expected "Mood: Gloomy" in output. Got: ${consoleOutput.join('\n')}`);
        assert.ok(consoleOutput.some(line => line.includes('Seek shelter in the ruins of old libraries')), `Expected "Seek shelter in the ruins of old libraries" in output. Got: ${consoleOutput.join('\n')}`);
    });
    afterEachTest();

    beforeEachTest();
    await testAsync('run should output a random mood and suggestion when no argv input and readline is mocked', async () => {
        // Mock rationale: process.argv is mocked to simulate no command-line input.
        // readlineInterface is mocked to prevent interactive prompt and provide a deterministic empty input.
        // Math.random is mocked to ensure the random mood selection is deterministic.
        const mockArgv = ['node', 'index.js']; // Simulate no input

        const mockReadlineInterface = {
            createInterface: () => ({
                question: (prompt, callback) => {
                    callback(''); // Simulate pressing Enter without input
                },
                close: () => {}
            })
        };

        Math.random = () => 0.0; // Force the first mood ('gloomy') for deterministic random selection

        await run(mockArgv, mockReadlineInterface); // Call run with mocked argv and readlineInterface

        assert.ok(consoleOutput.some(line => line.includes('Mood: Gloomy')), `Expected "Mood: Gloomy" in output. Got: ${consoleOutput.join('\n')}`);
        assert.ok(consoleOutput.some(line => line.includes('Seek shelter in the ruins of old libraries')), `Expected "Seek shelter in the ruins of old libraries" in output. Got: ${consoleOutput.join('\n')}`);
    });
    afterEachTest();

    beforeEachTest();
    await testAsync('run should output a classified mood and suggestion when no argv input but readline provides input', async () => {
        // Mock rationale: process.argv is mocked to simulate no command-line input.
        // readlineInterface is mocked to prevent interactive prompt and provide a deterministic input.
        const mockArgv = ['node', 'index.js']; // Simulate no input
        const testInputPhrase = 'feeling wild';

        const mockReadlineInterface = {
            createInterface: () => ({
                question: (prompt, callback) => {
                    callback(testInputPhrase); // Simulate typing 'feeling wild' and pressing Enter
                },
                close: () => {}
            })
        };

        await run(mockArgv, mockReadlineInterface); // Call run with mocked argv and readlineInterface

        assert.ok(consoleOutput.some(line => line.includes('Mood: Chaotic')), `Expected "Mood: Chaotic" in output. Got: ${consoleOutput.join('\n')}`);
        assert.ok(consoleOutput.some(line => line.includes('Don your most mismatched socks')), `Expected "Don your most mismatched socks" in output. Got: ${consoleOutput.join('\n')}`);
    });
    afterEachTest();

    console.log('\nAll tests completed.');
})(); // Immediately invoked async function to run async tests
