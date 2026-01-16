const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const { exit } = require('process');

const LOCAL_TIPS = [
  "Always carry a multi‑tool.",
  "Know how to purify water.",
  "Keep a fire starter in your bag.",
  "Have a backup power source.",
  "Learn basic first aid.",
  "Store extra food in airtight containers.",
  "Maintain a small emergency kit.",
  "Practice basic self‑defence moves.",
  "Keep a map and compass handy.",
  "Know how to signal for help."
];

const CACHE_FILE = path.join(os.homedir(), '.apocalypse_tip_cache');
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

async function getRandomTip() {
  const idx = Math.floor(Math.random() * LOCAL_TIPS.length);
  return LOCAL_TIPS[idx];
}

async function fetchTip() {
  const res = await fetch('https://api.adviceslip.com/advice', { cache: 'no-store' });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  const data = await res.json();
  return data.slip.advice;
}

async function readCache() {
  try {
    const content = await fs.readFile(CACHE_FILE, 'utf8');
    const obj = JSON.parse(content);
    if (Date.now() - obj.timestamp < CACHE_TTL_MS) {
      return obj.tip;
    }
  } catch (_) {}
  return null;
}

async function writeCache(tip) {
  const obj = { tip, timestamp: Date.now() };
  await fs.writeFile(CACHE_FILE, JSON.stringify(obj), 'utf8');
}

async function getTip({ useApi = false, force = false } = {}) {
  if (useApi) {
    const tip = await fetchTip();
    await writeCache(tip);
    return tip;
  }
  const cached = await readCache();
  if (cached && !force) return cached;
  const tip = await getRandomTip();
  await writeCache(tip);
  return tip;
}

async function main() {
  const args = process.argv.slice(2);
  const useApi = args.includes('--api');
  const force = args.includes('--force');
  try {
    const tip = await getTip({ useApi, force });
    console.log(tip);
  } catch (err) {
    console.error('Error:', err.message);
    exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { getRandomTip, fetchTip, readCache, writeCache, getTip };
