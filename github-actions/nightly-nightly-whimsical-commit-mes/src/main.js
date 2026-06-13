// src/main.js
function getAdjective() {
  const adjectives = [
    "Galactic",
    "Mystic",
    "Quantum",
    "Ethereal",
    "Radiant",
    "Nebulous",
    "Arcane",
    "Luminous",
    "Celestial",
    "Spectral"
  ];
  // deterministic selection using Math.random
  const idx = Math.floor(Math.random() * adjectives.length);
  return adjectives[idx];
}

function run() {
  const repo = process.env.GITHUB_REPOSITORY || "unknown/repo";
  const adjective = getAdjective();
  const message = `Whimsical commit suggestion: ${adjective} ${repo}`;
  console.log(message);
}

// If executed directly, run
if (require.main === module) {
  run();
}

// Export for testing
module.exports = { getAdjective, run };
