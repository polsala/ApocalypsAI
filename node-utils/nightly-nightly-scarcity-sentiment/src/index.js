const scarcityFactors = require('./scarcityData');

/**
 * Calculates the Scarcity Sentiment Score for an item.
 * The score is a combination of its base scarcity, perceived value, and how long it's been held.
 *
 * @param {string} itemName - The name of the item.
 * @param {string} category - The category of the item (e.g., "food", "medicine").
 * @param {number} perceivedValue - User's subjective value (1-10).
 * @param {number} daysHeld - How many days the item has been held (influences decay).
 * @returns {number} The calculated Scarcity Sentiment Score.
 */
function calculateScarcitySentiment(itemName, category, perceivedValue, daysHeld) {
  const factor = scarcityFactors[category.toLowerCase()] || scarcityFactors['misc'];

  // Base scarcity from predefined factors
  let score = factor.base;

  // Adjust by perceived value (user input)
  // Scales perceivedValue (1-10) to 0-1, then multiplies by valueMultiplier and a scaling factor (5)
  score += (perceivedValue / 10) * factor.valueMultiplier * 5;

  // Apply decay based on days held (monthly decay)
  score *= Math.pow(factor.decay, daysHeld / 30);

  return parseFloat(score.toFixed(2));
}

function runCli(args) {
  const item = args[0];
  const category = args[1];
  const value = parseInt(args[2], 10);
  const days = parseInt(args[3], 10);

  if (!item || !category || isNaN(value) || isNaN(days) || value < 1 || value > 10 || days < 0) {
    console.log("Usage: node src/index.js <itemName> <category> <perceivedValue(1-10)> <daysHeld>");
    console.log("Example: node src/index.js 'Can of Beans' food 8 60");
    console.log("\nAvailable categories:");
    console.log(Object.keys(scarcityFactors).join(', '));
    process.exit(1);
  }

  const score = calculateScarcitySentiment(item, category, value, days);
  console.log(`\n--- Scarcity Sentiment Report ---`);
  console.log(`Item: ${item}`);
  console.log(`Category: ${category}`);
  console.log(`Perceived Value: ${value}/10`);
  console.log(`Days Held: ${days}`);
  console.log(`\nCalculated Scarcity Sentiment Score: ${score}`);
  console.log(`---------------------------------`);
  console.log(`\nInterpretation: Higher score means more critical/valuable in current context.`);
  console.log(`Consider prioritizing items with higher scores for immediate use, secure storage, or strategic trade.`);
}

// Only run CLI if executed directly
if (require.main === module) {
  runCli(process.argv.slice(2));
}

module.exports = { calculateScarcitySentiment, scarcityFactors }; // Export for testing
