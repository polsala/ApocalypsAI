const assert = require('assert');
const { generateCalendar } = require('../src/emoji-calendar.js');

// Test: January 2023 â the 1st is a Sunday, so the first token should be âï¸01
const lines = generateCalendar(1, 2023);
assert(lines.length > 0, 'Calendar should contain at least one week');
assert(lines[0].startsWith('âï¸01'), `Expected first day to be âï¸01, got ${lines[0]}`);

// Test: February 2023 â the 1st is a Wednesday (ð)
const febLines = generateCalendar(2, 2023);
// Find the token for day 1
const firstWeekTokens = febLines[0].trim().split(/\s+/);
const day1Token = firstWeekTokens.find(tok => tok.endsWith('01'));
assert(day1Token === 'ð01', `Expected February 1 2023 to be ð01, got ${day1Token}`);

console.log('All emoji-calendar tests passed.');

