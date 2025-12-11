const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');

// Mock rationale: We are mocking the random number generator to ensure deterministic test results.
// This allows us to test specific branches of the logic.
let mockMath = Object.create(global.Math);
mockMath.random = () => 0.2; // This will trigger the structured greeting path
global.Math = mockMath;

const scriptPath = path.join(__dirname, '../src/main.js');

function runScript() {
  try {
    return execSync(`node ${scriptPath}`, { encoding: 'utf-8' }).trim();
  } catch (error) {
    console.error(`Error executing script: ${error.message}`);
    return null;
  }
}

// Test case 1: Ensure the script runs and produces output.
console.log('Test 1: Script execution and output presence');
const output1 = runScript();
assert(output1 !== null, 'Test 1 Failed: Script did not produce any output.');
assert(output1.length > 0, 'Test 1 Failed: Output is empty.');
console.log('Test 1 Passed.');

// Test case 2: Verify output format when Math.random() is set to a value that triggers the structured greeting.
console.log('Test 2: Structured greeting format');
// Re-mocking Math.random for this specific test case to ensure it hits the structured path
let mockMathStructured = Object.create(global.Math);
mockMathStructured.random = () => 0.2; // Triggers structured greeting
global.Math = mockMathStructured;

const output2 = runScript();
// Expected format: "<Greeting> <Interjection> <Celestial Object>?"
// We can't predict the exact phrase, but we can check for the presence of key components.
const expectedKeywords = [
  "fellow stardust", "cosmic expanse", "traveler of the nebulae", "solar cycle", "the void", // Greetings
  "Have you seen", "Did you notice", "I was just pondering", "My sensors detected", "It's quite remarkable", // Interjections
  "nebula", "asteroid", "stars", "comet", "galaxy" // Celestial Objects (partial check)
];

let containsExpectedKeyword = false;
for (const keyword of expectedKeywords) {
  if (output2.includes(keyword)) {
    containsExpectedKeyword = true;
    break;
  }
}
assert(containsExpectedKeyword, `Test 2 Failed: Output "${output2}" does not seem to follow the structured greeting format.`);
assert(output2.endsWith('?'), `Test 2 Failed: Structured greeting does not end with a question mark.`);
console.log('Test 2 Passed.');

// Test case 3: Verify output when Math.random() is set to a value that triggers a freeform theme.
console.log('Test 3: Freeform theme selection');
// Re-mocking Math.random for this specific test case to ensure it hits the theme path
let mockMathTheme = Object.create(global.Math);
mockMathTheme.random = () => 0.8; // Triggers theme
global.Math = mockMathTheme;

const output3 = runScript();
const freeformThemes = [
  "My warp drive is feeling a bit sluggish today. Perhaps a cosmic coffee?",
  "Beware the gravitational pull of existential dread, but enjoy the view!",
  "I think I saw a space whale migrating through the Kuiper Belt.",
  "The silence out here is deafening, yet strangely comforting.",
  "Is it just me, or is that black hole looking particularly hungry today?",
  "I'm trying to teach my pet quasar new tricks.",
  "The quantum foam is particularly bubbly this cycle."
];
assert(freeformThemes.includes(output3), `Test 3 Failed: Output "${output3}" is not one of the expected freeform themes.`);
console.log('Test 3 Passed.');

// Restore original Math.random
global.Math = require('math');

console.log('\nAll tests completed successfully!');
