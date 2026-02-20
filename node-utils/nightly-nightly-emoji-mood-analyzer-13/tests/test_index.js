// nightly-emoji-mood-analyzer tests
// Mock rationale: No external resources are required; tests are pure functions.

const assert = require("assert");
const { analyzeMood } = require("../src/index");

function runTests() {
  // Positive dominant
  const posText = "I am happy and love this awesome day!";
  assert.strictEqual(analyzeMood(posText), "😊", "Positive text should yield 😊");

  // Negative dominant
  const negText = "I am sad, angry and hate this terrible weather.";
  assert.strictEqual(analyzeMood(negText), "😢", "Negative text should yield 😢");

  // Tie -> neutral
  const tieText = "I love the good but also hate the bad.";
  assert.strictEqual(analyzeMood(tieText), "😐", "Tie should yield 😐");

  // No sentiment words -> neutral
  const neutralText = "The cat sits on the mat.";
  assert.strictEqual(analyzeMood(neutralText), "😐", "No sentiment words should yield 😐");

  console.log("All tests passed.");
}

runTests();
