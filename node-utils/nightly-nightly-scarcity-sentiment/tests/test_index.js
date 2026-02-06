const assert = require('assert');
const { calculateScarcitySentiment, scarcityFactors } = require('../src/index');

// Mock rationale: scarcityFactors is a static data object, not an external dependency.
// It's directly imported and used, so no explicit mocking is needed for its content,
// as it's part of the module under test.

function runTests() {
  console.log('Running tests for nightly-scarcity-sentiment...');

  // Test Case 1: Basic Food Item, held for 1 month
  let score1 = calculateScarcitySentiment('Can of Beans', 'food', 7, 30);
  console.log(`Test 1 (Can of Beans, food, 7, 30): ${score1}`);
  assert.strictEqual(score1, 12.2, 'Test Case 1 Failed: Basic food item score incorrect.');

  // Test Case 2: Critical Medicine, recently acquired (0 days held)
  let score2 = calculateScarcitySentiment('Antibiotics', 'medicine', 10, 0);
  console.log(`Test 2 (Antibiotics, medicine, 10, 0): ${score2}`);
  assert.strictEqual(score2, 27.5, 'Test Case 2 Failed: Critical medicine score incorrect.');

  // Test Case 3: Luxury Item, held for a long time (6 months)
  let score3 = calculateScarcitySentiment('Old Comic Book', 'luxury', 3, 180);
  console.log(`Test 3 (Old Comic Book, luxury, 3, 180): ${score3}`);
  assert.strictEqual(score3, 0.06, 'Test Case 3 Failed: Luxury item decay incorrect.');

  // Test Case 4: Tool, durable, moderate value, held for 3 months
  let score4 = calculateScarcitySentiment('Wrench', 'tools', 6, 90);
  console.log(`Test 4 (Wrench, tools, 6, 90): ${score4}`);
  assert.strictEqual(score4, 9.95, 'Test Case 4 Failed: Tool score incorrect.');

  // Test Case 5: Unknown category, falls back to 'misc', held for 10 days
  let score5 = calculateScarcitySentiment('Shiny Rock', 'unknown', 5, 10);
  console.log(`Test 5 (Shiny Rock, unknown, 5, 10): ${score5}`);
  assert.strictEqual(score5, 5.55, 'Test Case 5 Failed: Unknown category fallback incorrect.');

  // Test Case 6: Water, high value, short hold (15 days)
  let score6 = calculateScarcitySentiment('Purified Water', 'water', 9, 15);
  console.log(`Test 6 (Purified Water, water, 9, 15): ${score6}`);
  assert.strictEqual(score6, 19.92, 'Test Case 6 Failed: Water item score incorrect.');

  // Test Case 7: Fuel, high value, long hold (4 months)
  let score7 = calculateScarcitySentiment('Gasoline Can', 'fuel', 8, 120);
  console.log(`Test 7 (Gasoline Can, fuel, 8, 120): ${score7}`);
  assert.strictEqual(score7, 8.04, 'Test Case 7 Failed: Fuel item decay incorrect.');

  console.log('\nAll tests passed!');
}

runTests();
