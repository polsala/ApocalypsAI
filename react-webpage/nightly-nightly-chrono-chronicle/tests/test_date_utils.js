const assert = require('assert');
const { formatDate, getPrediction } = require('../src/date-utils');

function testFormatDate() {
  const date = new Date('2023-01-01T00:00:00Z');
  const formatted = formatDate(date);
  if (!formatted.includes('January')) throw new Error('Month missing');
  if (!formatted.includes('1, 2023')) throw new Error('Year or day missing');
}

function testPredictions() {
  for (let d = 0; d < 7; d++) {
    const date = new Date(2023, 0, 2 + d);
    const pred = getPrediction(date);
    if (typeof pred !== 'string' || pred.length === 0) throw new Error('Invalid prediction');
  }
}

try {
  testFormatDate();
  testPredictions();
  console.log('All tests passed');
} catch (e) {
  console.error(e);
  process.exit(1);
}
