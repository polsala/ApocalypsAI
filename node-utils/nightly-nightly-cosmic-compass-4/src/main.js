const chalk = require('chalk');

// Mock celestial data for deterministic testing
const MOCK_CELESTIAL_DATA = {
    stars: {
        northStar: { name: 'Polaris', direction: 'North', significance: 'Your unwavering guide.' },
        pleiades: { name: 'Seven Sisters', direction: 'East', significance: 'A cluster of hope.' },
        orion: { name: 'Orion', direction: 'South', significance: 'The hunter watches over you.' }
    },
    moonPhase: 'Full Moon',
    sunPosition: 'West',
    lore: [
        "The stars whisper secrets to those who listen.",
        "When the moon is full, shadows lengthen, but so does courage.",
        "Follow the sun's dying light to find your way home.",
        "Even in darkness, the constellations remember."
    ]
};

/**
 * Generates a whimsical celestial navigation tip.
 * @returns {string} A navigation tip.
 */
function generateCosmicTip() {
    const starNames = Object.keys(MOCK_CELESTIAL_DATA.stars);
    const randomStarName = starNames[Math.floor(Math.random() * starNames.length)];
    const star = MOCK_CELESTIAL_DATA.stars[randomStarName];
    const randomLore = MOCK_CELESTIAL_DATA.lore[Math.floor(Math.random() * MOCK_CELESTIAL_DATA.lore.length)];

    let tip = `Look to the ${chalk.yellow(star.name)} (${chalk.cyan(star.direction)}). ${chalk.green(star.significance)}
`;
    tip += `The ${chalk.blue(MOCK_CELESTIAL_DATA.moonPhase)} watches. ${chalk.gray(randomLore)}
`;
    tip += `The sun sets in the ${chalk.red(MOCK_CELESTIAL_DATA.sunPosition)}. ${chalk.gray(MOCK_CELESTIAL_DATA.lore[1])}
`;

    return tip;
}

/**
 * Main function to display cosmic navigation advice.
 */
function main() {
    console.log(chalk.bold.magenta("✨ Welcome to the ApocalypsAI Cosmic Compass! ✨"));
    console.log("---------------------------------------------------");
    console.log(generateCosmicTip());
    console.log("---------------------------------------------------");
    console.log(chalk.italic("May the stars guide your path."));
}

// Execute the main function if the script is run directly
if (require.main === module) {
    main();
}

module.exports = { generateCosmicTip };
