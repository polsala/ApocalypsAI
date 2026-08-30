const mapping = {
  A: 'Ashen',
  B: 'Bunker',
  C: 'Cinder',
  D: 'Dust',
  E: 'Eclipse',
  F: 'Feral',
  G: 'Grit',
  H: 'Hollow',
  I: 'Irradiated',
  J: 'Junk',
  K: 'Kale',
  L: 'Lurker',
  M: 'Mire',
  N: 'Nexus',
  O: 'Obsidian',
  P: 'Purge',
  Q: 'Quake',
  R: 'Rubble',
  S: 'Scavenge',
  T: 'Toxic',
  U: 'Utopia',
  V: 'Vault',
  W: 'Wasteland',
  X: 'Xenon',
  Y: 'Yield',
  Z: 'Zephyr',
  ' ': '/'
};

/**
 * Encode a plain‑text string into the wasteland radio code.
 * Non‑alphabetic characters (except space) are left unchanged.
 * @param {string} text Input phrase
 * @returns {string} Encoded phrase
 */
function encode(text) {
  return text
    .toUpperCase()
    .split('')
    .map(ch => mapping[ch] || ch)
    .join(' ');
}

// CLI handling – only runs when executed directly
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/index.js <phrase>');
    process.exit(1);
  }
  console.log(encode(input));
}

module.exports = { encode };
