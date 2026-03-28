const fs = require('fs');
const path = require('path');

/**
 * Parses command-line arguments into an object.
 * @returns {Object} An object containing parsed arguments.
 */
function getArgs() {
    const args = {};
    process.argv.slice(2).forEach(arg => {
        if (arg.startsWith('--')) {
            const [key, value] = arg.substring(2).split('=');
            args[key] = value || true;
        }
    });
    return args;
}

/**
 * Determines the hemisphere based on latitude.
 * A small buffer is used for equatorial regions.
 * @param {number} latitude - The geographical latitude.
 * @returns {'Northern' | 'Southern' | 'Equatorial'} The determined hemisphere.
 */
function getHemisphere(latitude) {
    if (latitude > 5) return 'Northern';
    if (latitude < -5) return 'Southern';
    return 'Equatorial';
}

/**
 * Loads cosmic anomalies data from the JSON file.
 * @returns {Array<Object>} An array of cosmic anomaly objects.
 */
function getCosmicAnomalies() {
    const anomaliesPath = path.join(__dirname, 'cosmic_anomalies.json');
    // Mock rationale: In tests, fs.readFileSync is mocked to provide deterministic data.
    const data = fs.readFileSync(anomaliesPath, 'utf8');
    return JSON.parse(data);
}

/**
 * Finds the most influential cosmic anomaly visible from a given latitude on a specific date.
 * @param {number} latitude - The geographical latitude.
 * @param {Date} date - The date for which to check visibility.
 * @returns {Object | null} The most influential anomaly, or null if none are visible.
 */
function findMostInfluentialAnomaly(latitude, date) {
    const currentMonth = date.getMonth() + 1; // getMonth() is 0-indexed
    const userHemisphere = getHemisphere(latitude);
    const anomalies = getCosmicAnomalies();

    const visibleAnomalies = anomalies.filter(anomaly => {
        const isVisibleMonth = anomaly.visibility_months.includes(currentMonth);
        const isInHemisphere = anomaly.hemisphere.includes(userHemisphere);
        return isVisibleMonth && isInHemisphere;
    });

    if (visibleAnomalies.length === 0) {
        return null;
    }

    // Sort by influence_score in descending order to find the most influential
    visibleAnomalies.sort((a, b) => b.influence_score - a.influence_score);
    return visibleAnomalies[0];
}

/**
 * Main function to run the Cosmic Compass CLI.
 */
function run() {
    const args = getArgs();
    const latitude = parseFloat(args.lat);
    // const longitude = parseFloat(args.lon); // Longitude not used for this simplified version, but parsed.
    const dateStr = args.date;

    if (isNaN(latitude)) {
        console.error('Error: --lat=<latitude> is required and must be a number.');
        process.exit(1);
    }

    let targetDate;
    if (dateStr) {
        targetDate = new Date(dateStr);
        if (isNaN(targetDate.getTime())) {
            console.error('Error: Invalid date format. Use YYYY-MM-DD.');
            process.exit(1);
        }
    } else {
        // Mock rationale: In tests, the Date constructor is mocked to provide a fixed date.
        targetDate = new Date();
    }

    const anomaly = findMostInfluentialAnomaly(latitude, targetDate);

    if (anomaly) {
        console.log(`\n🌌 The Nightly Cosmic Compass reveals...`);
        console.log(`From your vantage point (${latitude}° latitude) on ${targetDate.toDateString()},`);
        console.log(`the most influential cosmic anomaly is:`);
        console.log(`✨ ${anomaly.name} ✨`);
        console.log(`"${anomaly.description}"`);
        console.log(`(Influence Score: ${anomaly.influence_score})`);
        console.log(`\nMay its cosmic whispers guide your path.`);
    } else {
        console.log(`\n🌌 The Nightly Cosmic Compass finds no prominent cosmic anomalies visible from your location on ${targetDate.toDateString()}.`);
        console.log(`Perhaps the void holds its secrets close tonight, or new wonders await discovery!`);
    }
}

// Only run if not being imported (e.g., by tests)
if (require.main === module) {
    run();
}

// Export for testing purposes
module.exports = {
    getArgs,
    getHemisphere,
    getCosmicAnomalies, // Exported for mocking in tests
    findMostInfluentialAnomaly,
    run
};
