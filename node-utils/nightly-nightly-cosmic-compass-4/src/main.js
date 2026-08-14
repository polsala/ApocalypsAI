const moment = require('moment');

// Mock rationale: This array simulates potential cosmic events for whimsical output.
const COSMIC_EVENTS = [
  "Nebula's Whisper",
  "Quasar's Giggle",
  "Supernova's Sigh",
  "Black Hole's Hum",
  "Comet's Trail",
  "Asteroid's Dance",
  "Galactic Bloom",
  "Stardust Serenade",
  "Cosmic Ray's Kiss",
  "Pulsar's Pulse"
];

// Mock rationale: This array provides whimsical interpretations for celestial bearings.
const BEARING_INTERPRETATIONS = [
  "Follow the faint shimmer, and you might just find a nebula that sings your name.",
  "This direction leads to the echoes of creation, where new stars are born.",
  "A path less traveled, rumored to be guarded by benevolent space whales.",
  "The stars align here for moments of profound cosmic insight. Listen closely.",
  "Beware the gravitational pull of this direction; it may lead to unexpected adventures.",
  "A gentle breeze of cosmic dust will guide you. Trust your intuition.",
  "This bearing points towards a celestial library, filled with the stories of the universe.",
  "The void whispers secrets here. Seek the quietest corners.",
  "A vibrant tapestry of nebulae awaits. Prepare for a visual feast.",
  "The energy here is potent. Use it to fuel your journey."
];

/**
 * Generates a random cosmic event.
 * @returns {string} A whimsical cosmic event.
 */
function generateCosmicEvent() {
  const randomIndex = Math.floor(Math.random() * COSMIC_EVENTS.length);
  return COSMIC_EVENTS[randomIndex];
}

/**
 * Calculates a celestial bearing based on time and a cosmic event.
 * @param {string} event - The cosmic event string.
 * @returns {number} A bearing in degrees (0-360).
 */
function calculateCelestialBearing(event) {
  const now = moment();
  const timeInSeconds = now.unix();
  let eventHash = 0;
  for (let i = 0; i < event.length; i++) {
    eventHash = (eventHash << 5) - eventHash + event.charCodeAt(i);
    eventHash |= 0; // Convert to 32bit integer
  }

  // Combine time and event hash for a pseudo-random but deterministic result for a given time/event
  const combinedValue = timeInSeconds + eventHash;
  const bearing = (Math.abs(combinedValue) % 360);
  return bearing;
}

/**
 * Provides a whimsical interpretation for a given bearing.
 * @param {number} bearing - The celestial bearing in degrees.
 * @returns {string} A whimsical interpretation.
 */
function interpretBearing(bearing) {
  // Use bearing to pick an interpretation, ensuring it wraps around the array length
  const randomIndex = Math.floor(bearing / (360 / BEARING_INTERPRETATIONS.length));
  return BEARING_INTERPRETATIONS[randomIndex % BEARING_INTERPRETATIONS.length];
}

/**
 * Formats the bearing into a human-readable direction.
 * @param {number} bearing - The celestial bearing in degrees.
 * @returns {string} The direction (e.g., "North", "South-Southeast").
 */
function formatBearingDirection(bearing) {
  const directions = [
    "North", "North-Northeast", "Northeast", "East-Northeast", "East",
    "East-Southeast", "Southeast", "South-Southeast", "South", "South-Southwest",
    "Southwest", "West-Southwest", "West", "West-Northwest", "Northwest",
    "North-Northwest"
  ];
  const index = Math.floor((bearing + 11.25) / 22.5);
  return directions[index % directions.length];
}

function displayCosmicCompass() {
  const cosmicEvent = generateCosmicEvent();
  const bearing = calculateCelestialBearing(cosmicEvent);
  const interpretation = interpretBearing(bearing);
  const direction = formatBearingDirection(bearing);

  console.log("✨ Cosmic Compass Report ✨");
  console.log(`\nTime: ${moment().toISOString()}`);
  console.log(`Cosmic Event: ${cosmicEvent}`);
  console.log(`\nYour Celestial Bearing: ${bearing} degrees (${direction})`);
  console.log(`\nInterpretation: ${interpretation}`);
}

// Execute the compass
displayCosmicCompass();

module.exports = { generateCosmicEvent, calculateCelestialBearing, interpretBearing, formatBearingDirection, displayCosmicCompass };
