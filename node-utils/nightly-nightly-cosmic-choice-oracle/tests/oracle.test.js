const assert = require('assert');
const { getSuggestion, getCosmicIndex, cosmicAlignments } = require('../src/oracle');

// Mock rationale: The core logic relies on deterministic hashing and modulo operations
// to select suggestions. No external APIs or random numbers are used, so no complex
// mocking is required. The tests directly verify the deterministic output of the
// `getCosmicIndex` and `getSuggestion` functions.

function runTest(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

runTest('getCosmicIndex should return a deterministic positive integer for a given string', () => {
    const index1 = getCosmicIndex("hello world");
    const index2 = getCosmicIndex("hello world");
    const index3 = getCosmicIndex("another string");

    assert.strictEqual(index1, index2, 'Indexes for identical strings should be the same');
    assert.notStrictEqual(index1, index3, 'Indexes for different strings should be different');
    assert.ok(index1 >= 0, 'Index should be positive');
});

runTest('getSuggestion should return a deterministic suggestion for a given input', () => {
    const suggestion1 = getSuggestion("feeling lost");
    const suggestion2 = getSuggestion("feeling lost");
    const suggestion3 = getSuggestion("feeling inspired");

    assert.strictEqual(suggestion1, suggestion2, 'Suggestions for identical inputs should be the same');
    assert.notStrictEqual(suggestion1, suggestion3, 'Suggestions for different inputs should be different');
    assert.ok(typeof suggestion1 === 'string', 'Suggestion should be a string');
    assert.ok(suggestion1.includes("The "), 'Suggestion should contain alignment name');
    assert.ok(suggestion1.includes(" whispers: '"), 'Suggestion should contain the phrase');
});

runTest('getSuggestion should handle empty input deterministically', () => {
    const defaultSuggestion = getSuggestion("");
    const explicitDefaultSuggestion = getSuggestion("default cosmic query"); // This is what the function calls internally
    assert.strictEqual(defaultSuggestion, explicitDefaultSuggestion, 'Empty input should map to a deterministic default suggestion');
    assert.ok(defaultSuggestion.length > 0, 'Default suggestion should not be empty');
});

runTest('All cosmic alignments should have suggestions', () => {
    cosmicAlignments.forEach(alignment => {
        assert.ok(alignment.suggestions.length > 0, `Alignment "${alignment.name}" should have suggestions`);
    });
});

runTest('Specific input should map to a known alignment and suggestion (spot check)', () => {
    // Let's manually calculate for "feeling lost"
    const input = "feeling lost";
    const cosmicIndex = getCosmicIndex(input.toLowerCase());
    const alignmentIndex = cosmicIndex % cosmicAlignments.length;
    const expectedAlignment = cosmicAlignments[alignmentIndex];
    const suggestionIndex = cosmicIndex % expectedAlignment.suggestions.length;
    const expectedSuggestionText = expectedAlignment.suggestions[suggestionIndex];

    const actualSuggestion = getSuggestion(input);
    const expectedOutput = `${expectedAlignment.emoji} The ${expectedAlignment.name} whispers: '${expectedSuggestionText}'`;

    assert.strictEqual(actualSuggestion, expectedOutput, `Suggestion for "${input}" should match expected output`);
});

console.log('\nAll tests passed!');
