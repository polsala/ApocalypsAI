const { execSync } = require("child_process");
const { parseISO8601Duration, formatDuration } = require("../src/index.js");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || "Assertion failed");
  }
}

// Test parsing
let d = parseISO8601Duration("PT2H30M");
assert(d.hours === 2, "Hours should be 2");
assert(d.minutes === 30, "Minutes should be 30");
assert(d.seconds === 0, "Seconds should be 0");

// Test parsing with seconds
d = parseISO8601Duration("PT45S");
assert(d.hours === 0, "Hours should be 0");
assert(d.minutes === 0, "Minutes should be 0");
assert(d.seconds === 45, "Seconds should be 45");

// Test formatting
let f = formatDuration({hours:1, minutes:0, seconds:0});
assert(f === "1 hour", "Formatting 1 hour");

f = formatDuration({hours:0, minutes:5, seconds:0});
assert(f === "5 minutes", "Formatting minutes");

f = formatDuration({hours:0, minutes:0, seconds:12.5});
assert(f === "12.50 seconds", "Formatting seconds with fraction");

// Test CLI output
let output = execSync('node src/index.js "PT1H15M"', { encoding: "utf8" }).trim();
assert(output === "1 hour, 15 minutes", "CLI output mismatch");

// Test invalid input handling
let threw = false;
try {
  parseISO8601Duration("invalid");
} catch (e) {
  threw = true;
}
assert(threw, "Invalid input should throw");

console.log("All tests passed");
