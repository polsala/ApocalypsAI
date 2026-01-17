#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getFortunes() {
  const fortunesPath = path.join(__dirname, 'fortunes.json');
  const data = fs.readFileSync(fortunesPath, 'utf8');
  return JSON.parse(data);
}

function getRandomFortune() {
  const fortunes = getFortunes();
  const idx = Math.floor(Math.random() * fortunes.length);
  return fortunes[idx];
}

function main() {
  console.log(getRandomFortune());
}

if (require.main === module) {
  main();
}

module.exports = { getRandomFortune, getFortunes };
