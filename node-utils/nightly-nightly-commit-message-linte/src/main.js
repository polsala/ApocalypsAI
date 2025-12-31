#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// List of allowed commit types according to Conventional Commits
const ALLOWED_TYPES = [
  'feat', 'fix', 'docs', 'style', 'refactor', 'test',
  'chore', 'perf', 'build', 'ci', 'revert'
];

// Deterministic emoji suggestion (first in the list)
const EMOJI_SUGGESTION = '🚀';

function readStdin(callback) {
  let data = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => data += chunk);
  process.stdin.on('end', () => callback(data));
}

function loadMessage(source) {
  if (source) {
    // Treat source as a file path
    try {
      return fs.readFileSync(source, 'utf8');
    } catch (e) {
      console.error(`❌ Unable to read file: ${source}`);
      process.exit(1);
    }
  } else {
    // Read from stdin synchronously (fallback for non‑interactive environments)
    try {
      const fd = fs.openSync(0, 'r');
      const buffer = fs.readFileSync(fd, { encoding: 'utf8' });
      return buffer;
    } catch (_) {
      console.error('❌ No input provided. Pass a file path or pipe a message via stdin.');
      process.exit(1);
    }
  }
}

function validate(message) {
  const lines = message.split(/\r?\n/).filter(l => l.trim().length > 0);
  if (lines.length === 0) {
    return ['Commit message is empty.'];
  }
  const header = lines[0];
  const errors = [];

  if (header.length > 72) {
    errors.push('Header exceeds 72 characters.');
  }

  // Regex for Conventional Commit header
  const regex = /^([a-z]+)(\([^)]+\))?:\s(.+)$/;
  const match = header.match(regex);
  if (!match) {
    errors.push('Header does not match Conventional Commit format (type(scope)?: description).');
    return errors;
  }

  const [, type, , description] = match;
  if (!ALLOWED_TYPES.includes(type)) {
    errors.push(`Invalid commit type "${type}". Allowed types: ${ALLOWED_TYPES.join(', ')}.`);
  }

  if (!description[0] || description[0] !== description[0].toLowerCase()) {
    errors.push('Description should start with a lowercase letter.');
  }

  if (description.endsWith('.')) {
    errors.push('Description should not end with a period.');
  }

  return errors;
}

function suggestEmoji() {
  // Deterministic choice – always the first emoji in the list
  return EMOJI_SUGGESTION;
}

function main() {
  const args = process.argv.slice(2);
  const suggestFlag = args.includes('--suggest-emoji');
  const filteredArgs = args.filter(a => a !== '--suggest-emoji');
  const source = filteredArgs[0]; // may be undefined (stdin)

  const rawMessage = loadMessage(source);
  const errors = validate(rawMessage);

  if (errors.length > 0) {
    console.error('❌ Commit message validation failed:');
    errors.forEach(err => console.error(`  - ${err}`));
    process.exit(1);
  }

  let output = '✅ Commit message looks good 👍';
  if (suggestFlag) {
    output += `\n💡 Suggested emoji: ${suggestEmoji()}`;
  }
  console.log(output);
  process.exit(0);
}

if (require.main === module) {
  main();
}
