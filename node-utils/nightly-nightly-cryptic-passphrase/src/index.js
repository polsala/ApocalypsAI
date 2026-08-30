#!/usr/bin/env node

/**
 * nightly-cryptic-passphrase
 * Generate a themed passphrase composed of apocalyptic‑style words.
 */

const WORDS = [
  "ash",
  "bunker",
  "cinder",
  "dust",
  "ember",
  "flare",
  "gloom",
  "haze",
  "iron",
  "jolt",
  "kale",
  "lumen",
  "mire",
  "nexus",
  "oxide",
  "prax",
  "quell",
  "rift",
  "sable",
  "tide",
  "ultra",
  "vex",
  "waste",
  "xenon",
  "yonder",
  "zephyr"
];

/**
 * Generate a passphrase.
 * @param {Object} options
 * @param {number} [options.count=4] - Number of words.
 * @param {string} [options.delimiter='-'] - Delimiter between words.
 * @returns {string}
 */
function generatePassphrase({ count = 4, delimiter = "-" } = {}) {
  const result = [];
  for (let i = 0; i < count; i++) {
    const idx = Math.floor(Math.random() * WORDS.length);
    result.push(WORDS[idx]);
  }
  return result.join(delimiter);
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "-c" || arg === "--count") {
      options.count = parseInt(args[++i], 10);
    } else if (arg === "-d" || arg === "--delimiter") {
      options.delimiter = args[++i];
    }
  }
  const passphrase = generatePassphrase(options);
  console.log(passphrase);
}

module.exports = { generatePassphrase };
