const crypto = require('crypto');

/**
 * Generates a deterministic 'cosmic direction' based on time and a cosmic event.
 * @param {string} cosmicEvent - A string describing a cosmic event.
 * @returns {{direction: string, description: string}}
 */
function getCosmicDirection(cosmicEvent) {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();

  // Combine time components and event string for hashing
  const timeString = `${hours}:${minutes}:${seconds}`;
  const inputString = `${timeString}-${cosmicEvent}`;

  // Use SHA256 for a good distribution of hash values
  const hash = crypto.createHash('sha256').update(inputString).digest('hex');

  // Convert the first few characters of the hash to a number
  // We'll use the first 8 hex characters (32 bits) for our angle calculation
  const angleValue = parseInt(hash.substring(0, 8), 16);

  // Map the angle value (0 to 2^32 - 1) to a compass direction (0 to 360 degrees)
  const angle = (angleValue / 0xFFFFFFFF) * 360;

  // Determine the cardinal direction
  let direction = '';
  if (angle >= 337.5 || angle < 22.5) {
    direction = 'North';
  } else if (angle >= 22.5 && angle < 67.5) {
    direction = 'North-East';
  } else if (angle >= 67.5 && angle < 112.5) {
    direction = 'East';
  } else if (angle >= 112.5 && angle < 157.5) {
    direction = 'South-East';
  } else if (angle >= 157.5 && angle < 202.5) {
    direction = 'South';
  } else if (angle >= 202.5 && angle < 247.5) {
    direction = 'South-West';
  } else if (angle >= 247.5 && angle < 292.5) {
    direction = 'West';
  } else {
    direction = 'North-West';
  }

  // Whimsical descriptions based on direction
  const descriptions = {
    'North': 'Towards the Great Nebula of Serenity, where stardust whispers secrets.',
    'North-East': 'Guiding you to the shimmering Aurora of Possibilities, where dreams take flight.',
    'East': 'Leading you to the Dawn of Creation, where new galaxies are born.',
    'South-East': 'Pointing towards the Crystal Caves of Wisdom, echoing with ancient cosmic knowledge.',
    'South': 'Directing you to the Heart of the Celestial Bloom, a place of infinite growth.',
    'South-West': 'Navigating you to the Whispering Void, where silence speaks volumes.',
    'West': 'Leading you to the Sunset of Illumination, where understanding dawns.',
    'North-West': 'Guiding you to the Echoing Constellations, where past and future dance.'
  };

  return {
    direction: direction,
    description: descriptions[direction]
  };
}

// Get cosmic event from command line arguments
const cosmicEventArg = process.argv[2];

if (!cosmicEventArg) {
  console.error('Error: Please provide a cosmic event as an argument.');
  console.error('Example: node src/main.js "Galactic Alignment"');
  process.exit(1);
}

const result = getCosmicDirection(cosmicEventArg);

console.log(`Your Cosmic Compass points ${result.direction}.`);
console.log(`\n${result.description}`);
