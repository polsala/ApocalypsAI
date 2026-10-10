// tests/test_main.js
const { getAdjective, run } = require('../src/main');

// Mock Math.random to be deterministic
Math.random = () => 0.5; // selects middle adjective (index 5)

// Capture console.log output
let output = "";
const originalLog = console.log;
console.log = (msg) => { output = msg; };

process.env.GITHUB_REPOSITORY = "polsala/ApocalypsAI";

run();

// Restore original console.log
console.log = originalLog;

// Simple assertion
if (output !== "Whimsical commit suggestion: Nebulous polsala/ApocalypsAI") {
  throw new Error(`Unexpected output: ${output}`);
} else {
  console.log("Test passed");
}
