const assert = require('assert');
const { generateCommutePlan, transports, destinations, anomalies } = require('../src/index');

// Mock rationale: Math.random is non-deterministic, so we mock it to ensure
// predictable outcomes for our tests. This allows us to test specific scenarios
// and ensure the utility correctly selects elements from its predefined lists.
function mockMathRandom(values) {
    let i = 0;
    const originalMathRandom = Math.random;
    Math.random = () => {
        const value = values[i % values.length];
        i++;
        return value;
    };
    return () => {
        Math.random = originalMathRandom; // Restore original Math.random
    };
}

function runTest(name, fn) {
    try {
        fn();
        console.log(`\u2713 ${name}`); // Checkmark symbol
    } catch (error) {
        console.error(`\u2717 ${name}`); // Cross symbol
        console.error(error);
        process.exit(1);
    }
}

runTest('should generate a plan with valid elements from the predefined lists', () => {
    // Mock rationale: Provide a sequence of random numbers to ensure each category
    // (transport, destination, anomaly) gets a valid index within its array.
    const restoreMathRandom = mockMathRandom([0.1, 0.5, 0.9]);

    const plan = generateCommutePlan();

    assert.ok(transports.includes(plan.transport), `Transport "${plan.transport}" is not in the list.`);
    assert.ok(destinations.includes(plan.destination), `Destination "${plan.destination}" is not in the list.`);
    assert.ok(anomalies.includes(plan.anomaly), `Anomaly "${plan.anomaly}" is not in the list.`);

    restoreMathRandom();
});

runTest('should return the first elements when Math.random is mocked to zero', () => {
    // Mock rationale: Test the selection of the first element in each array
    // by forcing Math.random to return 0, which maps to index 0.
    const restoreMathRandom = mockMathRandom([
        0, // Forces transports[0]
        0, // Forces destinations[0]
        0  // Forces anomalies[0]
    ]);

    const plan = generateCommutePlan();

    assert.strictEqual(plan.transport, transports[0], 'Expected first transport');
    assert.strictEqual(plan.destination, destinations[0], 'Expected first destination');
    assert.strictEqual(plan.anomaly, anomalies[0], 'Expected first anomaly');

    restoreMathRandom();
});

runTest('should return the last elements when Math.random is mocked to values near one', () => {
    // Mock rationale: Test the selection of the last element in each array
    // by forcing Math.random to return a value just under 1, which maps to the last index.
    const restoreMathRandom = mockMathRandom([
        0.9999, // Forces transports[length - 1]
        0.9999, // Forces destinations[length - 1]
        0.9999  // Forces anomalies[length - 1]
    ]);

    const plan = generateCommutePlan();

    assert.strictEqual(plan.transport, transports[transports.length - 1], 'Expected last transport');
    assert.strictEqual(plan.destination, destinations[destinations.length - 1], 'Expected last destination');
    assert.strictEqual(plan.anomaly, anomalies[anomalies.length - 1], 'Expected last anomaly');

    restoreMathRandom();
});

console.log("\nAll tests completed.");
