#!/usr/bin/env node

/**
 * Nightly Strong Pass
 * A whimsical CLI that checks password strength.
 */

const process = require('process');
const readline = require('readline');

/**
 * Evaluate password strength.
 * @param {string} pwd
 * @returns {{score: number, suggestions: string[]}}
 */
function evaluate(pwd) {
  let score = 0;
  const length = pwd.length;
  const hasLower = /[a-z]/.test(pwd);
  const hasUpper = /[A-Z]/.test(pwd);
  const hasDigit = /[0-9]/.test(pwd);
  const hasSymbol = /[^a-zA-Z0-9]/.test(pwd);

  // Length
  if (length >= 8) score += 20;
  if (length >= 12) score += 20;
  if (length >= 16) score += 20;

  // Variety
  const variety = [hasLower, hasUpper, hasDigit, hasSymbol].filter(Boolean).length;
  score += variety * 10;

  // Randomness heuristic: penalize repeated chars
  const repeats = (pwd.match(/(.)\1+/g) || []).length;
  score -= repeats * 5;

  if (score < 0) score = 0;
  if (score > 100) score = 100;

  const suggestions = [];
  if (!hasLower) suggestions.push('Add lowercase letters');
  if (!hasUpper) suggestions.push('Add uppercase letters');
  if (!hasDigit) suggestions.push('Add digits');
  if (!hasSymbol) suggestions.push('Add symbols');
  if (length < 12) suggestions.push('Increase length');

  return { score, suggestions };
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-strong-pass <password>');
    process.exit(1);
  }
  const pwd = args[0];
  const { score, suggestions } = evaluate(pwd);

  let message;
  if (score >= 80) message = 'Your password is very strong.';
  else if (score >= 60) message = 'Your password is moderately strong.';
  else if (score >= 40) message = 'Your password is weak.';
  else message = 'Your password is very weak.';

  console.log(message);
  if (suggestions.length > 0) {
    console.log('Suggestions:');
    suggestions.forEach(s => console.log('- ' + s));
  }
}

if (require.main === module) {
  main();
}

module.exports = { evaluate };
