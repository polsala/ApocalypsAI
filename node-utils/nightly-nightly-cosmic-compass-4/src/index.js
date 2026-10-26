#!/usr/bin/env node

const DIRECTIONS = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest'];
const COSMIC_WHISPERS = [
  "The void whispers secrets of innovation.",
  "Align with the stellar currents for clarity.",
  "A gentle cosmic breeze guides your next thought.",
  "Feel the gravitational pull of new ideas.",
  "The nebulae swirl, revealing hidden paths.",
  "Embrace the cosmic dust, for it holds wisdom.",
  "Starlight illuminates your creative core.",
  "The universe conspires to inspire you."
];

function generateHash(seed) {
  let hash = 0;
  if (seed.length === 0) return hash;
  for (let i = 0; i < seed.length; i++) {
    const char = seed.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

function getCosmicGuidance(seed = String(Date.now())) {
  const hash = generateHash(seed);
  const directionIndex = hash % DIRECTIONS.length;
  const whisperIndex = hash % COSMIC_WHISPERS.length;

  const direction = DIRECTIONS[directionIndex];
  const whisper = COSMIC_WHISPERS[whisperIndex];

  return { direction, whisper, seed };
}

function main() {
  const args = process.argv.slice(2);
  let seed = args[0];

  if (!seed) {
    console.log("No seed provided. Using current timestamp for cosmic alignment.");
  }

  const { direction, whisper, seed: usedSeed } = getCosmicGuidance(seed);

  console.log("\n--- Nightly Cosmic Compass ---");
  console.log(`Seed used: "${usedSeed}"`);
  console.log(`Your Cosmic Direction: \x1b[1m${direction}\x1b[0m`); // Bold
  console.log(`Cosmic Whisper: \x1b[36m${whisper}\x1b[0m`); // Cyan
  console.log("----------------------------\n");
}

// Allow direct execution or module import for testing
if (require.main === module) {
  main();
} else {
  module.exports = { getCosmicGuidance, generateHash, DIRECTIONS, COSMIC_WHISPERS };
}
