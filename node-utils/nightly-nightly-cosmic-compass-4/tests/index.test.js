const { getCosmicGuidance, generateHash, DIRECTIONS, COSMIC_WHISPERS } = require('../src/index');

function assert(condition, message) {
  if (!condition) {
    console.error(`❌ Test failed: ${message}`);
    process.exit(1);
  }
}

console.log("Running tests for Nightly Cosmic Compass...");

// Mock rationale: We need deterministic results for testing, so we mock Date.now()
// to control the seed when no explicit seed is provided.
const originalDateNow = Date.now;

// Test 1: Deterministic output with a fixed seed
const seed1 = "apocalypsai";
const guidance1 = getCosmicGuidance(seed1);
assert(guidance1.direction === "Southwest", `Test 1 Failed: Expected Southwest, got ${guidance1.direction}`);
assert(guidance1.whisper === "The nebulae swirl, revealing hidden paths.", `Test 1 Failed: Expected specific whisper, got ${guidance1.whisper}`);
assert(guidance1.seed === seed1, `Test 1 Failed: Expected seed ${seed1}, got ${guidance1.seed}`);
console.log("✅ Test 1: Deterministic output with fixed seed passed.");

// Test 2: Deterministic output with a different fixed seed
const seed2 = "integrator";
const guidance2 = getCosmicGuidance(seed2);
assert(guidance2.direction === "Northwest", `Test 2 Failed: Expected Northwest, got ${guidance2.direction}`);
assert(guidance2.whisper === "The void whispers secrets of innovation.", `Test 2 Failed: Expected specific whisper, got ${guidance2.whisper}`);
assert(guidance2.seed === seed2, `Test 2 Failed: Expected seed ${seed2}, got ${guidance2.seed}`);
console.log("✅ Test 2: Deterministic output with different fixed seed passed.");

// Test 3: Output without a provided seed (mock Date.now)
Date.now = () => 1678886400000; // Mock rationale: Fixed timestamp for deterministic 'no seed' test
const guidance3 = getCosmicGuidance();
assert(guidance3.direction === "North", `Test 3 Failed: Expected North, got ${guidance3.direction}`);
assert(guidance3.whisper === "The universe conspires to inspire you.", `Test 3 Failed: Expected specific whisper, got ${guidance3.whisper}`);
assert(guidance3.seed === "1678886400000", `Test 3 Failed: Expected seed '1678886400000', got ${guidance3.seed}`);
console.log("✅ Test 3: Output with mocked Date.now() passed.");

// Test 4: Hash generation consistency
const testHash1 = generateHash("hello");
const testHash2 = generateHash("world");
assert(testHash1 === 99162322, `Test 4 Failed: Expected hash 99162322, got ${testHash1}`);
assert(testHash2 === 113318802, `Test 4 Failed: Expected hash 113318802, got ${testHash2}`);
console.log("✅ Test 4: Hash generation consistency passed.");

// Test 5: Empty seed should use Date.now() (mocked)
Date.now = () => 1678886400001; // Mock rationale: Another fixed timestamp for deterministic 'empty seed' test
const guidance4 = getCosmicGuidance("");
assert(guidance4.direction === "North", `Test 5 Failed: Expected North, got ${guidance4.direction}`);
assert(guidance4.whisper === "The universe conspires to inspire you.", `Test 5 Failed: Expected specific whisper, got ${guidance4.whisper}`);
assert(guidance4.seed === "1678886400001", `Test 5 Failed: Expected seed '1678886400001', got ${guidance4.seed}`);
console.log("✅ Test 5: Empty seed uses mocked Date.now() passed.");


// Restore original Date.now
Date.now = originalDateNow;

console.log("\nAll tests passed!");
