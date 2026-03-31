const fortunes = [
  "You will find a hidden stash of snacks in the pantry.",
  "A sudden burst of inspiration will strike during your next coffee break.",
  "Beware of the mischievous squirrels; they plot in the shadows.",
  "Your code will compile on the first try—today is your lucky day.",
  "An unexpected compliment will brighten your afternoon.",
  "A stray cat will become your new debugging companion.",
  "The next commit you push will be praised by the gods of CI.",
  "A mysterious breeze will carry a hint of fresh ideas.",
  "Your keyboard will type itself for a moment—enjoy the surprise.",
  "A tiny victory today will lead to a grand triumph tomorrow."
];

/**
 * Select a fortune based on a numeric seed.
 * The selection is deterministic: index = |seed| % fortunes.length.
 * @param {number} seed - Integer seed (can be negative).
 * @returns {string} Selected fortune.
 */
function getFortune(seed) {
  const idx = Math.abs(seed) % fortunes.length;
  return fortunes[idx];
}

// When run as a GitHub Action, read the INPUT_SEED environment variable.
if (require.main === module) {
  const rawSeed = process.env['INPUT_SEED'] || '0';
  const seed = parseInt(rawSeed, 10) || 0;
  const fortune = getFortune(seed);
  // Emit the output using the legacy set-output command (compatible with all runners).
  console.log(`::set-output name=fortune::${fortune}`);
}

module.exports = { getFortune };
