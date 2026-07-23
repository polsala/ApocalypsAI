import { classifyItem } from '../src/index';

// Simple assertion function
function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ Test Failed: ${message}`);
    process.exit(1);
  } else {
    console.log(`✅ Test Passed: ${message}`);
  }
}

// Mock rationale: Math.random() is used in classifyItem for whimsical score variation.
// To ensure deterministic tests, we mock Math.random() to return a fixed value.
const originalMathRandom = Math.random;

function runTests() {
  console.log("Running tests for Nightly Scavenged Item Classifier...\n");

  // Test 1: Food/Water - High utility
  Math.random = () => 0.9; // Mock for high score (e.g., 0.9 * 5 + 6 = 4.5 + 6 = 10.5 -> 10)
  const foodItem = classifyItem("a dusty can of beans");
  assert(foodItem.category === 'Food/Water', 'Test 1: "can of beans" should be Food/Water');
  assert(foodItem.utilityScore === 10, 'Test 1: "can of beans" should have utility score 10');
  assert(foodItem.whimsicalRating === 'Apocalypse Essential', 'Test 1: "can of beans" should be Apocalypse Essential');

  // Test 2: Tool/Weapon - Mid-high utility
  Math.random = () => 0.6; // Mock for mid-high score (e.g., 0.6 * 6 + 4 = 3.6 + 4 = 7.6 -> 7)
  const toolItem = classifyItem("a rusty crowbar");
  assert(toolItem.category === 'Tool/Weapon', 'Test 2: "rusty crowbar" should be Tool/Weapon');
  assert(toolItem.utilityScore === 7, 'Test 2: "rusty crowbar" should have utility score 7');
  assert(toolItem.whimsicalRating === 'Quite Handy', 'Test 2: "rusty crowbar" should be Quite Handy');

  // Test 3: Resource/Material - Mid utility
  Math.random = () => 0.4; // Mock for mid score (e.g., 0.4 * 6 + 3 = 2.4 + 3 = 5.4 -> 5)
  const resourceItem = classifyItem("a coil of copper wire");
  assert(resourceItem.category === 'Resource/Material', 'Test 3: "copper wire" should be Resource/Material');
  assert(resourceItem.utilityScore === 5, 'Test 3: "copper wire" should have utility score 5');
  assert(resourceItem.whimsicalRating === 'Potentially Useful', 'Test 3: "copper wire" should be Potentially Useful');

  // Test 4: Medical/Survival - Very high utility
  Math.random = () => 0.8; // Mock for very high score (e.g., 0.8 * 5 + 7 = 4 + 7 = 11 -> 10)
  const medicalItem = classifyItem("a half-used first aid kit");
  assert(medicalItem.category === 'Medical/Survival', 'Test 4: "first aid kit" should be Medical/Survival');
  assert(medicalItem.utilityScore === 10, 'Test 4: "first aid kit" should have utility score 10');
  assert(medicalItem.whimsicalRating === 'Apocalypse Essential', 'Test 4: "first aid kit" should be Apocalypse Essential');

  // Test 5: Junk/Curiosity - Low utility
  Math.random = () => 0.1; // Mock for low score (e.g., 0.1 * 4 + 1 = 0.4 + 1 = 1.4 -> 1)
  const junkItem = classifyItem("a broken plastic toy");
  assert(junkItem.category === 'Junk/Curiosity', 'Test 5: "broken plastic toy" should be Junk/Curiosity');
  assert(junkItem.utilityScore === 1, 'Test 5: "broken plastic toy" should have utility score 1');
  assert(junkItem.whimsicalRating === 'Dust Collector', 'Test 5: "broken plastic toy" should be Dust Collector');

  // Test 6: Uncategorized item
  Math.random = () => 0.0; // Mock for lowest possible score
  const unknownItem = classifyItem("a strange glowing orb");
  assert(unknownItem.category === 'Uncategorized', 'Test 6: "strange glowing orb" should be Uncategorized');
  assert(unknownItem.utilityScore === 1, 'Test 6: "strange glowing orb" should have default low utility score');
  assert(unknownItem.whimsicalRating === 'Dust Collector', 'Test 6: "strange glowing orb" should be Dust Collector');

  // Test 7: Case insensitivity
  Math.random = () => 0.7; // Mock for high score (e.g., 0.7 * 5 + 6 = 3.5 + 6 = 9.5 -> 9)
  const caseInsensitiveItem = classifyItem("A BOTTLE of WATER");
  assert(caseInsensitiveItem.category === 'Food/Water', 'Test 7: Case insensitivity for "A BOTTLE of WATER"');
  assert(caseInsensitiveItem.utilityScore === 9, 'Test 7: Case insensitivity score for "A BOTTLE of WATER"');

  // Test 8: Multiple keywords - should pick the first match in order of checks (Food/Water first)
  Math.random = () => 0.5; // Mock for high score (e.g., 0.5 * 5 + 6 = 2.5 + 6 = 8.5 -> 8)
  const complexItem = classifyItem("a rusty knife and a half-eaten apple"); 
  assert(complexItem.category === 'Food/Water', 'Test 8: "rusty knife and half-eaten apple" should prioritize Food/Water');
  assert(complexItem.utilityScore === 8, 'Test 8: "rusty knife and half-eaten apple" should have high food score');

  console.log("\nAll tests completed.");
}

// Run tests and restore Math.random
try {
  runTests();
} finally {
  Math.random = originalMathRandom; // Restore original Math.random
}
