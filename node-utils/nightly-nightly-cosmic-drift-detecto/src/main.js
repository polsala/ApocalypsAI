const process = require('process');

// Function to generate a single data point with some noise
function generateCosmicReading(mean = 100, stdDev = 10) {
    const u1 = Math.random();
    const u2 = Math.random();
    const randStdNormal = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);
    return mean + stdDev * randStdNormal;
}

// Whimsical alerts for cosmic anomalies
const cosmicAlerts = [
    "A rogue nebula just zipped through the data stream! Prepare for unexpected stardust!",
    "The cosmic background radiation is acting a bit quirky today. Keep an eye out!",
    "Did a black hole just swallow a data packet? Readings are... unusual.",
    "A passing comet has left a trail of anomalous readings. Fascinating!",
    "The universe is humming a different tune! Anomaly detected.",
    "Looks like a wormhole opened up and warped some data points. Intriguing!"
];

function getRandomAlert() {
    return cosmicAlerts[Math.floor(Math.random() * cosmicAlerts.length)];
}

// Function to calculate mean and standard deviation
function calculateStats(data) {
    const n = data.length;
    if (n === 0) {
        return { mean: 0, stdDev: 0 };
    }
    const mean = data.reduce((sum, value) => sum + value, 0) / n;
    const variance = data.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / n;
    const stdDev = Math.sqrt(variance);
    return { mean, stdDev };
}

// Main function to run the detector
async function runCosmicDriftDetector(streamSize = 500, anomalyThreshold = 2) {
    console.log("Initializing cosmic data stream...");
    let dataStream = [];
    let currentMean = 0;
    let currentStdDev = 0;

    for (let i = 0; i < streamSize; i++) {
        const reading = generateCosmicReading();
        dataStream.push(reading);

        // Recalculate stats periodically or on every point for simplicity
        // For very large streams, a rolling average/std dev would be more efficient
        const stats = calculateStats(dataStream);
        currentMean = stats.mean;
        currentStdDev = stats.stdDev;

        const lowerBound = currentMean - anomalyThreshold * currentStdDev;
        const upperBound = currentMean + anomalyThreshold * currentStdDev;

        if (reading < lowerBound || reading > upperBound) {
            console.log(`\n✨ COSMIC ANOMALY DETECTED! ✨`);
            console.log(`  Reading: ${reading.toFixed(2)}`);
            console.log(`  Mean: ${currentMean.toFixed(2)}`);
            console.log(`  StdDev: ${currentStdDev.toFixed(2)}`);
            console.log(`  Alert: "${getRandomAlert()}"`);
        }

        // Simulate some delay between readings
        await new Promise(resolve => setTimeout(resolve, 10));
    }

    console.log("\nCosmic data stream simulation complete.");
}

// Parse command line arguments
const args = process.argv.slice(2);
const streamSizeArg = args.find(arg => arg.startsWith('--streamSize='));
const anomalyThresholdArg = args.find(arg => arg.startsWith('--anomalyThreshold='));

const streamSize = streamSizeArg ? parseInt(streamSizeArg.split('=')[1], 10) : 500;
const anomalyThreshold = anomalyThresholdArg ? parseFloat(anomalyThresholdArg.split('=')[1]) : 2;

runCosmicDriftDetector(streamSize, anomalyThreshold).catch(console.error);
