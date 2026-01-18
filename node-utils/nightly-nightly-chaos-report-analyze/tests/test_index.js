"use strict";

const test = require('node:test');
const assert = require('node:assert');
const analyzeReport = require('../src/index.js');

// Mock rationale: Avoid file I/O and network calls by directly testing the core logic with in-memory data.

test('analyzeReport computes correct resilience score', () => {
  const report = { total_tests: 100, failed_tests: 10, failures: [] };
  const result = analyzeReport(report);
  assert.strictEqual(result.resilienceScore, 90);
});

test('analyzeReport handles zero tests', () => {
  const report = { total_tests: 0, failed_tests: 0, failures: [] };
  const result = analyzeReport(report);
  assert.strictEqual(result.resilienceScore, 100);
});

test('analyzeReport identifies top failure categories', () => {
  const report = {
    total_tests: 10,
    failed_tests: 4,
    failures: [
      { category: 'network' },
      { category: 'resource' },
      { category: 'network' },
      { category: 'service' },
      { category: 'network' },
    ],
  };
  const result = analyzeReport(report);
  assert.deepStrictEqual(result.topFailures, [
    { category: 'network', count: 3 },
    { category: 'resource', count: 1 },
    { category: 'service', count: 1 },
  ]);
});
