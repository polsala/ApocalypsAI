#!/usr/bin/env node

// Mock rationale: This utility is designed to be standalone and does not rely on external services for its core functionality. All data is generated internally.

const RA_HOURS = 24;
const RA_MINUTES = 60;
const RA_SECONDS = 60;
const DEC_DEGREES = 90;
const DEC_MINUTES = 60;
const DEC_SECONDS = 60;

const STAR_SYSTEM_PREFIXES = [
  "Astro", "Cosmo", "Galacto", "Nebulo", "Stellar", "Xeno", "Zeta", "Orion", "Sirius", "Vega"
];
const STAR_SYSTEM_SUFFIXES = [
  "Prime", "Minor", "Major", "Station", "Colony", "Nexus", "Haven", "Reach", "Point", "Gate"
];

const NEBULA_ADJECTIVES = [
  "Whispering", "Shimmering", "Crimson", "Azure", "Emerald", "Golden", "Veiled", "Silent", "Echoing", "Radiant"
];
const NEBULA_NOUNS = [
  "Veil", "Cloud", "Mist", "Sea", "River", "Garden", "Heart", "Eye", "Tapestry", "Aurora"
];

const WARP_LANE_PREFIXES = [
  "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Nexus", "Orion", "Pegasus", "Cygnus", "Lyra"
];
const WARP_LANE_NUMBERS = [
  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "X", "XII", "XXI"
];

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function formatRa() {
  const hours = getRandomInt(RA_HOURS);
  const minutes = getRandomInt(RA_MINUTES);
  const seconds = getRandomInt(RA_SECONDS);
  return `${hours}h ${minutes}m ${seconds}s`;
}

function formatDec() {
  const degrees = getRandomInt(DEC_DEGREES);
  const minutes = getRandomInt(DEC_MINUTES);
  const seconds = getRandomInt(DEC_SECONDS);
  const sign = Math.random() < 0.5 ? '-' : '+';
  return `${sign}${degrees}° ${minutes}′ ${seconds}″`;
}

function generateStarSystem() {
  const prefix = STAR_SYSTEM_PREFIXES[getRandomInt(STAR_SYSTEM_PREFIXES.length)];
  const suffix = STAR_SYSTEM_SUFFIXES[getRandomInt(STAR_SYSTEM_SUFFIXES.length)];
  return `${prefix} ${suffix}`;
}

function generateNebula() {
  const adjective = NEBULA_ADJECTIVES[getRandomInt(NEBULA_ADJECTIVES.length)];
  const noun = NEBULA_NOUNS[getRandomInt(NEBULA_NOUNS.length)];
  return `${adjective} ${noun}`;
}

function generateWarpLane() {
  const prefix = WARP_LANE_PREFIXES[getRandomInt(WARP_LANE_PREFIXES.length)];
  const number = WARP_LANE_NUMBERS[getRandomInt(WARP_LANE_NUMBERS.length)];
  return `${prefix}-${number}`;
}

function generateCosmicCoordinates() {
  const starSystem = generateStarSystem();
  const ra = formatRa();
  const dec = formatDec();
  const nebula = generateNebula();
  const warpLane = generateWarpLane();

  console.log("Navigating towards:");
  console.log(`  Star System: ${starSystem}`);
  console.log(`  Coordinates: RA ${ra}, Dec ${dec}`);
  console.log(`  Nebula: ${nebula}`);
  console.log(`  Warp Lane: ${warpLane}`);
  console.log("\nMay your journey be swift and your discoveries wondrous!");
}

if (require.main === module) {
  generateCosmicCoordinates();
}

module.exports = { generateCosmicCoordinates };
