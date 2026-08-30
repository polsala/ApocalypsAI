const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '..', 'data.json');

function loadData() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    return [];
  }
}

function saveData(items) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(items, null, 2), 'utf8');
}

/**
 * Adds an item.
 * @param {string} name
 * @param {number} daysUntilExpire
 */
function addItem(name, daysUntilExpire) {
  if (!name) throw new Error('Name required');
  const days = Number(daysUntilExpire);
  if (isNaN(days) || days < 0) throw new Error('Invalid days');
  const items = loadData();
  const now = Date.now();
  const expireAt = now + days * 24 * 60 * 60 * 1000;
  items.push({ name, expireAt });
  saveData(items);
}

/**
 * Returns all items.
 * @returns {Array<{name:string,expireAt:number}>}
 */
function listItems() {
  return loadData();
}

/**
 * Returns items expiring within the next `thresholdDays` (default 7).
 * @param {number} [thresholdDays=7]
 * @returns {Array<{name:string,expireAt:number}>}
 */
function getExpiringItems(thresholdDays = 7) {
  const now = Date.now();
  const limit = now + thresholdDays * 24 * 60 * 60 * 1000;
  return loadData().filter(item => item.expireAt <= limit);
}

module.exports = { addItem, listItems, getExpiringItems };
