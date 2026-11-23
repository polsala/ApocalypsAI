#!/usr/bin/env node

const { getSuggestion } = require('./oracle');

const args = process.argv.slice(2);
const input = args.join(' ').trim();

if (!input) {
    console.log("🌌 Provide a query to consult the cosmic oracle! E.g., 'node src/index.js \"feeling lost\"'");
    process.exit(1);
}

const suggestion = getSuggestion(input);
console.log(suggestion);
