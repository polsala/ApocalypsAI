#!/usr/bin/env node
/**
 * nightly-issue-label-suggester
 * Suggests GitHub issue labels based on title keywords.
 */

function suggestLabels(title) {
  if (typeof title !== 'string') return [];
  const map = {
    bug: ['bug'],
    error: ['bug'],
    fail: ['bug'],
    crash: ['bug'],
    broken: ['bug'],
    feature: ['enhancement'],
    add: ['enhancement'],
    implement: ['enhancement'],
    improve: ['enhancement'],
    upgrade: ['enhancement'],
    doc: ['documentation'],
    docs: ['documentation'],
    readme: ['documentation'],
    documentation: ['documentation'],
    test: ['testing'],
    ci: ['ci'],
    build: ['ci'],
    refactor: ['refactor'],
    performance: ['performance'],
    security: ['security'],
    deps: ['dependencies'],
    dependency: ['dependencies'],
    chore: ['chore']
  };
  const lower = title.toLowerCase();
  const words = lower.split(/\\s+/);
  const labels = new Set();
  for (const word of words) {
    if (map[word]) {
      map[word].forEach(l => labels.add(l));
    }
  }
  if (labels.size === 0) {
    labels.add('question');
  }
  return Array.from(labels);
}

// CLI mode
if (require.main === module) {
  const title = process.argv[2] || '';
  const result = suggestLabels(title);
  console.log(JSON.stringify(result));
}

module.exports = { suggestLabels };
