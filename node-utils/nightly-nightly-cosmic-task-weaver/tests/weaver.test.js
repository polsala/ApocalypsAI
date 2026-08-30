const { selectWeightedTask, getCosmicAlignment, getCosmicIntroduction, getCosmicConclusion } = require('../src/weaver');
const cosmicPhrases = require('../src/cosmicPhrases');

// Mock rationale: Math.random is non-deterministic. For reliable tests, we need to control its output.
// By providing a mock random function, we ensure that the task selection logic behaves predictably.

function runTests() {
  let passed = 0;
  let failed = 0;

  function assert(condition, message) {
    if (condition) {
      console.log(`  ✅ ${message}`);
      passed++;
    } else {
      console.error(`  ❌ ${message}`);
      failed++;
    }
  }

  console.log("Running tests for weaver.js...");

  // Test 1: Empty tasks array
  console.log("\n--- Test: Empty tasks array ---");
  const emptyTasks = [];
  assert(selectWeightedTask(emptyTasks) === null, "should return null for empty tasks array");

  // Test 2: Single task
  console.log("\n--- Test: Single task ---");
  const singleTask = [{ name: "Task A", weight: 1 }];
  assert(selectWeightedTask(singleTask, () => 0.5) === "Task A", "should select the single task");

  // Test 3: Multiple tasks, equal weight, deterministic random
  console.log("\n--- Test: Multiple tasks, equal weight ---");
  const equalWeightTasks = [
    { name: "Task A", weight: 1 },
    { name: "Task B", weight: 1 },
    { name: "Task C", weight: 1 },
  ];
  assert(selectWeightedTask(equalWeightTasks, () => 0.1) === "Task A", "should select Task A (0.1)");
  assert(selectWeightedTask(equalWeightTasks, () => 0.4) === "Task B", "should select Task B (0.4)");
  assert(selectWeightedTask(equalWeightTasks, () => 0.8) === "Task C", "should select Task C (0.8)");

  // Test 4: Multiple tasks, different weights, deterministic random
  console.log("\n--- Test: Multiple tasks, different weights ---");
  const weightedTasks = [
    { name: "High Priority", weight: 3 }, // 0-3
    { name: "Medium Priority", weight: 2 }, // 3-5
    { name: "Low Priority", weight: 1 },    // 5-6
  ]; // Total weight = 6
  assert(selectWeightedTask(weightedTasks, () => 0.1 / 6) === "High Priority", "should select High Priority (0.1)");
  assert(selectWeightedTask(weightedTasks, () => 2.9 / 6) === "High Priority", "should select High Priority (2.9)");
  assert(selectWeightedTask(weightedTasks, () => 3.1 / 6) === "Medium Priority", "should select Medium Priority (3.1)");
  assert(selectWeightedTask(weightedTasks, () => 4.9 / 6) === "Medium Priority", "should select Medium Priority (4.9)");
  assert(selectWeightedTask(weightedTasks, () => 5.1 / 6) === "Low Priority", "should select Low Priority (5.1)");
  assert(selectWeightedTask(weightedTasks, () => 5.9 / 6) === "Low Priority", "should select Low Priority (5.9)");

  // Test 5: Tasks with default weight (undefined weight)
  console.log("\n--- Test: Tasks with default weight ---");
  const defaultWeightTasks = [
    { name: "Task X" },
    { name: "Task Y", weight: 2 },
    { name: "Task Z" },
  ]; // Total weight = 1 + 2 + 1 = 4
  assert(selectWeightedTask(defaultWeightTasks, () => 0.5 / 4) === "Task X", "should select Task X (0.5)");
  assert(selectWeightedTask(defaultWeightTasks, () => 1.5 / 4) === "Task Y", "should select Task Y (1.5)");
  assert(selectWeightedTask(defaultWeightTasks, () => 3.5 / 4) === "Task Z", "should select Task Z (3.5)");

  // Test 6: Phrase generation (deterministic by mocking Math.random)
  console.log("\n--- Test: Phrase generation ---");
  // Mock rationale: Phrase selection relies on Math.random. Mocking it ensures specific phrases are chosen for testing.
  const mockRandomFn = (index) => () => index / cosmicPhrases.alignments.length;
  assert(getCosmicAlignment(mockRandomFn(0)) === cosmicPhrases.alignments[0], "should get the first alignment phrase");
  assert(getCosmicAlignment(mockRandomFn(1)) === cosmicPhrases.alignments[1], "should get the second alignment phrase");

  const mockRandomIntroFn = (index) => () => index / cosmicPhrases.introductions.length;
  assert(getCosmicIntroduction(mockRandomIntroFn(0)) === cosmicPhrases.introductions[0], "should get the first introduction phrase");

  const mockRandomConclusionFn = (index) => () => index / cosmicPhrases.conclusions.length;
  assert(getCosmicConclusion(mockRandomConclusionFn(0)) === cosmicPhrases.conclusions[0], "should get the first conclusion phrase");


  console.log(`\nTests finished: ${passed} passed, ${failed} failed.`);
  if (failed > 0) {
    process.exit(1);
  }
}

runTests();
