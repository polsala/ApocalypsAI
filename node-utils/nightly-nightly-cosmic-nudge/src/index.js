#!/usr/bin/env node

const defaultNudges = [
    "Scavenge for supplies",
    "Repair a broken tool",
    "Meditate on the void",
    "Organize your survival stash",
    "Help a fellow survivor",
    "Explore the nearby ruins",
    "Rest and recuperate",
    "Sharpen your wits with a puzzle",
    "Tend to the hydroponic garden",
    "Update your logbook"
];

/**
 * Selects a random item from an array.
 * @param {Array<string>} options - The array of options to choose from.
 * @returns {string} A randomly selected option.
 */
function getRandomNudge(options) {
    if (!options || options.length === 0) {
        return "Contemplate the infinite emptiness."; // Default for no options
    }
    const randomIndex = Math.floor(Math.random() * options.length);
    return options[randomIndex];
}

/**
 * Main function to run the Cosmic Nudge CLI.
 */
function main() {
    const args = process.argv.slice(2); // Get arguments after 'node src/index.js'

    let optionsToUse;
    if (args.length > 0) {
        optionsToUse = args;
    } else {
        optionsToUse = defaultNudges;
    }

    const nudge = getRandomNudge(optionsToUse);
    console.log(`🌌 The cosmos whispers: ${nudge}`);
}

// Only run main if this script is executed directly
if (require.main === module) {
    main();
}

module.exports = {
    getRandomNudge,
    defaultNudges
};
