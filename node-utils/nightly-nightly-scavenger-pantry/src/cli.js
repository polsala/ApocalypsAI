#!/usr/bin/env node
const { addItem, listItems, getExpiringItems } = require('./util');
const path = require('path');
const fs = require('fs');

function ensureDataFile() {
  const dataPath = path.join(__dirname, '..', 'data.json');
  if (!fs.existsSync(dataPath)) {
    fs.writeFileSync(dataPath, '[]', 'utf8');
  }
}
ensureDataFile();

const args = process.argv.slice(2);
const command = args[0];

if (command === 'add') {
  const [name, days] = args.slice(1);
  try {
    addItem(name, days);
    console.log(`Added "${name}" expiring in ${days} days.`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
} else if (command === 'list') {
  const items = listItems();
  if (items.length === 0) {
    console.log('No items stored.');
  } else {
    items.forEach(i => {
      const d = new Date(i.expireAt);
      console.log(`${i.name} – expires on ${d.toISOString().split('T')[0]}`);
    });
  }
} else if (command === 'check') {
  const items = getExpiringItems();
  if (items.length === 0) {
    console.log('No items expiring within 7 days.');
  } else {
    console.log('Expiring soon:');
    items.forEach(i => {
      const d = new Date(i.expireAt);
      console.log(`${i.name} – expires on ${d.toISOString().split('T')[0]}`);
    });
  }
} else {
  console.log('Usage: node src/cli.js <add|list|check> [args]');
  process.exit(1);
}
