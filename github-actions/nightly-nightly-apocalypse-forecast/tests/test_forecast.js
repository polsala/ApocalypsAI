// Mock rationale: deterministic mapping based on inputs
const { generateForecast } = require('../src/forecast');

function assertEqual(actual, expected, msg) {
  if (actual !== expected) {
    console.error(`FAIL: ${msg}\n  Expected: ${expected}\n  Got: ${actual}`);
    process.exit(1);
  }
}

// Test case 1: no issues, no PRs → perfect odds, sunny emoji
const result1 = generateForecast(0, 0);
assertEqual(
  result1,
  '☀️ Apocalypse Forecast: 0 open issues, 0 open PRs. Survival odds: 100%',
  'Zero‑case forecast'
);

// Test case 2: moderate load → 70% odds, partly‑cloudy emoji
const result2 = generateForecast(5, 5);
assertEqual(
  result2,
  '🌤️ Apocalypse Forecast: 5 open issues, 5 open PRs. Survival odds: 70%',
  'Mid‑load forecast'
);

console.log('All tests passed');
