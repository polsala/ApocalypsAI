import { renderBarChart } from '../src/graph';
import assert from 'assert';

function stripAnsi(str: string): string {
  return str.replace(/\[[0-9;]*m/gg, '');
}

// Test scaling without colour
const values = [1, 2, 5];
const chart = renderBarChart(values, { width: 10, color: false });
const lines = chart.split('
');
assert.strictEqual(lines.length, 3, 'should produce three lines');
assert.strictEqual(lines[0].length, 2, '1/5 of width 10 => 2 chars');
assert.strictEqual(lines[1].length, 4, '2/5 of width 10 => 4 chars');
assert.strictEqual(lines[2].length, 10, 'max value fills full width');

// Test colour flag adds ANSI codes
const chartColor = renderBarChart([3], { width: 6, color: true });
assert.ok(/\[3[12]m/.test(chartColor), 'ANSI colour code expected');

// Test empty input returns empty string
const empty = renderBarChart([], { width: 5 });
assert.strictEqual(empty, '', 'empty input should yield empty output');

console.log('All tests passed');
