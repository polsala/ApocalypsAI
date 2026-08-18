#!/usr/bin/env node

const readline = require('readline');

function hasLetter(str) {
  return /[a-zA-Z]/.test(str);
}
function hasNumber(str) {
  return /[0-9]/.test(str);
}
function hasSymbol(str) {
  return /[^a-zA-Z0-9]/.test(str);
}
function hasUpper(str) {
  return /[A-Z]/.test(str);
}
function hasLower(str) {
  return /[a-z]/.test(str);
}

function evaluate(password) {
  const len = password.length;
  const letter = hasLetter(password);
  const number = hasNumber(password);
  const symbol = hasSymbol(password);
  const upper = hasUpper(password);
  const lower = hasLower(password);

  if (len < 6) return 'Very Weak 😱';
  if (len >= 6 && (!letter || !number) && !symbol) return 'Weak 🙈';
  if (len >= 8 && letter && number && !symbol) return 'Moderate 😐';
  if (len >= 10 && letter && number && symbol && !(upper && lower)) return 'Strong 💪';
  if (len >= 12 && letter && number && symbol && upper && lower) return 'Very Strong 🚀';
  // Fallback
  return 'Moderate 😐';
}

function outputResult(pwd) {
  const rating = evaluate(pwd);
  console.log(rating);
}

function main() {
  const argPwd = process.argv[2];
  if (argPwd !== undefined) {
    outputResult(argPwd);
    return;
  }
  // No argument: read from stdin
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });
  let data = '';
  rl.on('line', (line) => {
    data += line;
  });
  rl.on('close', () => {
    outputResult(data.trim());
  });
}

if (require.main === module) {
  main();
}
