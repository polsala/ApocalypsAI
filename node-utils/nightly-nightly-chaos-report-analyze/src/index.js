"use strict";

const fs = require('fs');
const yaml = require('js-yaml');

function parseReport(inputPath) {
  const content = fs.readFileSync(inputPath, 'utf-8');
  if (inputPath.endsWith('.yaml') || inputPath.endsWith('.yml')) {
    return yaml.load(content);
  }
  return JSON.parse(content);
}

function computeResilienceScore(total, failed) {
  if (total === 0) return 100;
  return Math.max(0, 100 - Math.round((failed / total) * 100));
}

function getFailureCategories(failures) {
  const categories = {};
  failures.forEach(f => {
    categories[f.category] = (categories[f.category] || 0) + 1;
  });
  return Object.entries(categories)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([category, count]) => ({ category, count }));
}

function analyzeReport(report) {
  const total = report.total_tests || 0;
  const failed = report.failed_tests || 0;
  const failures = report.failures || [];

  return {
    resilienceScore: computeResilienceScore(total, failed),
    totalTests: total,
    failedTests: failed,
    topFailures: getFailureCategories(failures),
  };
}

function cli() {
  const args = process.argv.slice(2);
  const inputIndex = args.indexOf('--input');
  if (inputIndex === -1 || !args[inputIndex + 1]) {
    console.error('Error: --input <file> is required');
    process.exit(1);
  }
  const inputPath = args[inputIndex + 1];
  try {
    const report = parseReport(inputPath);
    const result = analyzeReport(report);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Failed to analyze report:', err.message);
    process.exit(1);
  }
}

if (require.main === module) {
  cli();
}

module.exports = analyzeReport;
