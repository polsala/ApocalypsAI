const fs = require('fs').promises;
const path = require('path');

/**
 * Generates a whimsical weather forecast based on environmental data.
 * @param {object} envData - Environmental data object.
 * @param {number} envData.temperature - Temperature in Celsius.
 * @param {number} envData.radiation_level - Radiation level in Sieverts.
 * @param {number} envData.anomaly_index - Anomaly index (0.0-1.0).
 * @param {number} envData.wind_speed - Wind speed in km/h.
 * @param {number} envData.temporal_stability - Temporal stability (0.0-1.0).
 * @returns {string} The whimsical weather forecast.
 */
function generateForecast(envData) {
    let forecast = [];

    // Temperature
    if (envData.temperature < 0) {
        forecast.push("The air bites with a Frost-Kissed Chill.");
    } else if (envData.temperature < 10) {
        forecast.push("A crisp, cool breeze whispers through the ruins.");
    } else if (envData.temperature < 25) {
        forecast.push("Mild currents drift across the wasteland.");
    } else if (envData.temperature < 35) {
        forecast.push("The sun beats down, bringing a Warm Glow.");
    } else {
        forecast.push("A Scorching Aura permeates the atmosphere.");
    }

    // Radiation
    if (envData.radiation_level > 0.5) {
        forecast.push("High radiation levels suggest a Blight Bloom on the horizon.");
    } else if (envData.radiation_level > 0.1) {
        forecast.push("A faint, shimmering Radiant Haze is present.");
    } else {
        forecast.push("Radiation levels are stable, offering clear skies (of sorts).");
    }

    // Anomaly Index
    if (envData.anomaly_index > 0.7) {
        forecast.push("Expect significant Temporal Distortions and reality ripples.");
    } else if (envData.anomaly_index > 0.3) {
        forecast.push("Minor Chrono-Flickers might be observed.");
    } else {
        forecast.push("Temporal currents are unusually calm.");
    }

    // Wind Speed
    if (envData.wind_speed > 40) {
        forecast.push("Beware the Gale-Force Whispers, they carry dust and secrets.");
    } else if (envData.wind_speed > 15) {
        forecast.push("A brisk Wind-Scour sweeps across the plains.");
    } else {
        forecast.push("Gentle breezes stir the dust.");
    }

    // Temporal Stability
    if (envData.temporal_stability < 0.3) {
        forecast.push("The fabric of time feels thin; prepare for unexpected echoes.");
    } else if (envData.temporal_stability < 0.7) {
        forecast.push("Temporal eddies are active, causing minor temporal drizzle.");
    } else {
        forecast.push("The timeline holds firm, for now.");
    }

    return forecast.join(" ");
}

async function main(filePath) {
    const defaultPath = path.join(__dirname, '..', 'data', 'environment.json');
    const dataPath = filePath || defaultPath;

    try {
        const data = await fs.readFile(dataPath, 'utf8');
        const envData = JSON.parse(data);
        const forecast = generateForecast(envData);
        console.log("Whisperwind Weather Vane Forecast:");
        console.log(forecast);
    } catch (error) {
        console.error(`Error reading or parsing environment data from ${dataPath}:`, error.message);
        process.exit(1);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    const args = process.argv.slice(2);
    main(args[0]);
}

module.exports = { generateForecast, main }; // Export for testing
