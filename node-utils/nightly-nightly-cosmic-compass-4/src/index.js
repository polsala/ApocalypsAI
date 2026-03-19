const { getLunarPhase, getZodiacSign, getPlanetaryInfluence, getCosmicGuidance } = require('./cosmicData');

function runCosmicCompass() {
  const today = new Date();

  const lunarPhase = getLunarPhase(today);
  const zodiacSign = getZodiacSign(today);
  const planetaryInfluence = getPlanetaryInfluence(today);
  const { direction, activity } = getCosmicGuidance(lunarPhase, zodiacSign, planetaryInfluence);

  console.log("\n🌌 Nightly Cosmic Compass 🌌\n");
  console.log("Today's Cosmic Alignment:");
  console.log(`  Lunar Phase: ${lunarPhase}`);
  console.log(`  Zodiac Sign: ${zodiacSign}`);
  console.log(`  Planetary Influence: ${planetaryInfluence.planet} (${planetaryInfluence.influence})`);
  console.log("\nCosmic Direction: " + direction);
  console.log("Activity Suggestion: " + activity + "\n");
}

// Export for testing purposes
module.exports = {
  runCosmicCompass
};

// Run the CLI if executed directly
if (require.main === module) {
  runCosmicCompass();
}
